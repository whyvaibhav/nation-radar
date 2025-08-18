#!/usr/bin/env python3
"""
Nation Radar Intelligence Hub - Unified App
Serves both frontend and backend API endpoints
"""

import os
import sqlite3
import json
from datetime import datetime, timedelta
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Configuration
DB_PATH = os.path.join('backend', 'tweets.db')
CSV_PATH = os.path.join('backend', 'tweets.csv')

def get_db_connection():
    """Create a database connection"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def serve_frontend():
    """Serve the main dashboard"""
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static assets"""
    return send_from_directory('frontend', path)

# API Endpoints
@app.route('/api/crestal-data')
def get_crestal_data():
    """Get latest Crestal-related data"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        # Get recent tweets with scores
        query = """
        SELECT id, text, username, score, created_at, 
               engagement_likes, engagement_retweets, engagement_replies, 
               engagement_views, engagement_bookmarks, engagement_quote_tweets
        FROM tweets 
        WHERE score > 0 
        ORDER BY created_at DESC 
        LIMIT 50
        """
        
        cursor = conn.execute(query)
        tweets = []
        
        for row in cursor:
            tweet = {
                "id": row['id'],
                "text": row['text'],
                "username": row['username'],
                "score": row['score'],
                "created_at": row['created_at'],
                "engagement": {
                    "likes": row['engagement_likes'] or 0,
                    "retweets": row['engagement_retweets'] or 0,
                    "replies": row['engagement_replies'] or 0,
                    "views": row['engagement_views'] or 0,
                    "bookmarks": row['engagement_bookmarks'] or 0,
                    "quote_tweets": row['engagement_quote_tweets'] or 0
                }
            }
            tweets.append(tweet)
        
        conn.close()
        
        return jsonify({
            "success": True,
            "data": tweets,
            "count": len(tweets),
            "last_updated": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/leaderboard')
def get_leaderboard():
    """Get top tweets by score"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        # Get top tweets by score
        query = """
        SELECT id, text, username, score, created_at,
               engagement_likes, engagement_retweets, engagement_replies,
               engagement_views, engagement_bookmarks, engagement_quote_tweets
        FROM tweets 
        WHERE score > 0 
        ORDER BY score DESC 
        LIMIT 20
        """
        
        cursor = conn.execute(query)
        leaderboard = []
        
        for row in cursor:
            tweet = {
                "id": row['id'],
                "text": row['text'],
                "username": row['username'],
                "score": row['score'],
                "created_at": row['created_at'],
                "engagement": {
                    "likes": row['engagement_likes'] or 0,
                    "retweets": row['engagement_retweets'] or 0,
                    "replies": row['engagement_replies'] or 0,
                    "views": row['engagement_views'] or 0,
                    "bookmarks": row['engagement_bookmarks'] or 0,
                    "quote_tweets": row['engagement_quote_tweets'] or 0
                }
            }
            leaderboard.append(tweet)
        
        conn.close()
        
        return jsonify({
            "success": True,
            "data": leaderboard,
            "count": len(leaderboard)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/system-status')
def get_system_status():
    """Get system status and statistics"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        # Get basic stats
        cursor = conn.execute("SELECT COUNT(*) as total FROM tweets")
        total_tweets = cursor.fetchone()['total']
        
        cursor = conn.execute("SELECT COUNT(*) as scored FROM tweets WHERE score > 0")
        scored_tweets = cursor.fetchone()['scored']
        
        cursor = conn.execute("SELECT AVG(score) as avg_score FROM tweets WHERE score > 0")
        avg_score = cursor.fetchone()['avg_score'] or 0
        
        cursor = conn.execute("SELECT MAX(created_at) as last_update FROM tweets")
        last_update = cursor.fetchone()['last_update']
        
        conn.close()
        
        return jsonify({
            "success": True,
            "status": "operational",
            "statistics": {
                "total_tweets": total_tweets,
                "scored_tweets": scored_tweets,
                "average_score": round(avg_score, 3),
                "last_update": last_update,
                "database_size": os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/search')
def search_tweets():
    """Search tweets by keyword"""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({"error": "Query parameter 'q' is required"}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        # Search in tweet text
        search_query = """
        SELECT id, text, username, score, created_at,
               engagement_likes, engagement_retweets, engagement_replies,
               engagement_views, engagement_bookmarks, engagement_quote_tweets
        FROM tweets 
        WHERE text LIKE ? AND score > 0
        ORDER BY score DESC 
        LIMIT 20
        """
        
        cursor = conn.execute(search_query, (f'%{query}%',))
        results = []
        
        for row in cursor:
            tweet = {
                "id": row['id'],
                "text": row['text'],
                "username": row['username'],
                "score": row['score'],
                "created_at": row['created_at'],
                "engagement": {
                    "likes": row['engagement_likes'] or 0,
                    "retweets": row['engagement_retweets'] or 0,
                    "replies": row['engagement_replies'] or 0,
                    "views": row['engagement_views'] or 0,
                    "bookmarks": row['engagement_bookmarks'] or 0,
                    "quote_tweets": row['engagement_quote_tweets'] or 0
                }
            }
            results.append(tweet)
        
        conn.close()
        
        return jsonify({
            "success": True,
            "query": query,
            "results": results,
            "count": len(results)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=os.environ.get('DEBUG') == '1', host='0.0.0.0', port=port)
