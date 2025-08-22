#!/usr/bin/env python3
"""
Updated Nation Radar Pipeline
Uses the new Twitter API (twitter293.p.rapidapi.com) that we successfully tested
"""

import sys
import os
import re
import time
from fetchers.new_twitter_fetcher import NewTwitterFetcher
from storage.csv_storage import CSVStorage
from storage.sqlite_storage import SQLiteStorage
import requests
from config import KEYWORDS, DAYS_LOOKBACK, CSV_FILENAME
from nation_agent import format_tweet_for_agent, get_agent_score
from dedup import earliest_unique_tweets, compute_text_hash, load_seen_hashes, save_seen_hashes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Helper: Check if text contains ticker (e.g., $NATION) ---
def contains_ticker(text, ticker):
    """Only match ticker as $TICKER, not as part of another word"""
    pattern = re.compile(rf'\${ticker}\b', re.IGNORECASE)
    return bool(pattern.search(text))

# --- Engagement helpers ---
def engagement_has_signal(engagement: dict) -> bool:
    """Return True if any engagement metric is > 0."""
    if not isinstance(engagement, dict):
        return False
    fields = ["likes", "retweets", "replies", "views", "bookmarks", "quote_tweets"]
    try:
        return any(int(engagement.get(f, 0) or 0) > 0 for f in fields)
    except Exception:
        return False

