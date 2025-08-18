#!/usr/bin/env python3
"""
Snscrape Tweet Fetcher
Uses snscrape library to fetch tweets without API keys
"""

import snscrape.modules.twitter as sntwitter
from datetime import datetime, timezone, timedelta
import time

class SnscrapeFetcher:
    def __init__(self, days_lookback=None):
        self.days_lookback = days_lookback or 1
        
    def fetch(self, keyword):
        """Fetch tweets for a keyword using snscrape"""
        tweets = []
        
        # Calculate the date range
        since_date = datetime.now(timezone.utc) - timedelta(days=self.days_lookback)
        since_str = since_date.strftime("%Y-%m-%d")
        
        # Build the search query
        query = f"{keyword} since:{since_str}"
        
        try:
            # Use snscrape to search tweets
            scraper = sntwitter.TwitterSearchScraper(query)
            
            # Limit to 100 tweets per keyword to avoid rate limiting
            for i, tweet in enumerate(scraper.get_items()):
                if i >= 100:  # Limit results
                    break
                    
                tweets.append({
                    "id": str(tweet.id),
                    "text": tweet.rawContent,
                    "username": tweet.user.username,
                    "profile_pic": tweet.user.profileImageUrl,
                    "created_at": tweet.date.isoformat()
                })
                
                # Small delay to be respectful
                time.sleep(0.1)
                
        except Exception as e:
            print(f"Error fetching tweets for {keyword}: {e}")
            
        return tweets 