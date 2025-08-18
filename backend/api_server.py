#!/usr/bin/env python3
"""
Nation Radar VPS API Server
Exposes tweet data via HTTP endpoints for Railway frontend
"""

import os
import sqlite3
import json
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration
DB_PATH = "tweets.db"
PORT = int(os.environ.get('VPS_API_PORT', 5001))

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
def home():
    """API home endpoint"""
    return jsonify({
        "message": "Nation Radar VPS API Server",
        "status": "operational",
        "endpoints": [
            "/api/tweets",
            "/api/leaderboard", 
            "/api/stats",
            "/api/search"
        ],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/tweets')
def get_tweets():
    """Get latest tweets with scores"""
    try:
        limit = request.args.get('limit', 50, type=int)
        
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        query = """
        SELECT id, text, username, score, created_at, engagement
        FROM tweets 
        WHERE score > 0 
        ORDER BY created_at DESC 
        LIMIT ?
        """
        
        cursor = conn.execute(query, (limit,))
        tweets = []
        
        for row in cursor:
            # Parse engagement data (it's stored as TEXT)
            engagement_data = {}
            try:
                if row['engagement']:
                    engagement_data = json.loads(row['engagement'])
                else:
                    engagement_data = {}
            except:
                engagement_data = {}
            
            tweet = {
                "id": row['id'],
                "text": row['text'],
                "username": row['username'],
                "score": row['score'],
                "created_at": row['created_at'],
                "engagement": {
                    "likes": engagement_data.get('likes', 0),
                    "retweets": engagement_data.get('retweets', 0),
                    "replies": engagement_data.get('replies', 0),
                    "views": engagement_data.get('views', 0),
                    "bookmarks": engagement_data.get('bookmarks', 0),
                    "quote_tweets": engagement_data.get('quote_tweets', 0)
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
        limit = request.args.get('limit', 20, type=int)
        
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        query = """
        SELECT id, text, username, score, created_at, engagement
        FROM tweets 
        WHERE score > 0 
        ORDER BY score DESC 
        LIMIT ?
        """
        
        cursor = conn.execute(query, (limit,))
        leaderboard = []
        
        for row in cursor:
            # Parse engagement data (it's stored as TEXT)
            engagement_data = {}
            try:
                if row['engagement']:
                    engagement_data = json.loads(row['engagement'])
                else:
                    engagement_data = {}
            except:
                engagement_data = {}
            
            tweet = {
                "id": row['id'],
                "text": row['text'],
                "username": row['username'],
                "score": row['score'],
                "created_at": row['created_at'],
                "engagement": {
                    "likes": engagement_data.get('likes', 0),
                    "retweets": engagement_data.get('retweets', 0),
                    "replies": engagement_data.get('replies', 0),
                    "views": engagement_data.get('views', 0),
                    "bookmarks": engagement_data.get('bookmarks', 0),
                    "quote_tweets": engagement_data.get('quote_tweets', 0)
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

@app.route('/api/stats')
def get_stats():
    """Get system statistics"""
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
        
        limit = request.args.get('limit', 20, type=int)
        
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        # Search in tweet text
        search_query = """
        SELECT id, text, username, score, created_at, engagement
        FROM tweets 
        WHERE text LIKE ? AND score > 0
        ORDER BY score DESC 
        LIMIT ?
        """
        
        cursor = conn.execute(search_query, (f'%{query}%', limit))
        results = []
        
        for row in cursor:
            # Parse engagement data (it's stored as TEXT)
            engagement_data = {}
            try:
                if row['engagement']:
                    engagement_data = json.loads(row['engagement'])
                else:
                    engagement_data = {}
            except:
                engagement_data = {}
            
            tweet = {
                "id": row['id'],
                "text": row['text'],
                "username": row['username'],
                "score": row['score'],
                "created_at": row['created_at'],
                "engagement": {
                    "likes": engagement_data.get('likes', 0),
                    "retweets": engagement_data.get('retweets', 0),
                    "replies": engagement_data.get('replies', 0),
                    "views": engagement_data.get('views', 0),
                    "bookmarks": engagement_data.get('bookmarks', 0),
                    "quote_tweets": engagement_data.get('quote_tweets', 0)
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
    print(f"🚀 Starting Nation Radar VPS API Server on port {PORT}")
    print(f"📊 Database: {DB_PATH}")
    print(f"🌐 API endpoints available at:")
    print(f"   - http://localhost:{PORT}/")
    print(f"   - http://localhost:{PORT}/api/tweets")
    print(f"   - http://localhost:{PORT}/api/leaderboard")
    print(f"   - http://localhost:{PORT}/api/stats")
    print(f"   - http://localhost:{PORT}/api/search?q=keyword")
    
    app.run(debug=False, host='0.0.0.0', port=PORT)
