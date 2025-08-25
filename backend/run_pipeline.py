#!/usr/bin/env python3
"""
Updated Nation Radar Pipeline
Uses the new Twitter API (twitter293.p.rapidapi.com) that we successfully tested
ENHANCED VERSION: Removed broken detail API calls, optimized rate limiting
"""

import sys
import os
import re
import time
import logging
from datetime import datetime
from fetchers.new_twitter_fetcher import NewTwitterFetcher
# CSV storage removed - using SQLite only
from storage.sqlite_storage import SQLiteStorage
import requests
from config import KEYWORDS, DAYS_LOOKBACK
from nation_agent import format_tweet_for_agent, get_agent_score
from dedup import earliest_unique_tweets, compute_text_hash, load_seen_hashes, save_seen_hashes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

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

def main():
    start_time = datetime.now()
    print("Starting Nation Radar Pipeline...")

    # Use the new Twitter fetcher
    fetcher = NewTwitterFetcher(days_lookback=DAYS_LOOKBACK)
    
    # Use SQLite as primary storage (more efficient and reliable)
    db_storage = SQLiteStorage(db_path="tweets.db")
    seen_ids = set()
    seen_hashes = load_seen_hashes()
    all_results = []
    
    # Statistics tracking
    stats = {
        'keywords_processed': 0,
        'tweets_found': 0,
        'tweets_processed': 0,
        'tweets_stored': 0,
        'api_errors': 0,
        'duplicates_skipped': 0
    }
    
    total_keywords = len(KEYWORDS)
    for i, keyword in enumerate(KEYWORDS, 1):
        print(f"Processing keyword {i}/{total_keywords}: {keyword}")
        
        try:
            tweets = fetcher.fetch(keyword)
            stats['keywords_processed'] += 1
            
            if not tweets:
                print(f"No tweets found for: {keyword}")
                continue
            
            stats['tweets_found'] += len(tweets)
            
            # Deduplicate by normalized text within this batch, keep earliest
            tweets = earliest_unique_tweets(tweets)
            
            count = 0
            for tweet in tweets:
                # Post-filter: For $NATION, only process tweets containing $NATION (not #NATION or plain 'nation')
                if keyword == "$NATION":
                    if not contains_ticker(tweet['text'], "NATION"):
                        continue  # Skip tweets that don't have $NATION exactly
                        
                if count >= 100:  # Process 100 tweets per keyword (optimized)
                    print(f"Reached limit of 100 tweets for: {keyword}")
                    break
                    
                tweet_id = tweet.get('id')
                if not tweet_id or tweet_id in seen_ids:
                    stats['duplicates_skipped'] += 1
                    continue
                    
                seen_ids.add(tweet_id)
                stats['tweets_processed'] += 1
                
                # Use engagement from search API only (removed broken detail API calls)
                existing_engagement = tweet.get('engagement') if isinstance(tweet, dict) else None
                
                if existing_engagement and engagement_has_signal(existing_engagement):
                    # Use engagement data from search API
                    tweet['engagement'] = existing_engagement
                    logger.debug(f"Using search API engagement for tweet {tweet_id}")
                else:
                    # Default engagement if none available
                    tweet['engagement'] = {"likes": 0, "retweets": 0, "replies": 0, "views": 0, "bookmarks": 0, "quote_tweets": 0}
                    logger.debug(f"No engagement data for tweet {tweet_id}, using defaults")
                
                # Skip if we've already scored near-identical content in past runs
                content_hash = compute_text_hash(tweet.get('text', ''))
                if content_hash in seen_hashes:
                    stats['duplicates_skipped'] += 1
                    continue
                    
                formatted = format_tweet_for_agent(tweet)
                logger.debug(f"\n--- Message sent to agent ---\n{formatted}\n----------------------------\n")
                
                try:
                    score = get_agent_score(formatted)
                    tweet['score'] = score
                except Exception as e:
                    logger.error(f"Error getting agent score for tweet {tweet_id}: {e}")
                    stats['api_errors'] += 1
                    tweet['score'] = 0
                
                # Store to database (enforces cross-run dedup)
                if db_storage.append_row(tweet):
                    all_results.append((tweet['username'], score, tweet['id']))
                    logger.info(f"Stored tweet {tweet['id']} by @{tweet['username']} with score {score}")
                    stats['tweets_stored'] += 1
                    count += 1
                else:
                    logger.info(f"Skipped duplicate tweet {tweet['id']} by @{tweet['username']} (already processed)")
                    stats['duplicates_skipped'] += 1
                
                # Mark this content as seen so future reposts won't be scored again
                seen_hashes.add(content_hash)
                
                # Rate limiting: Only between keywords, not between tweets
                # Removed 2-second delay here - it was causing excessive slowdown
                
        except Exception as e:
            logger.error(f"Error processing keyword '{keyword}': {e}")
            stats['api_errors'] += 1
            continue
        
        # Add delay between keywords only
        if i < total_keywords:  # Don't delay after the last keyword
            time.sleep(2)
    
    # Persist seen hashes across runs
    save_seen_hashes(seen_hashes)
    
    # Calculate execution time
    execution_time = datetime.now() - start_time
    
    print(f"\nPipeline completed in {execution_time}")
    print(f"Keywords processed: {stats['keywords_processed']}/{len(KEYWORDS)}")
    print(f"Tweets found: {stats['tweets_found']}")
    print(f"Tweets stored: {stats['tweets_stored']}")
    print(f"Duplicates skipped: {stats['duplicates_skipped']}")
    
    if all_results:
        print("\nTop 5 by score:")
        for username, score, tweet_id in sorted(all_results, key=lambda x: -x[1])[:5]:
            print(f"  @{username}: {score}")
    
    print("Pipeline execution completed successfully!")

if __name__ == "__main__":
    main()
