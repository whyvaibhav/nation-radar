#!/usr/bin/env python3
"""
RapidAPI Twitter Fetcher
Uses RapidAPI's Twitter API with free tier
"""

import requests
import os
from datetime import datetime, timezone, timedelta
import time

class RapidAPIFetcher:
    def __init__(self, days_lookback=None):
        self.days_lookback = days_lookback or 1
        # RapidAPI Twitter API endpoint
        self.url = "https://twitter154.p.rapidapi.com/search/search"
        
    def fetch(self, keyword):
        """Fetch tweets for a keyword using RapidAPI"""
        tweets = []
        
        # Calculate the date range
        since_date = datetime.now(timezone.utc) - timedelta(days=self.days_lookback)
        since_str = since_date.strftime("%Y-%m-%d")
        
        headers = {
            "X-RapidAPI-Key": os.getenv('RAPIDAPI_KEY', 'YOUR_RAPIDAPI_KEY'),  # Set this in .env
            "X-RapidAPI-Host": "twitter154.p.rapidapi.com"
        }
        
        querystring = {
            "query": keyword,
            "section": "top",
            "min_retweets": "0",
            "min_likes": "0",
            "min_replies": "0",
            "limit": "20"
        }
        
        try:
            response = requests.get(self.url, headers=headers, params=querystring)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                for tweet in results:
                    tweets.append({
                        "id": str(tweet.get('tweet_id', '')),
                        "text": tweet.get('text', ''),
                        "username": tweet.get('user', {}).get('username', 'unknown'),
                        "profile_pic": tweet.get('user', {}).get('profile_pic_url', ''),
                        "created_at": tweet.get('creation_date', '')
                    })
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"Error fetching tweets for {keyword}: {e}")
            
        return tweets 