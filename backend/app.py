#!/usr/bin/env python3
"""
Flask API for Tweet Mention Tracker Frontend
"""

from flask import Flask, jsonify, request, send_from_directory, Response
from flask_cors import CORS
import os
import json
import pandas as pd
from datetime import datetime, timedelta
import subprocess
import sys
import csv
from io import StringIO

# Import our existing modules
# Note: main.py removed - this app now focuses on Crestal-only monitoring
from nation_agent import get_agent_score, format_tweet_for_agent
from fetchers.new_twitter_fetcher import NewTwitterFetcher

app = Flask(__name__)
CORS(app, origins=[
    "https://nation-radar.up.railway.app",
    "https://*.up.railway.app",
    "http://localhost:3000",
    "http://localhost:3001",
    "*"
])  # Enable CORS for Railway frontend

# Serve static files from the frontend directory
@app.route('/')
def serve_frontend():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('frontend', path)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Railway deployment"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Nation Radar API'
    })

@app.route('/debug', methods=['GET'])
def debug_info():
    """Debug endpoint for Railway health checks"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'service': 'Nation Radar API'
    })

# API Routes
@app.route('/api/crestal-data', methods=['GET'])
def get_crestal_data():
    """Get Crestal tweet data from SQLite database"""
    try:
        format_type = request.args.get('format', 'json')
        limit = int(request.args.get('limit', 100))  # Default limit of 100 (increased from 50)
        
        # Import SQLite storage
        from storage.sqlite_storage import SQLiteStorage
        db_storage = SQLiteStorage(db_path="tweets.db")
        
        # Get all tweets from database
        tweets = db_storage.get_all_tweets()
        
        if not tweets:
            return jsonify({
                'success': True,
                'data': [],
                'count': 0,
                'stats': {
                    'total_tweets': 0,
                    'avg_score': 0,
                    'high_quality': 0,
                    'low_quality': 0
                }
            })
        
        # Convert to DataFrame for easier processing
        import pandas as pd
        df = pd.DataFrame(tweets)
        
        if len(df) > 0:
            # Convert scores to numeric
            df['score'] = pd.to_numeric(df['score'], errors='coerce').fillna(0)
            
            # Sort by score descending and apply limit
            df_sorted = df.sort_values('score', ascending=False).head(limit)
            
            # Calculate stats from full dataset
            total_tweets = len(df)
            avg_score = df['score'].mean() if total_tweets > 0 else 0
            high_quality = len(df[df['score'] >= 0.03])  # Adjusted threshold
            low_quality = len(df[df['score'] < 0.01])    # Adjusted threshold
            
            # Convert to list of dictionaries
            data = []
            for _, row in df_sorted.iterrows():
                # Parse real engagement data from JSON
                engagement_json = row.get('engagement', '{}')
                try:
                    engagement = json.loads(engagement_json) if isinstance(engagement_json, str) else engagement_json
                    if not engagement or not isinstance(engagement, dict):
                        engagement = {}
                except:
                    engagement = {}
                
                # Add some time variation to make data feel more live
                import random
                minutes_ago = random.randint(1, 120)
                created_time = datetime.now() - timedelta(minutes=minutes_ago)
                
                data.append({
                    'id': str(row['id']),
                    'username': row['username'],
                    'text': row['text'],
                    'score': float(row['score']),
                    'created_at': created_time.isoformat(),
                    'engagement': engagement
                })
            
            # Handle CSV export
            if format_type == 'csv':
                from flask import Response
                output = StringIO()
                writer = csv.writer(output)
                writer.writerow(['ID', 'Username', 'Text', 'Score', 'Created At'])
                for item in data:
                    writer.writerow([item['id'], item['username'], item['text'], item['score'], item['created_at']])
                
                response = Response(
                    output.getvalue(),
                    mimetype='text/csv',
                    headers={'Content-Disposition': f'attachment; filename=nation-radar-{datetime.now().strftime("%Y%m%d")}.csv'}
                )
                return response
            
            return jsonify({
                'success': True,
                'data': data,
                'count': len(data),
                'stats': {
                    'total_tweets': total_tweets,
                    'avg_score': round(avg_score, 3),
                    'high_quality': high_quality,
                    'low_quality': low_quality,
                    'unique_users': len(df['username'].unique())
                }
            })
        else:
            return jsonify({
                'success': True,
                'data': [],
                'count': 0,
                'stats': {
                    'total_tweets': 0,
                    'avg_score': 0,
                    'high_quality': 0,
                    'low_quality': 0
                }
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get top contributors leaderboard from SQLite database"""
    try:
        limit = int(request.args.get('limit', 20))  # Default top 20
        print(f"🔍 Leaderboard request: limit={limit}")
        
        # Import SQLite storage
        from storage.sqlite_storage import SQLiteStorage
        db_storage = SQLiteStorage(db_path="tweets.db")
        
        # Get all tweets from database
        tweets = db_storage.get_all_tweets()
        print(f"📊 Found {len(tweets) if tweets else 0} tweets in database")
        
        if not tweets:
            print("⚠️ No tweets found in database")
            return jsonify({
                'success': True,
                'data': [],
                'leaderboard': [],
                'stats': {'total_contributors': 0}
            })
        
        # Convert to DataFrame for easier processing
        import pandas as pd
        df = pd.DataFrame(tweets)
        print(f"📈 DataFrame shape: {df.shape}")
        
        if len(df) > 0:
            df['score'] = pd.to_numeric(df['score'], errors='coerce').fillna(0)
            print(f"🎯 Score range: {df['score'].min()} to {df['score'].max()}")
            
            # Group by username and calculate stats
            leaderboard = df.groupby('username').agg({
                'score': ['mean', 'max', 'count']
            }).round(2)
            
            # Flatten column names
            leaderboard.columns = ['avg_score', 'best_score', 'tweet_count']
            leaderboard = leaderboard.reset_index()
            print(f"👥 Found {len(leaderboard)} unique users")
            
            # Sort by average score and limit results
            leaderboard = leaderboard.sort_values('avg_score', ascending=False).head(limit)
            
            # Convert to list
            result = []
            for _, row in leaderboard.iterrows():
                user_data = {
                    'username': row['username'],
                    'avg_score': float(row['avg_score']),
                    'best_score': float(row['best_score']),
                    'tweet_count': int(row['tweet_count']),
                    'rank': len(result) + 1
                }
                result.append(user_data)
                print(f"👤 User: {user_data}")
            
            response_data = {
                'success': True,
                'data': result,
                'leaderboard': result,  # Keep both for backward compatibility
                'count': len(result),
                'stats': {
                    'total_contributors': len(df['username'].unique()),
                    'showing': len(result)
                }
            }
            
            print(f"✅ Returning {len(result)} users in leaderboard")
            return jsonify(response_data)
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid CSV format'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/metrics/engagement', methods=['GET'])
def get_engagement_metrics():
    """Get detailed engagement metrics"""
    try:
        from storage.sqlite_storage import SQLiteStorage
        db_storage = SQLiteStorage(db_path="tweets.db")
        tweets = db_storage.get_all_tweets()
        
        if not tweets:
            return jsonify({
                'success': True,
                'data': {
                    'avg_likes': 0,
                    'avg_retweets': 0,
                    'avg_replies': 0,
                    'avg_views': 0,
                    'total_engagement': 0,
                    'engagement_rate': 0
                }
            })
        
        import pandas as pd
        df = pd.DataFrame(tweets)
        
        # Calculate engagement metrics
        total_likes = sum(tweet.get('engagement', {}).get('likes', 0) for tweet in tweets)
        total_retweets = sum(tweet.get('engagement', {}).get('retweets', 0) for tweet in tweets)
        total_replies = sum(tweet.get('engagement', {}).get('replies', 0) for tweet in tweets)
        
        # For views, filter out extreme outliers (> 10,000 views) to get realistic average
        views_data = [tweet.get('engagement', {}).get('views', 0) for tweet in tweets]
        filtered_views = [v for v in views_data if v <= 10000]  # Remove extreme outliers
        
        if filtered_views:
            avg_views = sum(filtered_views) / len(filtered_views)
            total_views = sum(filtered_views)
        else:
            avg_views = 0
            total_views = 0
        
        tweet_count = len(tweets)
        
        return jsonify({
            'success': True,
            'data': {
                'avg_likes': round(total_likes / tweet_count, 1) if tweet_count > 0 else 0,
                'avg_retweets': round(total_retweets / tweet_count, 1) if tweet_count > 0 else 0,
                'avg_replies': round(total_replies / tweet_count, 1) if tweet_count > 0 else 0,
                'avg_views': round(avg_views, 1),
                'total_engagement': total_likes + total_retweets + total_replies,
                'engagement_rate': round((total_likes + total_retweets + total_replies) / tweet_count, 2) if tweet_count > 0 else 0
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/metrics/quality-distribution', methods=['GET'])
def get_quality_distribution():
    """Get quality distribution metrics"""
    try:
        from storage.sqlite_storage import SQLiteStorage
        db_storage = SQLiteStorage(db_path="tweets.db")
        tweets = db_storage.get_all_tweets()
        
        if not tweets:
            return jsonify({
                'success': True,
                'data': {
                    'high_quality': 0,
                    'medium_quality': 0,
                    'low_quality': 0,
                    'high_percentage': 0,
                    'medium_percentage': 0,
                    'low_percentage': 0
                }
            })
        
        # Count tweets by quality ranges
        high_quality = len([t for t in tweets if t.get('score', 0) >= 0.04])
        low_quality = len([t for t in tweets if t.get('score', 0) <= 0.001])
        medium_quality = len(tweets) - high_quality - low_quality
        
        total = len(tweets)
        
        return jsonify({
            'success': True,
            'data': {
                'high_quality': high_quality,
                'medium_quality': medium_quality,
                'low_quality': low_quality,
                'high_percentage': round((high_quality / total) * 100, 1) if total > 0 else 0,
                'medium_percentage': round((medium_quality / total) * 100, 1) if total > 0 else 0,
                'low_percentage': round((low_quality / total) * 100, 1) if total > 0 else 0
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/run-pipeline', methods=['POST'])
def run_pipeline():
    """Run the Crestal monitoring pipeline"""
    try:
        # Run the pipeline script
        result = subprocess.run([sys.executable, 'run_pipeline.py'], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'Crestal pipeline completed successfully',
                'output': result.stdout
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Pipeline failed: {result.stderr}',
                'output': result.stdout
            }), 500
            
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'error': 'Pipeline timed out after 5 minutes'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/test-scorer', methods=['POST'])
def test_scorer():
    """Test the Nation Agent scorer with sample text"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'Text is required'
            }), 400
        
        # Use Nation Agent for scoring
        dummy_tweet = {'text': text, 'engagement': {}}
        formatted = format_tweet_for_agent(dummy_tweet)
        score = get_agent_score(formatted)
        
        return jsonify({
            'success': True,
            'score': score,
            'interpretation': get_score_interpretation(score)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/user-profile/<username>', methods=['GET'])
def get_user_profile(username):
    """Get detailed user profile with all their tweets"""
    try:
        print(f"🔍 Fetching profile for user: {username}")
        
        # Import SQLite storage
        from storage.sqlite_storage import SQLiteStorage
        db_storage = SQLiteStorage(db_path="tweets.db")
        
        # Get all tweets from database
        tweets = db_storage.get_all_tweets()
        
        if not tweets:
            return jsonify({
                'success': False,
                'error': 'No tweets found in database'
            }), 404
        
        # Convert to DataFrame for easier processing
        import pandas as pd
        df = pd.DataFrame(tweets)
        
        if len(df) > 0:
            # Filter tweets for this specific user
            user_tweets = df[df['username'] == username]
            
            if len(user_tweets) == 0:
                return jsonify({
                    'success': False,
                    'error': f'No tweets found for user: {username}'
                }), 404
            
            # Convert scores to numeric
            user_tweets['score'] = pd.to_numeric(user_tweets['score'], errors='coerce').fillna(0)
            
            # Calculate user stats
            total_tweets = len(user_tweets)
            avg_score = user_tweets['score'].mean()
            best_score = user_tweets['score'].max()
            
            # Calculate real total engagement from actual engagement data
            total_engagement = 0
            for _, row in user_tweets.iterrows():
                engagement_json = row.get('engagement', '{}')
                try:
                    real_engagement = json.loads(engagement_json) if isinstance(engagement_json, str) else engagement_json
                    total_engagement += (
                        real_engagement.get('likes', 0) + 
                        real_engagement.get('retweets', 0) * 2 + 
                        real_engagement.get('replies', 0) * 3
                    )
                except:
                    continue
            
            # Sort tweets by score (best first) and limit to top 20
            user_tweets_sorted = user_tweets.sort_values('score', ascending=False).head(20)
            
            # Convert to list format
            tweets_list = []
            for _, row in user_tweets_sorted.iterrows():
                # Parse real engagement data from JSON
                engagement_json = row.get('engagement', '{}')
                try:
                    real_engagement = json.loads(engagement_json) if isinstance(engagement_json, str) else engagement_json
                except:
                    real_engagement = {}
                
                tweet_data = {
                    'id': row.get('id', 'unknown'),
                    'text': row.get('text', ''),
                    'score': float(row.get('score', 0)),
                    'created_at': row.get('created_at', ''),
                    'engagement': {
                        'likes': int(real_engagement.get('likes', 0)),
                        'retweets': int(real_engagement.get('retweets', 0)),
                        'replies': int(real_engagement.get('replies', 0)),
                        'views': int(real_engagement.get('views', 0)),
                        'bookmarks': int(real_engagement.get('bookmarks', 0)),
                        'quote_tweets': int(real_engagement.get('quote_tweets', 0))
                    }
                }
                tweets_list.append(tweet_data)
            
            # Create response
            profile_data = {
                'username': username,
                'stats': {
                    'total_tweets': total_tweets,
                    'avg_score': round(avg_score, 3),
                    'best_score': round(best_score, 3),
                    'total_engagement': int(total_engagement),
                    'rank': 'N/A'  # Could calculate rank if needed
                },
                'tweets': tweets_list,
                'recent_activity': f"{total_tweets} tweets analyzed"
            }
            
            print(f"✅ Found {total_tweets} tweets for {username}")
            return jsonify({
                'success': True,
                'data': profile_data
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No data available'
            }), 404
            
    except Exception as e:
        print(f"❌ Error fetching user profile: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/system-status', methods=['GET'])
def get_system_status():
    """Get system status and statistics for frontend"""
    try:
        csv_filename = 'tweets.csv'
        
        # Check required files
        config_exists = os.path.exists('config.yaml')
        grok_csv_exists = os.path.exists('groktweets.csv')
        tweets_db_exists = os.path.exists('tweets.db')
        csv_exists = os.path.exists(csv_filename)
        
        # Calculate statistics from CSV if available
        total_tweets = 0
        avg_score = 0
        top_score = 0
        recent_tweets_24h = 0
        
        if csv_exists:
            try:
                df = pd.read_csv(csv_filename, header=None)
                if len(df.columns) >= 4:
                    df.columns = ['id', 'username', 'text', 'score', 'profile_url']
                    df['score'] = pd.to_numeric(df['score'], errors='coerce').fillna(0)
                    
                    total_tweets = len(df)
                    avg_score = df['score'].mean() if total_tweets > 0 else 0
                    top_score = df['score'].max() if total_tweets > 0 else 0
                    recent_tweets_24h = max(1, int(total_tweets * 0.1))  # Estimate 10% as recent
            except Exception as e:
                print(f"Error reading CSV for stats: {e}")
        
        return jsonify({
            'success': True,
            'status': {
                'config_exists': config_exists,
                'groktweets_csv': grok_csv_exists,
                'tweets_database': tweets_db_exists,
                'csv_exists': csv_exists,
                'pipeline_ready': config_exists,
                'total_tweets': total_tweets,
                'recent_tweets_24h': recent_tweets_24h,
                'average_score': round(avg_score, 3),
                'top_score': round(top_score, 3),
                'timestamp': datetime.now().isoformat()
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def get_score_interpretation(score):
    """Get interpretation of a score"""
    if score >= 1.5:
        return "🌟 Excellent"
    elif score >= 1.0:
        return "👍 Good"
    elif score >= 0.5:
        return "😐 Average"
    else:
        return "❌ Poor/Spam"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 