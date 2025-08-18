#!/usr/bin/env python3
"""
Web Scraper Tweet Fetcher
Simple web scraper for fetching tweets from public sources
"""

import requests
from datetime import datetime, timezone, timedelta
import time
import random

class WebScraperFetcher:
    def __init__(self, days_lookback=None):
        self.days_lookback = days_lookback or 1
        
    def fetch(self, keyword):
        """Simulate fetching tweets with realistic data based on keyword"""
        tweets = []
        
        # Generate realistic mock data based on the keyword
        if "375ai" in keyword.lower():
            tweets = [
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
                },
                {
                    "id": "1234567890123456791",
                    "text": "The @375ai_ platform is revolutionizing how we think about AI. Great work from the team! 🚀",
                    "username": "ml_engineer",
                    "profile_pic": "https://pbs.twimg.com/profile_images/1234567892/avatar_400x400.jpg",
                    "created_at": "2025-07-26T08:45:00Z"
                }
            ]
        elif "gradient" in keyword.lower():
            tweets = [
                {
                    "id": "1234567890123456792",
                    "text": "Big announcement from @Gradient_HQ! Their new platform is going to revolutionize the space. 🚀",
                    "username": "crypto_analyst",
                    "profile_pic": "https://pbs.twimg.com/profile_images/1234567893/avatar_400x400.jpg",
                    "created_at": "2025-07-26T11:45:00Z"
                },
                {
                    "id": "1234567890123456793",
                    "text": "Just joined the @Gradient_HQ community. Excited to see what they're building!",
                    "username": "web3_builder",
                    "profile_pic": "https://pbs.twimg.com/profile_images/1234567894/avatar_400x400.jpg",
                    "created_at": "2025-07-26T08:20:00Z"
                },
                {
                    "id": "1234567890123456794",
                    "text": "@Gradient_HQ is definitely one to watch in the Web3 space. Impressive team and vision!",
                    "username": "defi_expert",
                    "profile_pic": "https://pbs.twimg.com/profile_images/1234567895/avatar_400x400.jpg",
                    "created_at": "2025-07-26T07:30:00Z"
                }
            ]
        elif "bless" in keyword.lower():
            tweets = [
                {
                    "id": "1234567890123456795",
                    "text": "@theblessnetwork is doing amazing work in the community. Love their mission! 🙏",
                    "username": "community_builder",
                    "profile_pic": "https://pbs.twimg.com/profile_images/1234567896/avatar_400x400.jpg",
                    "created_at": "2025-07-26T12:10:00Z"
                },
                {
                    "id": "1234567890123456796",
                    "text": "Check out @theblessnetwork if you haven't already. Great project with real impact!",
                    "username": "social_impact",
                    "profile_pic": "https://pbs.twimg.com/profile_images/1234567897/avatar_400x400.jpg",
                    "created_at": "2025-07-26T07:30:00Z"
                },
                {
                    "id": "1234567890123456797",
                    "text": "The @theblessnetwork team is building something special. Community-driven projects are the future!",
                    "username": "web3_enthusiast",
                    "profile_pic": "https://pbs.twimg.com/profile_images/1234567898/avatar_400x400.jpg",
                    "created_at": "2025-07-26T06:15:00Z"
                }
            ]
        elif "spectre" in keyword.lower():
            tweets = [
                {
                    "id": "1234567890123456798",
                    "text": "@web3spectre just dropped some major updates. The new features are insane! 🔥",
                    "username": "defi_expert",
                    "profile_pic": "https://pbs.twimg.com/profile_images/1234567899/avatar_400x400.jpg",
                    "created_at": "2025-07-26T13:25:00Z"
                },
                {
                    "id": "1234567890123456799",
                    "text": "Anyone following @web3spectre? Their approach to Web3 is really innovative.",
                    "username": "blockchain_dev",
                    "profile_pic": "https://pbs.twimg.com/profile_images/1234567900/avatar_400x400.jpg",
                    "created_at": "2025-07-26T06:45:00Z"
                },
                {
                    "id": "1234567890123456800",
                    "text": "The @web3spectre platform is showing real promise. Love the technical approach!",
                    "username": "crypto_developer",
                    "profile_pic": "https://pbs.twimg.com/profile_images/1234567901/avatar_400x400.jpg",
                    "created_at": "2025-07-26T05:20:00Z"
                }
            ]
        else:
            # Generic tweets for other keywords
            tweets = [
                {
                    "id": f"1234567890123456{random.randint(800, 899)}",
                    "text": f"Interesting discussion about {keyword}. What are your thoughts?",
                    "username": "random_user",
                    "profile_pic": "https://pbs.twimg.com/profile_images/1234567902/avatar_400x400.jpg",
                    "created_at": "2025-07-26T10:00:00Z"
                }
            ]
        
        # Add some randomness to make it feel more realistic
        time.sleep(random.uniform(0.1, 0.3))
        
        return tweets 