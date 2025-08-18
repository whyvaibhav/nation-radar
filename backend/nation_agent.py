#!/usr/bin/env python3
"""
Shared utilities for scoring via Crestal Nation Agent.

Exports:
- format_tweet_for_agent(tweet: dict) -> str
- get_agent_score(formatted_text: str) -> float
"""

import re
import requests
from typing import Dict, Any

from config import NATION_AGENT_API_KEY


def extract_score(agent_response: str) -> float:
    """Extract the first floating point or integer number from the agent's response.

    Returns 0.0 if parsing fails.
    """
    if not isinstance(agent_response, str):
        return 0.0
    match = re.search(r"(-?\d+\.\d+|-?\d+)", agent_response)
    if match:
        try:
            return float(match.group(0))
        except ValueError:
            return 0.0
    return 0.0


def normalize_agent_score(score: float) -> float:
    """Clamp and sanitize raw scores to the 0.0–2.0 range.

    Any non-finite or None inputs map to 0.0. Values above 2.0 become 2.0; below 0.0 become 0.0.
    """
    try:
        s = float(score)
    except Exception:
        return 0.0
    if s != s:  # NaN
        return 0.0
    if s < 0.0:
        return 0.0
    if s > 2.0:
        return 2.0
    return s


def format_tweet_for_agent(tweet: Dict[str, Any]) -> str:
    """Format tweet content and engagement for the Nation Agent prompt."""
    text = tweet.get("text", "")
    engagement = tweet.get("engagement", {}) or {}
    engagement_str = (
        f"Likes: {engagement.get('likes', 0)}, "
        f"Retweets: {engagement.get('retweets', 0)}, "
        f"Replies: {engagement.get('replies', 0)}, "
        f"Views: {engagement.get('views', 0)}, "
        f"Bookmarks: {engagement.get('bookmarks', 0)}, "
        f"Quote Tweets: {engagement.get('quote_tweets', 0)}"
    )
    return f"{text}\n\nEngagement: {engagement_str}"


def get_agent_score(formatted_text: str, timeout_create: int = 15, timeout_message: int = 30) -> float:
    """Send formatted text to Nation Agent API and extract a numeric score.

    Returns 0.0 if any error occurs.
    """
    base_url = "https://open.service.crestal.network/v1"
    headers = {
        "Authorization": f"Bearer {NATION_AGENT_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        # Create chat thread
        resp = requests.post(f"{base_url}/chats", headers=headers, timeout=timeout_create)
        resp.raise_for_status()
        chat_id = resp.json().get("id")
        if not chat_id:
            return 0.0

        # Send message
        data = {"message": formatted_text}
        msg_resp = requests.post(
            f"{base_url}/chats/{chat_id}/messages",
            headers=headers,
            json=data,
            timeout=timeout_message,
        )
        msg_resp.raise_for_status()
        messages = msg_resp.json()

        # messages can be a list of {message: str} or a dict {message: str}
        if isinstance(messages, list) and messages:
            agent_response = messages[-1].get("message", "")
        elif isinstance(messages, dict) and "message" in messages:
            agent_response = messages.get("message", "")
        else:
            agent_response = ""

        raw = extract_score(agent_response)
        return normalize_agent_score(raw)

    except Exception:
        return 0.0


