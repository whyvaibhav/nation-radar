#!/usr/bin/env python3
"""
Ryan's Twitter API Fetcher
Uses Ryan's Twitter API from RapidAPI
"""

import requests
import os
from datetime import datetime, timezone, timedelta
import time

class RyanTwitterFetcher:
    def __init__(self, days_lookback=None):
        self.days_lookback = days_lookback or 1
        # Ryan's Twitter API endpoint
        self.url = "https://twitter-api47.p.rapidapi.com/v2/search"
        
    def fetch(self, keyword):
        """Fetch tweets for a keyword using Ryan's Twitter API"""
        tweets = []
        
        # Calculate the date range
        since_date = datetime.now(timezone.utc) - timedelta(days=self.days_lookback)
        since_str = since_date.strftime("%Y-%m-%d")
        
        headers = {
            "X-RapidAPI-Key": os.getenv('RAPIDAPI_KEY', 'YOUR_RAPIDAPI_KEY'),
            "X-RapidAPI-Host": "twitter-api47.p.rapidapi.com"
        }
        
        querystring = {
            "query": keyword,
            "type": "Latest",  # Required parameter
            "limit": "15"  # Optimized for 500/month API quota
        }
        
        try:
            response = requests.get(self.url, headers=headers, params=querystring)
            
            if response.status_code == 200:
                data = response.json()
                raw_tweets = data.get('tweets', [])
                
                for raw_tweet in raw_tweets:
                    try:
                        # Extract tweet data from complex structure
                        if 'content' in raw_tweet and 'itemContent' in raw_tweet['content']:
                            item_content = raw_tweet['content']['itemContent']
                            
                            if 'tweet_results' in item_content and 'result' in item_content['tweet_results']:
                                tweet_result = item_content['tweet_results']['result']
                                
                                if 'legacy' in tweet_result:
                                    legacy = tweet_result['legacy']
                                    
                                    # Extract user info
                                    username = 'unknown'
                                    profile_url = ''
                                    if 'core' in tweet_result and 'user_results' in tweet_result['core']:
                                        user_result = tweet_result['core']['user_results']['result']
                                        if 'legacy' in user_result:
                                            user_legacy = user_result['legacy']
                                            username = user_legacy.get('screen_name', 'unknown')
                                            # Create Twitter profile URL
                                            profile_url = f"https://twitter.com/{username}" if username != 'unknown' else ''
                                    
                                    # Build basic engagement from legacy if present
                                    engagement = {
                                        "likes": int(legacy.get('favorite_count', 0) or 0),
                                        "retweets": int(legacy.get('retweet_count', 0) or 0),
                                        "replies": int(legacy.get('reply_count', 0) or 0),
                                        "quote_tweets": int(legacy.get('quote_count', 0) or 0),
                                        "views": 0,
                                        "bookmarks": int(legacy.get('bookmark_count', 0) or 0),
                                    }

                                    # Some responses include views/impressions outside legacy
                                    try:
                                        if 'views' in tweet_result:
                                            views_obj = tweet_result.get('views')
                                            if isinstance(views_obj, dict) and 'count' in views_obj:
                                                engagement['views'] = int(views_obj.get('count') or 0)
                                            elif isinstance(views_obj, (int, str)):
                                                engagement['views'] = int(views_obj)
                                        # Alternate impression keys
                                        if 'impression_count' in legacy:
                                            engagement['views'] = int(legacy.get('impression_count') or engagement['views'])
                                        if 'impressions' in legacy:
                                            engagement['views'] = int(legacy.get('impressions') or engagement['views'])
                                    except Exception:
                                        pass

                                    # Create tweet object
                                    tweet = {
                                        "id": legacy.get('id_str', ''),
                                        "text": legacy.get('full_text', ''),
                                        "username": username,
                                        "profile_pic": profile_url,  # Using profile_pic field for profile URL
                                        "created_at": legacy.get('created_at', ''),
                                        "engagement": engagement
                                    }
                                    
                                    if tweet['id'] and tweet['text']:
                                        tweets.append(tweet)
                                        
                    except Exception as e:
                        print(f"Error parsing tweet: {e}")
                        continue
                        
            elif response.status_code == 429:
                print(f"Rate limited for keyword '{keyword}'; backing off 5s")
                time.sleep(5)
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"Error fetching tweets for keyword '{keyword}': {e}")
            
        return tweets 