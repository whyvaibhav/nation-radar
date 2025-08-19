#!/usr/bin/env python3
"""
SQLite-based storage with content-hash deduplication for scale.

- Ensures each tweet id is stored once (PRIMARY KEY)
- Ensures each normalized content hash is stored once (content_hashes)
  so copy/paste reposts are rejected across runs

append_row(tweet: dict) -> bool
  - Returns True if the tweet is newly stored; False if skipped as duplicate
"""

from __future__ import annotations

import json
import os
import sqlite3
from typing import Optional

from dedup import compute_text_hash


class SQLiteStorage:
    def __init__(self, db_path: str = "tweets.db") -> None:
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tweets (
                id TEXT PRIMARY KEY,
                username TEXT,
                text TEXT,
                score REAL,
                url TEXT,
                created_at TEXT,
                engagement TEXT,
                inserted_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS content_hashes (
                content_hash TEXT PRIMARY KEY,
                canonical_tweet_id TEXT,
                first_seen_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        self.conn.commit()

    @staticmethod
    def _tweet_url(username: str, tweet_id: str) -> str:
        return f"https://x.com/{username}/status/{tweet_id}"

    def append_row(self, tweet: dict) -> bool:
        tweet_id: Optional[str] = tweet.get("id")
        username: str = tweet.get("username", "")
        text: str = tweet.get("text", "")
        score: float = float(tweet.get("score", 0.0) or 0.0)
        created_at: str = tweet.get("created_at", "")
        engagement_json: str = json.dumps(tweet.get("engagement", {}), ensure_ascii=False)
        url: str = self._tweet_url(username, tweet_id) if tweet_id and username else ""

        if not tweet_id:
            return False

        content_hash = compute_text_hash(text)

        cur = self.conn.cursor()
        # Reject if content hash already seen
        cur.execute("SELECT 1 FROM content_hashes WHERE content_hash = ?", (content_hash,))
        if cur.fetchone():
            return False

        # Insert tweet row if not exists
        try:
            cur.execute(
                "INSERT INTO tweets (id, username, text, score, url, created_at, engagement) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (tweet_id, username, text, score, url, created_at, engagement_json),
            )
        except sqlite3.IntegrityError:
            # Tweet id already exists; treat as duplicate
            return False

        # Mark content hash as seen with this canonical tweet id
        cur.execute(
            "INSERT OR IGNORE INTO content_hashes (content_hash, canonical_tweet_id) VALUES (?, ?)",
            (content_hash, tweet_id),
        )
        self.conn.commit()
        return True

    def get_all_tweets(self) -> list:
        """Get all tweets from the database"""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id, username, text, score, url, created_at, engagement
            FROM tweets 
            ORDER BY score DESC
        """)
        
        tweets = []
        for row in cur.fetchall():
            tweet = {
                'id': row[0],
                'username': row[1],
                'text': row[2],
                'score': row[3],
                'url': row[4],
                'created_at': row[5],
                'engagement': json.loads(row[6]) if row[6] else {}
            }
            tweets.append(tweet)
        
        return tweets

    def close(self) -> None:
        try:
            self.conn.close()
        except Exception:
            pass


