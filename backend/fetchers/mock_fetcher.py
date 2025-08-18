#!/usr/bin/env python3
"""
Mock Tweet Fetcher for testing purposes
Simulates tweet data when real API is unavailable
"""

import random
from datetime import datetime, timezone, timedelta

class MockFetcher:
    def __init__(self, days_lookback=None):
        self.days_lookback = days_lookback or 1
        
    def fetch(self, keyword):
        """Simulate fetching tweets for a keyword"""
        # Generate some mock tweets based on the keyword
        mock_tweets = []
        
        # Different mock data based on keyword
        if "375ai" in keyword.lower():
            mock_tweets = [
                {
                    "id": "1234567890123456789",
                    "text": "Just discovered @375ai_ and it's absolutely mind-blowing! The AI capabilities are incredible. #AI #Innovation",
                    "username": "tech_enthusiast",
                    "profile_pic": "https://pbs.twimg.com/profile_images/1234567890/avatar_400x400.jpg",
                    "created_at": "2025-07-26T10:30:00Z"
                },
                {
                    "id": "1234567890123456790",
                    "text": "Anyone tried @375ai_ yet? Looking for reviews and experiences. Seems promising!",
                    "username": "ai_researcher",
                    "profile_pic": "https://pbs.twimg.com/profile_images/1234567891/avatar_400x400.jpg",
                    "created_at": "2025-07-26T09:15:00Z"
                }
            ]
        elif "gradient" in keyword.lower():
            mock_tweets = [
                {
                    "id": "1234567890123456791",
                    "text": "Big announcement from @Gradient_HQ! Their new platform is going to revolutionize the space. 🚀",
                    "username": "crypto_analyst",
                    "profile_pic": "https://pbs.twimg.com/profile_images/1234567892/avatar_400x400.jpg",
                    "created_at": "2025-07-26T11:45:00Z"
                },
                {
                    "id": "1234567890123456792",
                    "text": "Just joined the @Gradient_HQ community. Excited to see what they're building!",
                    "username": "web3_builder",
                    "profile_pic": "https://pbs.twimg.com/profile_images/1234567893/avatar_400x400.jpg",
                    "created_at": "2025-07-26T08:20:00Z"
                }
            ]
        elif "bless" in keyword.lower():
            mock_tweets = [
                {
                    "id": "1234567890123456793",
                    "text": "@theblessnetwork is doing amazing work in the community. Love their mission! 🙏",
                    "username": "community_builder",
                    "profile_pic": "https://pbs.twimg.com/profile_images/1234567894/avatar_400x400.jpg",
                    "created_at": "2025-07-26T12:10:00Z"
                },
                {
                    "id": "1234567890123456794",
                    "text": "Check out @theblessnetwork if you haven't already. Great project with real impact!",
                    "username": "social_impact",
                    "profile_pic": "https://pbs.twimg.com/profile_images/1234567895/avatar_400x400.jpg",
                    "created_at": "2025-07-26T07:30:00Z"
                }
            ]
        elif "spectre" in keyword.lower():
            mock_tweets = [
                {
                    "id": "1234567890123456795",
                    "text": "@web3spectre just dropped some major updates. The new features are insane! 🔥",
                    "username": "defi_expert",
                    "profile_pic": "https://pbs.twimg.com/profile_images/1234567896/avatar_400x400.jpg",
                    "created_at": "2025-07-26T13:25:00Z"
                },
                {
                    "id": "1234567890123456796",
                    "text": "Anyone following @web3spectre? Their approach to Web3 is really innovative.",
                    "username": "blockchain_dev",
                    "profile_pic": "https://pbs.twimg.com/profile_images/1234567897/avatar_400x400.jpg",
                    "created_at": "2025-07-26T06:45:00Z"
                }
            ]
        else:
            # Generic mock tweets for other keywords
            mock_tweets = [
                {
                    "id": f"1234567890123456{random.randint(700, 799)}",
                    "text": f"Interesting discussion about {keyword}. What are your thoughts?",
                    "username": "random_user",
                    "profile_pic": "https://pbs.twimg.com/profile_images/1234567898/avatar_400x400.jpg",
                    "created_at": "2025-07-26T10:00:00Z"
                }
            ]
        
        return mock_tweets 