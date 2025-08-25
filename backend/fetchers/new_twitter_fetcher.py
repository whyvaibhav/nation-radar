#!/usr/bin/env python3
"""
Efficient Twitter API Fetcher - Quality over Quantity
Focused on relevant, high-quality content with minimal spam
"""

import requests
import time
import os
from typing import List, Dict, Any
from datetime import datetime, timedelta

class NewTwitterFetcher:
    def __init__(self, days_lookback: int = 21):
        self.days_lookback = days_lookback
        self.api_key = os.getenv('RAPIDAPI_KEY', 'bd408a75efmsh7d13585f3a40368p186d85jsndd821cdf1fef')
        self.base_url = "https://twitter293.p.rapidapi.com"
        
    def fetch(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Fetch tweets using focused, quality-oriented collection
        """
        all_tweets = []
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "twitter293.p.rapidapi.com"
        }
        
        # Strategy 1: Focused categories only
        categories = ["Top", "Latest"]  # Removed "Mixed" to reduce noise
        
        for category in categories:
            print(f"🔍 Fetching {category} tweets for keyword: {keyword}")
            category_tweets = self._fetch_category_with_pagination(keyword, category, headers)
            all_tweets.extend(category_tweets)
            print(f"✅ Found {len(category_tweets)} {category} tweets for '{keyword}'")
            
            # Rate limiting between categories
            time.sleep(2)
        
        # Strategy 2: Limited, focused variations only
        search_variations = self._generate_focused_variations(keyword)
        
        for variation in search_variations:
            print(f"🔍 Fetching tweets for variation: {variation}")
            variation_tweets = self._fetch_category_with_pagination(variation, "Latest", headers)
            all_tweets.extend(variation_tweets)
            print(f"✅ Found {len(variation_tweets)} tweets for variation '{variation}'")
            time.sleep(2)
        
        # Remove duplicates based on tweet ID
        unique_tweets = {}
        for tweet in all_tweets:
            if tweet['id'] not in unique_tweets:
                unique_tweets[tweet['id']] = tweet
        
        tweets = list(unique_tweets.values())
        
        # Filter tweets by date (within lookback period)
        filtered_tweets = self._filter_tweets_by_date(tweets)
        
        # Additional quality filtering
        quality_tweets = self._filter_quality_content(filtered_tweets, keyword)
        
        print(f"🎯 Total unique tweets for '{keyword}': {len(tweets)}")
        print(f"📅 Tweets within {self.days_lookback} days: {len(filtered_tweets)}")
        print(f"✨ Quality tweets: {len(quality_tweets)}")
        
        return quality_tweets
    
    def _generate_focused_variations(self, keyword: str) -> List[str]:
        """
        Generate focused search variations to reduce noise
        """
        variations = []
        
        # Only use exact phrase matching for better quality
        if ' ' in keyword:
            # For multi-word keywords like "Crestal Network"
            variations.append(f'"{keyword}"')  # Exact phrase only
        else:
            # For single words like "Crestal"
            variations.append(f'"{keyword}"')  # Exact phrase only
        
        return variations
    
    def _filter_quality_content(self, tweets: List[Dict[str, Any]], keyword: str) -> List[Dict[str, Any]]:
        """
        Filter out low-quality, generic content
        """
        quality_tweets = []
        
        for tweet in tweets:
            text = tweet.get('text', '').lower()
            
            # Skip if tweet is too short (likely spam)
            if len(text) < 20:
                continue
            
            # Skip if tweet contains common spam indicators
            spam_indicators = [
                'follow me', 'retweet', 'like', 'dm me', 'send me',
                'airdrop', 'free', 'claim', 'moon', 'pump', '100x',
                '🚀', '💎', '🔥', '📈', '💰'
            ]
            
            if any(indicator in text for indicator in spam_indicators):
                continue
            
            # Skip if tweet is mostly hashtags
            hashtag_count = text.count('#')
            if hashtag_count > 5:
                continue
            
            # Skip if tweet is mostly mentions
            mention_count = text.count('@')
            if mention_count > 3:
                continue
            
            # Ensure keyword relevance
            keyword_lower = keyword.lower().replace('$', '').replace('"', '')
            if keyword_lower not in text and keyword_lower.replace(' ', '') not in text:
                continue
            
            quality_tweets.append(tweet)
        
        return quality_tweets
    
    def _fetch_category_with_pagination(self, keyword: str, category: str, headers: Dict) -> List[Dict[str, Any]]:
        """
        Fetch tweets for a specific category with limited pagination
        """
        tweets = []
        max_requests = 3  # Reduced to 3 requests per category for efficiency
        cursor = None
        
        for request_num in range(max_requests):
            try:
                url = f"{self.base_url}/search/{keyword}"
                params = {
                    "count": "50",  # Reduced to 50 tweets per request
                    "category": category
                }
                
                # Add cursor for pagination if available
                if cursor:
                    params["cursor"] = cursor
                
                print(f"  📄 Request {request_num + 1}/{max_requests} for {category}")
                response = requests.get(url, headers=headers, params=params, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    batch_tweets = self._extract_tweets_from_response(data)
                    
                    if not batch_tweets:
                        print(f"  ⚠️  No more tweets found for {category}")
                        break
                    
                    tweets.extend(batch_tweets)
                    print(f"  ✅ Got {len(batch_tweets)} tweets (total: {len(tweets)})")
                    
                    # Check for cursor for next page
                    cursor = self._extract_cursor(data)
                    if not cursor:
                        print(f"  📄 No more pages for {category}")
                        break
                        
                elif response.status_code == 429:
                    print(f"  ⏳ Rate limited, waiting 30 seconds...")
                    time.sleep(30)
                    continue
                elif response.status_code == 404:
                    print(f"  ❌ Search not found for '{keyword}' in {category}")
                    break
                else:
                    print(f"  ❌ API Error {response.status_code} for {category}")
                    break
                    
            except Exception as e:
                print(f"  ❌ Error in request {request_num + 1}: {e}")
                break
            
            # Rate limiting between requests
            time.sleep(2)
        
        return tweets
    
    def _extract_cursor(self, data: Dict[str, Any]) -> str:
        """
        Extract cursor for pagination from API response
        """
        try:
            if 'entries' in data:
                for entry in data['entries']:
                    if entry.get('type') == 'TimelineAddCursor':
                        content = entry.get('content', {})
                        if content.get('cursorType') == 'Bottom':
                            return content.get('value', '')
        except Exception as e:
            print(f"❌ Error extracting cursor: {e}")
        return None
    
    def _filter_tweets_by_date(self, tweets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter tweets to only include those within the lookback period
        """
        cutoff_date = datetime.now() - timedelta(days=self.days_lookback)
        filtered_tweets = []
        
        for tweet in tweets:
            try:
                # Parse tweet date
                tweet_date_str = tweet.get('created_at', '')
                if tweet_date_str:
                    # Handle Twitter format: "Thu Aug 21 20:08:17 +0000 2025"
                    try:
                        tweet_date = datetime.strptime(tweet_date_str, '%a %b %d %H:%M:%S %z %Y')
                    except ValueError:
                        # Try ISO format if Twitter format fails
                        try:
                            tweet_date = datetime.fromisoformat(tweet_date_str.replace('Z', '+00:00'))
                        except ValueError:
                            print(f"❌ Cannot parse date: {tweet_date_str}")
                            # Include tweet if we can't parse the date
                            filtered_tweets.append(tweet)
                            continue
                    
                    # Convert to naive datetime for comparison
                    if tweet_date.tzinfo:
                        tweet_date = tweet_date.replace(tzinfo=None)
                    
                    if tweet_date >= cutoff_date:
                        filtered_tweets.append(tweet)
                        
            except Exception as e:
                print(f"❌ Error parsing tweet date: {e}")
                # Include tweet if we can't parse the date
                filtered_tweets.append(tweet)
        
        return filtered_tweets
    
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
