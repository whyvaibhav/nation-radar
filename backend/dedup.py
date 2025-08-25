#!/usr/bin/env python3
"""
Local text normalization and duplicate filtering utilities.

Goals:
- Remove exact duplicates and retweets
- Keep unique content even if similar
- Less aggressive normalization to preserve content diversity
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
    "'": "'",
    "'": "'",
    "´": "'",
    "`": "'",
    """: '"',
    """: '"',
    "–": "-",
    "—": "-",
    "…": "...",
    "\xa0": " ",  # non-breaking space
})


def normalize_tweet_text(text: str) -> str:
    """
    Less aggressive normalization - only removes obvious noise
    """
    if not isinstance(text, str):
        return ""
    
    # Basic cleaning only
    unescaped = html.unescape(text)
    normalized_quotes = unescaped.translate(_SMART_PUNCT_MAP)
    lowercased = normalized_quotes.lower()
    
    # Remove RT prefix for retweet detection
    no_rt = _RETWEET_PREFIX.sub("", lowercased)
    
    # Remove URLs but keep the rest of the content
    no_urls = _URL_PATTERN.sub("", no_rt)
    
    # Normalize whitespace
    collapsed = _WHITESPACE_PATTERN.sub(" ", no_urls)
    cleaned = collapsed.strip()
    
    return cleaned


def compute_text_hash(text: str) -> str:
    """
    Compute hash of normalized text for duplicate detection
    """
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
    """
    Return only the earliest tweet per normalized text within the provided list.
    Less aggressive - only removes exact duplicates and retweets.
    """
    by_hash: Dict[str, Dict] = {}
    
    for tw in tweets:
        text = tw.get("text", "")
        
        # Skip empty tweets
        if not text.strip():
            continue
            
        content_hash = compute_text_hash(text)
        created_at = parse_twitter_date(tw.get("created_at", ""))
        
        existing = by_hash.get(content_hash)
        if existing is None:
            by_hash[content_hash] = {"tweet": tw, "created_at": created_at}
        else:
            # Keep the earliest tweet
            if created_at < existing["created_at"]:
                by_hash[content_hash] = {"tweet": tw, "created_at": created_at}

    return [entry["tweet"] for entry in by_hash.values()]


def load_seen_hashes(file_path: str = "seen_text_hashes.txt") -> Set[str]:
    """
    Load previously seen content hashes
    """
    path = Path(file_path)
    if not path.exists():
        return set()
    try:
        return set(h.strip() for h in path.read_text(encoding="utf-8").splitlines() if h.strip())
    except Exception:
        return set()


def save_seen_hashes(hashes: Set[str], file_path: str = "seen_text_hashes.txt") -> None:
    """
    Save content hashes for future deduplication
    """
    path = Path(file_path)
    try:
        path.write_text("\n".join(sorted(hashes)) + "\n", encoding="utf-8")
    except Exception:
        # Best-effort persistence; ignore failures
        pass


def is_similar_content(text1: str, text2: str, similarity_threshold: float = 0.9) -> bool:
    """
    Check if two texts are very similar (for advanced deduplication)
    """
    # Simple similarity check - can be enhanced with more sophisticated algorithms
    normalized1 = normalize_tweet_text(text1)
    normalized2 = normalize_tweet_text(text2)
    
    # If they're exactly the same after normalization, they're duplicates
    if normalized1 == normalized2:
        return True
    
    # For now, only exact matches are considered duplicates
    # This can be enhanced with fuzzy matching if needed
    return False


