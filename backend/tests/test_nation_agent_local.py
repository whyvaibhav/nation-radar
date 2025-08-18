#!/usr/bin/env python3
"""
Lightweight local tests for Nation Agent utilities.
Run: python test_nation_agent_local.py
"""

from nation_agent import format_tweet_for_agent, extract_score


def test_format_tweet_for_agent():
    tweet = {
        "text": "Hello $NATION!",
        "engagement": {
            "likes": 10,
            "retweets": 2,
            "replies": 1,
            "views": 100,
            "bookmarks": 0,
            "quote_tweets": 1,
        },
    }
    formatted = format_tweet_for_agent(tweet)
    assert "Hello $NATION!" in formatted
    assert "Engagement:" in formatted
    assert "Likes: 10" in formatted


def test_extract_score():
    assert extract_score("1.23") == 1.23
    assert extract_score("Score: 0.75") == 0.75
    assert extract_score("-0.5") == -0.5
    assert extract_score("No number here") == 0.0


if __name__ == "__main__":
    test_format_tweet_for_agent()
    test_extract_score()
    print("All local tests passed.")


