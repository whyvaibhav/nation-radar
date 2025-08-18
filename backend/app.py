#!/usr/bin/env python3
"""
Flask API for Tweet Mention Tracker Frontend
"""

from flask import Flask, jsonify, request, send_from_directory, Response
from flask_cors import CORS
import os
import json
import pandas as pd
from datetime import datetime
import subprocess
import sys
import csv
from io import StringIO

# Import our existing modules
# Note: main.py removed - this app now focuses on Crestal-only monitoring
from nation_agent import get_agent_score, format_tweet_for_agent
from fetchers.ryan_twitter_fetcher import RyanTwitterFetcher

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Serve static files from the frontend directory
@app.route('/')
def serve_frontend():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('frontend', path)

# API Routes
@app.route('/api/crestal-data', methods=['GET'])
def get_crestal_data():
    """Get Crestal tweet data from tweets.csv"""
    try:
        csv_filename = 'tweets.csv'
        format_type = request.args.get('format', 'json')
        
        if not os.path.exists(csv_filename):
            return jsonify({
                'success': True,
                'data': [],
                'stats': {
                    'total_tweets': 0,
                    'avg_score': 0,
                    'high_quality': 0,
                    'low_quality': 0
                }
            })
        
        # Read CSV data
        df = pd.read_csv(csv_filename, header=None)
        if len(df.columns) >= 4:
            df.columns = ['id', 'username', 'text', 'score', 'profile_url']
            
            # Convert scores to numeric
            df['score'] = pd.to_numeric(df['score'], errors='coerce').fillna(0)
            
            # Calculate stats
            total_tweets = len(df)
            avg_score = df['score'].mean() if total_tweets > 0 else 0
            high_quality = len(df[df['score'] >= 1.0])
            low_quality = len(df[df['score'] < 0.5])
            
            # Convert to list of dictionaries
            data = []
            for _, row in df.iterrows():
                data.append({
                    'id': row['id'],
                    'username': row['username'],
                    'text': row['text'],
                    'score': float(row['score']),
                    'profile_url': row['profile_url'],
                    'engagement': {
                        'likes': 0,
                        'retweets': 0,
                        'replies': 0,
                        'views': 0
                    }
                })
            
            # Handle CSV export
            if format_type == 'csv':
                from flask import Response
                output = StringIO()
                writer = csv.writer(output)
                writer.writerow(['ID', 'Username', 'Text', 'Score', 'Profile URL'])
                for item in data:
                    writer.writerow([item['id'], item['username'], item['text'], item['score'], item['profile_url']])
                
                response = Response(
                    output.getvalue(),
                    mimetype='text/csv',
                    headers={'Content-Disposition': f'attachment; filename=nation-radar-{datetime.now().strftime("%Y%m%d")}.csv'}
                )
                return response
            
            return jsonify({
                'success': True,
                'data': data,
                'stats': {
                    'total_tweets': total_tweets,
                    'avg_score': round(avg_score, 2),
                    'high_quality': high_quality,
                    'low_quality': low_quality,
                    'unique_users': len(df['username'].unique())
                }
            })
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

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get top contributors leaderboard"""
    try:
        csv_filename = 'tweets.csv'
        limit = int(request.args.get('limit', 20))  # Default top 20
        
        if not os.path.exists(csv_filename):
            return jsonify({
                'success': True,
                'leaderboard': [],
                'stats': {'total_contributors': 0}
            })
        
        # Read and process data
        df = pd.read_csv(csv_filename, header=None)
        if len(df.columns) >= 4:
            df.columns = ['id', 'username', 'text', 'score', 'profile_url']
            df['score'] = pd.to_numeric(df['score'], errors='coerce').fillna(0)
            
            # Group by username and calculate stats
            leaderboard = df.groupby('username').agg({
                'score': ['mean', 'max', 'count'],
                'profile_url': 'first'
            }).round(2)
            
            # Flatten column names
            leaderboard.columns = ['avg_score', 'best_score', 'tweet_count', 'profile_url']
            leaderboard = leaderboard.reset_index()
            
            # Sort by average score and limit results
            leaderboard = leaderboard.sort_values('avg_score', ascending=False).head(limit)
            
            # Convert to list
            result = []
            for _, row in leaderboard.iterrows():
                result.append({
                    'username': row['username'],
                    'avg_score': float(row['avg_score']),
                    'best_score': float(row['best_score']),
                    'tweet_count': int(row['tweet_count']),
                    'profile_url': row['profile_url'],
                    'rank': len(result) + 1
                })
            
            return jsonify({
                'success': True,
                'leaderboard': result,
                'stats': {
                    'total_contributors': len(df['username'].unique()),
                    'showing': len(result)
                }
            })
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
    """Get system status and configuration"""
    try:
        # Check required files
        config_exists = os.path.exists('config.yaml')
        grok_csv_exists = os.path.exists('groktweets.csv')
        tweets_db_exists = os.path.exists('tweets.db')
        
        return jsonify({
            'success': True,
            'status': {
                'config_exists': config_exists,
                'groktweets_csv': grok_csv_exists,
                'tweets_database': tweets_db_exists,
                'pipeline_ready': config_exists,
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
    app.run(debug=True, host='0.0.0.0', port=5000) 