#!/usr/bin/env python3
"""
New Twitter API Fetcher using the working endpoint format
"""

import requests
import time
import os
from typing import List, Dict, Any

class NewTwitterFetcher:
    def __init__(self, days_lookback: int = 7):
        self.days_lookback = days_lookback
        self.api_key = os.getenv('RAPIDAPI_KEY', 'bd408a75efmsh7d13585f3a40368p186d85jsndd821cdf1fef')
        self.base_url = "https://twitter293.p.rapidapi.com"
        
    def fetch(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Fetch tweets using the working endpoint format discovered from HAR file
        """
        tweets = []
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "twitter293.p.rapidapi.com"
        }
        
        # Use the working endpoint format: /search/{keyword}
        url = f"{self.base_url}/search/{keyword}"
        
        # Use the working parameters from HAR file
        params = {
            "count": "80",  # Increased from 20 to 80
            "category": "Top"  # This was the key - using "Top" category
        }
        
        try:
            print(f"🔍 Fetching tweets for keyword: {keyword}")
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                tweets = self._extract_tweets_from_response(data)
                print(f"✅ Found {len(tweets)} tweets for '{keyword}'")
            else:
                print(f"❌ API Error {response.status_code}: {response.text[:200]}")
                
        except Exception as e:
            print(f"❌ Error fetching tweets for '{keyword}': {e}")
            
        return tweets
    
    def _extract_tweets_from_response(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract tweets from the API response
        """
        tweets = []
        
        try:
            if 'entries' in data:
                for entry in data['entries']:
                    if entry.get('type') == 'TimelineAddEntries':
                        for sub_entry in entry.get('entries', []):
                            content = sub_entry.get('content', {})
                            if content.get('entryType') == 'TimelineTimelineItem':
                                item_content = content.get('itemContent', {})
                                if item_content.get('itemType') == 'TimelineTweet':
                                    tweet_result = item_content.get('tweet_results', {}).get('result', {})
                                    if tweet_result:
                                        tweet = self._parse_tweet_result(tweet_result)
                                        if tweet:
                                            tweets.append(tweet)
        except Exception as e:
            print(f"❌ Error parsing response: {e}")
            
        return tweets
    
    def _parse_tweet_result(self, tweet_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse a single tweet result into our standard format
        """
        try:
            if 'legacy' not in tweet_result:
                return None
                
            legacy = tweet_result['legacy']
            
            # Extract user information
            username = "unknown"
            if 'core' in tweet_result and 'user_results' in tweet_result['core']:
                user_result = tweet_result['core']['user_results']['result']
                if 'legacy' in user_result:
                    username = user_result['legacy'].get('screen_name', 'unknown')
            
            # Extract engagement metrics
            engagement = {
                "likes": int(legacy.get('favorite_count', 0) or 0),
                "retweets": int(legacy.get('retweet_count', 0) or 0),
                "replies": int(legacy.get('reply_count', 0) or 0),
                "quote_tweets": int(legacy.get('quote_count', 0) or 0),
                "bookmarks": int(legacy.get('bookmark_count', 0) or 0),
                "views": 0
            }
            
            # Try to get views from the views object
            if 'views' in tweet_result:
                views_obj = tweet_result.get('views')
                if isinstance(views_obj, dict) and 'count' in views_obj:
                    engagement['views'] = int(views_obj.get('count') or 0)
                elif isinstance(views_obj, (int, str)):
                    engagement['views'] = int(views_obj)
            
            tweet = {
                "id": legacy.get('id_str', ''),
                "text": legacy.get('full_text', ''),
                "username": username,
                "created_at": legacy.get('created_at', ''),
                "engagement": engagement
            }
            
            return tweet
            
        except Exception as e:
            print(f"❌ Error parsing tweet: {e}")
            return None
