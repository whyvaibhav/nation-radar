#!/usr/bin/env python3
"""
Local tests for dedup utilities.
Run: python test_dedup_local.py
"""

from dedup import normalize_tweet_text, compute_text_hash, earliest_unique_tweets


def test_normalize_and_hash_same_for_reposts():
    a = "Crestal Network is awesome! https://x.com/abc\n"
    b = "  crestal network is AWESOME!  https://x.com/def  "
    assert normalize_tweet_text(a) == normalize_tweet_text(b)
    assert compute_text_hash(a) == compute_text_hash(b)


def test_earliest_wins():
    tweets = [
        {"id": "2", "text": "Hello World", "created_at": "Mon Aug 11 12:16:00 +0000 2025"},
        {"id": "1", "text": "Hello World", "created_at": "Mon Aug 11 12:15:00 +0000 2025"},
        {"id": "3", "text": "Different text", "created_at": "Mon Aug 11 12:17:00 +0000 2025"},
    ]
    unique = earliest_unique_tweets(tweets)
    ids = sorted(t["id"] for t in unique)
    assert set(ids) == {"1", "3"}


if __name__ == "__main__":
    test_normalize_and_hash_same_for_reposts()
    test_earliest_wins()
    print("Dedup local tests passed.")