def fetch_tweet_engagement_new_api(tweet_id):
    """Fetch engagement metrics for a tweet using the new Twitter API.
    Returns dict on success, or None if not available.
    """
    
    RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', 'bd408a75efmsh7d13585f3a40368p186d85jsndd821cdf1fef')
    
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "twitter293.p.rapidapi.com"
    }
    
    # Try different endpoints for tweet details
    endpoints = [
        f"https://twitter293.p.rapidapi.com/tweet/{tweet_id}",
        f"https://twitter293.p.rapidapi.com/tweets/{tweet_id}",
        f"https://twitter293.p.rapidapi.com/tweet/details/{tweet_id}"
    ]
    
    try:
        # Add delay to prevent rate limiting
        time.sleep(1)
        
        for endpoint in endpoints:
            try:
                response = requests.get(endpoint, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Parse engagement metrics from response
                    engagement = {
                        "likes": 0,
                        "retweets": 0, 
                        "replies": 0,
                        "views": 0,
                        "bookmarks": 0,
                        "quote_tweets": 0
                    }
                    
                    # Try to extract from various response structures
                    try:
                        # Handle the threaded conversation format
                        if 'data' in data and 'threaded_conversation_with_injections_v2' in data['data']:
                            instructions = data['data']['threaded_conversation_with_injections_v2'].get('instructions', [])
                            
                            for instruction in instructions:
                                if instruction.get('type') == 'TimelineAddEntries':
                                    entries = instruction.get('entries', [])
                                    
                                    for entry in entries:
                                        content = entry.get('content', {})
                                        if content.get('entryType') == 'TimelineTimelineItem':
                                            item_content = content.get('itemContent', {})
                                            if item_content.get('itemType') == 'TimelineTweet':
                                                tweet_result = item_content.get('tweet_results', {}).get('result', {})
                                                
                                                if tweet_result and 'legacy' in tweet_result:
                                                    legacy = tweet_result['legacy']
                                                    engagement['likes'] = int(legacy.get('favorite_count', 0) or 0)
                                                    engagement['retweets'] = int(legacy.get('retweet_count', 0) or 0)
                                                    engagement['replies'] = int(legacy.get('reply_count', 0) or 0)
                                                    engagement['quote_tweets'] = int(legacy.get('quote_count', 0) or 0)
                                                    engagement['bookmarks'] = int(legacy.get('bookmark_count', 0) or 0)
                                                    
                                                    # Try to get views
                                                    if 'views' in tweet_result:
                                                        views_obj = tweet_result.get('views')
                                                        if isinstance(views_obj, dict) and 'count' in views_obj:
                                                            engagement['views'] = int(views_obj.get('count') or 0)
                                                        elif isinstance(views_obj, (int, str)):
                                                            engagement['views'] = int(views_obj)
                                                    
                                                    break  # Found the tweet, break out
                        
                        # Handle simple tweet format
                        elif 'legacy' in data:
                            legacy = data['legacy']
                            engagement['likes'] = int(legacy.get('favorite_count', 0) or 0)
                            engagement['retweets'] = int(legacy.get('retweet_count', 0) or 0)
                            engagement['replies'] = int(legacy.get('reply_count', 0) or 0)
                            engagement['quote_tweets'] = int(legacy.get('quote_count', 0) or 0)
                            engagement['bookmarks'] = int(legacy.get('bookmark_count', 0) or 0)
                            
                            # Try to get views
                            if 'views' in data:
                                views_obj = data.get('views')
                                if isinstance(views_obj, dict) and 'count' in views_obj:
                                    engagement['views'] = int(views_obj.get('count') or 0)
                                elif isinstance(views_obj, (int, str)):
                                    engagement['views'] = int(views_obj)
                        
                        # Handle public_metrics structure
                        elif 'public_metrics' in data:
                            metrics = data['public_metrics']
                            engagement['likes'] = int(metrics.get('like_count', 0) or 0)
                            engagement['retweets'] = int(metrics.get('retweet_count', 0) or 0)
                            engagement['replies'] = int(metrics.get('reply_count', 0) or 0)
                            engagement['quote_tweets'] = int(metrics.get('quote_count', 0) or 0)
                            engagement['bookmarks'] = int(metrics.get('bookmark_count', 0) or 0)
                            engagement['views'] = int(metrics.get('impression_count', 0) or 0)
                        
                    except Exception as e:
                        print(f"Error parsing engagement data: {e}")
                        pass
                    
                    return engagement if engagement_has_signal(engagement) else None
                    
                elif response.status_code == 429:
                    print(f"Rate limited on engagement endpoint; waiting 30 seconds...")
                    time.sleep(30)
                    continue
                else:
                    print(f"Status {response.status_code} for endpoint {endpoint}")
                    continue
                    
            except Exception as e:
                print(f"Error with endpoint {endpoint}: {e}")
                continue
        
        print(f"Warning: Could not fetch engagement for tweet {tweet_id}")
        return None
        
    except Exception as e:
        print(f"Error fetching engagement for tweet {tweet_id}: {e}")
        return {"likes": 0, "retweets": 0, "replies": 0, "views": 0, "bookmarks": 0, "quote_tweets": 0}

def main():
    print(f"Loading config: keywords={KEYWORDS}, days_lookback={DAYS_LOOKBACK}, csv={CSV_FILENAME}")
    print("🚀 Starting Nation Radar Pipeline - NEW API VERSION")
    print("📊 Using: twitter293.p.rapidapi.com (the API that worked for @web3spectre)")
    print("📊 API Quota: 20,000 requests/month | Collection: 6 keywords × 5 tweets = 30 tweets per run")
    print("⏰ Frequency: Weekly (every 7 days) | Monthly API usage: ~360 requests")
    
    # Use the new Twitter fetcher
    fetcher = NewTwitterFetcher(days_lookback=DAYS_LOOKBACK)
    
    # Use SQLite as primary storage (more efficient and reliable)
    db_storage = SQLiteStorage(db_path="tweets.db")
    seen_ids = set()
    seen_hashes = load_seen_hashes()
    all_results = []
    
    for keyword in KEYWORDS:
        print(f"\n🔍 Fetching tweets for keyword: {keyword}")
        tweets = fetcher.fetch(keyword)
        
        if not tweets:
            print(f"❌ No tweets found for keyword: {keyword}")
            continue
        
        # Deduplicate by normalized text within this batch, keep earliest
        tweets = earliest_unique_tweets(tweets)
        count = 0
        
        for tweet in tweets:
            # Post-filter: For $NATION, only process tweets containing $NATION (not #NATION or plain 'nation')
            if keyword == "$NATION":
                if not contains_ticker(tweet['text'], "NATION"):
                    continue  # Skip tweets that don't have $NATION exactly
                    
            if count >= 80:  # Process 80 tweets per keyword (increased from 5)
                break
                
            tweet_id = tweet.get('id')
            if not tweet_id or tweet_id in seen_ids:
                continue
                
            seen_ids.add(tweet_id)
            
            # Use engagement from search if present; otherwise try detail API
            existing_engagement = tweet.get('engagement') if isinstance(tweet, dict) else None
            detail_engagement = fetch_tweet_engagement_new_api(tweet_id)
            
            if detail_engagement is not None:
                tweet['engagement'] = detail_engagement
            elif existing_engagement:
                tweet['engagement'] = existing_engagement
            else:
                tweet['engagement'] = {"likes": 0, "retweets": 0, "replies": 0, "views": 0, "bookmarks": 0, "quote_tweets": 0}
            
            # Skip if we've already scored near-identical content in past runs
            content_hash = compute_text_hash(tweet.get('text', ''))
            if content_hash in seen_hashes:
                continue
                
            formatted = format_tweet_for_agent(tweet)
            print(f"\n--- Message sent to agent ---\n{formatted}\n----------------------------\n")
            
            score = get_agent_score(formatted)
            tweet['score'] = score
            
            # Store to database (enforces cross-run dedup)
            if db_storage.append_row(tweet):
                all_results.append((tweet['username'], score, tweet['id']))
                print(f"✅ Stored tweet {tweet['id']} by @{tweet['username']} with score {score}")
                count += 1
            else:
                print(f"⏭️  Skipped duplicate tweet {tweet['id']} by @{tweet['username']} (already processed)")
            
            # Mark this content as seen so future reposts won't be scored again
            seen_hashes.add(content_hash)
    
    # Persist seen hashes across runs
    save_seen_hashes(seen_hashes)
    
    print(f"\n🎯 Pipeline complete. {len(all_results)} unique tweets processed.")
    print(f"📈 Collection Summary:")
    print(f"   • Keywords processed: {len(KEYWORDS)}")
    print(f"   • Tweets collected: {len(all_results)}")
    print(f"   • API usage: ~{len(KEYWORDS) * 15} requests")
    print(f"   • Next run: Weekly (every 7 days)")
    
    if all_results:
        print("\n🏆 Top 5 by score:")
        for username, score, tweet_id in sorted(all_results, key=lambda x: -x[1])[:5]:
            print(f"   @{username}: {score} (ID: {tweet_id})")

if __name__ == "__main__":
    main()
