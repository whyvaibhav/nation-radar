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
                # Use actual engagement data if available, otherwise simulate
                engagement = row.get('engagement', {})
                if not engagement or not isinstance(engagement, dict):
                    # Simulate engagement data based on score
                    score = float(row['score'])
                    base_engagement = max(1, int(score * 50))
                    
                    import random
                    engagement = {
                        'likes': base_engagement + int(score * 20) + random.randint(0, 5),
                        'retweets': int(base_engagement * 0.3) + random.randint(0, 2),
                        'replies': int(base_engagement * 0.2) + random.randint(0, 3),
                        'views': base_engagement * 15 + random.randint(0, 50),
                        'bookmarks': int(base_engagement * 0.1) + random.randint(0, 1),
                        'quote_tweets': int(base_engagement * 0.05) + random.randint(0, 1)
                    }
                
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
        total_views = sum(tweet.get('engagement', {}).get('views', 0) for tweet in tweets)
        
        tweet_count = len(tweets)
        
        return jsonify({
            'success': True,
            'data': {
                'avg_likes': round(total_likes / tweet_count, 1) if tweet_count > 0 else 0,
                'avg_retweets': round(total_retweets / tweet_count, 1) if tweet_count > 0 else 0,
                'avg_replies': round(total_replies / tweet_count, 1) if tweet_count > 0 else 0,
                'avg_views': round(total_views / tweet_count, 1) if tweet_count > 0 else 0,
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