import sys
import os
import re
import time
from fetchers.ryan_twitter_fetcher import RyanTwitterFetcher
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


def fetch_tweet_engagement(tweet_id):
    """Fetch engagement metrics for a tweet using RapidAPI.
    Try multiple compatible Ryan API hosts/endpoints to reduce 404s.
    Returns dict on success, or None if not available.
    """
    
    RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
    if not RAPIDAPI_KEY:
        print("Warning: RAPIDAPI_KEY not found, using default engagement metrics")
        return {"likes": 0, "retweets": 0, "replies": 0, "views": 0, "bookmarks": 0, "quote_tweets": 0}
    
    # Allow overriding host/path via env if needed
    override_host = os.getenv("RAPIDAPI_ENGAGEMENT_HOST", "").strip()
    override_url = os.getenv("RAPIDAPI_ENGAGEMENT_URL", "").strip()

    candidates = []
    if override_host and override_url:
        candidates.append({"url": override_url, "host": override_host, "params": {"id": tweet_id}})

    # Common Ryan API variants
    candidates.extend([
        # Ryan v2 details (as in your screenshot)
        {"url": "https://twitter-api47.p.rapidapi.com/v2/tweet/details", "host": "twitter-api47.p.rapidapi.com", "params": {"id": tweet_id}},
        {"url": "https://twitter-api47.p.rapidapi.com/v2/tweet/details", "host": "twitter-api47.p.rapidapi.com", "params": {"tweet_id": tweet_id}},
        # Ryan v2 basic
        {"url": "https://twitter-api47.p.rapidapi.com/v2/tweet", "host": "twitter-api47.p.rapidapi.com", "params": {"id": tweet_id}},
        # Ryan php variant
        {"url": "https://twitter-api45.p.rapidapi.com/tweet.php", "host": "twitter-api45.p.rapidapi.com", "params": {"id": tweet_id}},
        {"url": "https://twitter-api-45.p.rapidapi.com/tweet.php", "host": "twitter-api-45.p.rapidapi.com", "params": {"id": tweet_id}},
        # Other RapidAPI product sometimes used
        {"url": "https://twitter154.p.rapidapi.com/tweet/details", "host": "twitter154.p.rapidapi.com", "params": {"tweet_id": tweet_id}},
    ])
    
    try:
        # Add delay to prevent rate limiting
        time.sleep(1)
        
        data = None
        last_status = None
        for candidate in candidates:
            headers = {
                "X-RapidAPI-Key": RAPIDAPI_KEY,
                "X-RapidAPI-Host": candidate["host"],
            }
            response = requests.get(candidate["url"], headers=headers, params=candidate["params"], timeout=30)
            last_status = response.status_code
            if response.status_code == 200:
                try:
                    data = response.json()
                except Exception:
                    data = None
                if data:
                    break
            elif response.status_code == 429:
                print("Rate limited on engagement detail endpoint; backing off 2s and retrying next candidate")
                time.sleep(2)
                continue

        if data is not None:
            
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
                engagement['likes'] = int(data.get('like_count', data.get('likes', 0)))
                engagement['retweets'] = int(data.get('retweet_count', data.get('retweets', 0)))
                engagement['replies'] = int(data.get('reply_count', data.get('replies', 0)))
                # Views / impressions can be present under different keys
                views_candidates = [
                    data.get('view_count'),
                    data.get('views'),
                    (data.get('views') or {}).get('count') if isinstance(data.get('views'), dict) else None,
                    data.get('impression_count'),
                    data.get('impressions'),
                ]
                for vc in views_candidates:
                    if vc is not None:
                        try:
                            engagement['views'] = int(vc)
                            break
                        except Exception:
                            pass
                engagement['bookmarks'] = int(data.get('bookmark_count', data.get('bookmarks', 0)))
                engagement['quote_tweets'] = int(data.get('quote_count', data.get('quote_tweets', 0)))
                
                # Check public_metrics structure
                if 'public_metrics' in data:
                    metrics = data['public_metrics']
                    engagement['likes'] = int(metrics.get('like_count', engagement['likes']))
                    engagement['retweets'] = int(metrics.get('retweet_count', engagement['retweets']))
                    engagement['replies'] = int(metrics.get('reply_count', engagement['replies']))
                    engagement['quote_tweets'] = int(metrics.get('quote_count', engagement['quote_tweets']))
            except Exception as e:
                print(f"Error parsing engagement data: {e}")
                pass
            
            return engagement if engagement_has_signal(engagement) else None
            
        else:
            status = last_status if last_status is not None else "unknown"
            print(f"Warning: Could not fetch engagement for tweet {tweet_id}, status {status}")
            return None
            
    except Exception as e:
        print(f"Error fetching engagement for tweet {tweet_id}: {e}")
        return {"likes": 0, "retweets": 0, "replies": 0, "views": 0, "bookmarks": 0, "quote_tweets": 0}

def main():
    print(f"Loading config: keywords={KEYWORDS}, days_lookback={DAYS_LOOKBACK}, csv={CSV_FILENAME}")
    print("🚀 Starting Nation Radar Pipeline - Weekly Collection Mode")
    print("📊 API Quota: 500 requests/month | Collection: 6 keywords × 5 tweets = 30 tweets per run")
    print("⏰ Frequency: Weekly (every 7 days) | Monthly API usage: ~360 requests")
    
    fetcher = RyanTwitterFetcher(days_lookback=DAYS_LOOKBACK)
    # Use SQLite for scalable dedup; still write CSV for human-readable export
    db_storage = SQLiteStorage(db_path="tweets.db")
    csv_storage = CSVStorage(filename=CSV_FILENAME)
    seen_ids = set()
    seen_hashes = load_seen_hashes()
    all_results = []
    
    for keyword in KEYWORDS:
        print(f"Fetching tweets for keyword: {keyword}")
        tweets = fetcher.fetch(keyword)
        # Deduplicate by normalized text within this batch, keep earliest
        tweets = earliest_unique_tweets(tweets)
        count = 0
        for tweet in tweets:
            # Post-filter: For $NATION, only process tweets containing $NATION (not #NATION or plain 'nation')
            if keyword == "$NATION":
                if not contains_ticker(tweet['text'], "NATION"):
                    continue  # Skip tweets that don't have $NATION exactly
            if count >= 5:  # Process 5 tweets per keyword (optimized for weekly collection)
                break
            tweet_id = tweet.get('id')
            if not tweet_id or tweet_id in seen_ids:
                continue
            seen_ids.add(tweet_id)
            # Use engagement from search if present; otherwise try detail API
            existing_engagement = tweet.get('engagement') if isinstance(tweet, dict) else None
            detail_engagement = fetch_tweet_engagement(tweet_id)
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
            print("\n--- Message sent to agent ---\n" + formatted + "\n----------------------------\n")
            score = get_agent_score(formatted)
            tweet['score'] = score
            # Store to DB first (enforces cross-run dedup), then append to CSV if accepted
            if db_storage.append_row(tweet):
                csv_storage.append_row(tweet)
            all_results.append((tweet['username'], score, tweet['id']))
            print(f"Stored tweet {tweet['id']} by @{tweet['username']} with score {score}")
            count += 1
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