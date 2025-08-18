#!/usr/bin/env python3
"""
Local text normalization and duplicate filtering utilities.

Goals:
- Normalize tweet text so copy/paste reposts hash the same
- Pick the earliest created_at for identical content within a batch
"""

import html
import re
import hashlib
from datetime import datetime
from typing import Dict, List, Set
from pathlib import Path


_URL_PATTERN = re.compile(r"https?://\S+", re.IGNORECASE)
_WHITESPACE_PATTERN = re.compile(r"\s+")
_RETWEET_PREFIX = re.compile(r"^rt\s+@\w+:\s*", re.IGNORECASE)

# Map common smart punctuation to ASCII equivalents
_SMART_PUNCT_MAP = str.maketrans({
    "’": "'",
    "‘": "'",
    "´": "'",
    "`": "'",
    "“": '"',
    "”": '"',
    "–": "-",
    "—": "-",
    "…": "...",
    "\xa0": " ",  # non-breaking space
})


def normalize_tweet_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    unescaped = html.unescape(text)
    normalized_quotes = unescaped.translate(_SMART_PUNCT_MAP)
    lowercased = normalized_quotes.lower()
    # Remove common RT prefix noise so retweets of same text normalize together
    no_rt = _RETWEET_PREFIX.sub("", lowercased)
    no_urls = _URL_PATTERN.sub("", no_rt)
    collapsed = _WHITESPACE_PATTERN.sub(" ", no_urls)
    cleaned = collapsed.strip().strip('"').strip("'")
    # Drop trailing punctuation-only endings (e.g., repeated dots/exclamations)
    cleaned = re.sub(r"[\.!?]+$", "", cleaned).strip()
    return cleaned


def compute_text_hash(text: str) -> str:
    normalized = normalize_tweet_text(text)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def parse_twitter_date(date_str: str) -> datetime:
    # Example: Mon Aug 11 12:15:23 +0000 2025
    try:
        return datetime.strptime(date_str, "%a %b %d %H:%M:%S %z %Y")
    except Exception:
        # Fallback: treat as very late if unknown, so won't win "earliest"
        return datetime.max.replace(tzinfo=None)


def earliest_unique_tweets(tweets: List[Dict]) -> List[Dict]:
    """Return only the earliest tweet per normalized text within the provided list."""
    by_hash: Dict[str, Dict] = {}
    for tw in tweets:
        text = tw.get("text", "")
        content_hash = compute_text_hash(text)
        created_at = parse_twitter_date(tw.get("created_at", ""))
        existing = by_hash.get(content_hash)
        if existing is None:
            by_hash[content_hash] = {"tweet": tw, "created_at": created_at}
        else:
            if created_at < existing["created_at"]:
                by_hash[content_hash] = {"tweet": tw, "created_at": created_at}

    return [entry["tweet"] for entry in by_hash.values()]


def load_seen_hashes(file_path: str = "seen_text_hashes.txt") -> Set[str]:
    path = Path(file_path)
    if not path.exists():
        return set()
    try:
        return set(h.strip() for h in path.read_text(encoding="utf-8").splitlines() if h.strip())
    except Exception:
        return set()


def save_seen_hashes(hashes: Set[str], file_path: str = "seen_text_hashes.txt") -> None:
    path = Path(file_path)
    try:
        path.write_text("\n".join(sorted(hashes)) + "\n", encoding="utf-8")
    except Exception:
        # Best-effort persistence; ignore failures
        pass


