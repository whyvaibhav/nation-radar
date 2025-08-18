#!/usr/bin/env python3
"""
Vercel-optimized Flask API for Crestal Tweet Monitor
Serverless deployment version
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import json
import pandas as pd
from datetime import datetime
import requests

# Create Flask app
app = Flask(__name__)
CORS(app)

# Mock data for Vercel deployment (since we can't access VPS files directly)
MOCK_CRESTAL_DATA = [
    {
        "id": "1954862780156182819",
        "username": "crestal_builder",
        "text": "Just deployed my first agent on @crestalnetwork! The autonomous capabilities are incredible. $NATION holders are going to love this ecosystem growth 🚀",
        "score": 1.85,
        "profile_url": "https://twitter.com/crestal_builder"
    },
    {
        "id": "1954860123456789012",
        "username": "defi_analyst",
        "text": "@crestalnetwork's Nation Agent system is revolutionizing how we think about autonomous AI. The quality scoring mechanism ensures only valuable content rises to the top.",
        "score": 1.65,
        "profile_url": "https://twitter.com/defi_analyst"
    },
    {
        "id": "1954858987654321098",
        "username": "crypto_researcher",
        "text": "Researching $NATION tokenomics and the Crestal ecosystem. The agent-to-agent interactions are fascinating from a technical perspective.",
        "score": 1.45,
        "profile_url": "https://twitter.com/crypto_researcher"
    },
    {
        "id": "1954857111222333444",
        "username": "ai_enthusiast",
        "text": "The Nation Agent on Crestal Network just scored my content perfectly! This AI understands context and value better than any system I've seen.",
        "score": 1.75,
        "profile_url": "https://twitter.com/ai_enthusiast"
    },
    {
        "id": "1954855000111222333",
        "username": "web3_dev",
        "text": "Building on @crestalnetwork has been an amazing experience. The agent infrastructure makes deployment seamless. $NATION 🌟",
        "score": 1.55,
        "profile_url": "https://twitter.com/web3_dev"
    }
]

# Serve static files from frontend directory
@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

# API Routes
@app.route('/api/crestal-data', methods=['GET'])
def get_crestal_data():
    """Get Crestal tweet data - Vercel version with mock data"""
    try:
        # In production, this would fetch from your data source
        # For demo purposes, using mock data
        data = MOCK_CRESTAL_DATA
        
        # Calculate stats
        total_tweets = len(data)
        scores = [tweet['score'] for tweet in data]
        avg_score = sum(scores) / len(scores) if scores else 0
        high_quality = len([s for s in scores if s >= 1.0])
        low_quality = len([s for s in scores if s < 0.5])
        
        return jsonify({
            'success': True,
            'data': data,
            'stats': {
                'total_tweets': total_tweets,
                'avg_score': round(avg_score, 2),
                'high_quality': high_quality,
                'low_quality': low_quality
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get top contributors leaderboard - Vercel version"""
    try:
        limit = int(request.args.get('limit', 20))
        
        # Process mock data into leaderboard format
        user_stats = {}
        for tweet in MOCK_CRESTAL_DATA:
            username = tweet['username']
            if username not in user_stats:
                user_stats[username] = {
                    'scores': [],
                    'profile_url': tweet['profile_url']
                }
            user_stats[username]['scores'].append(tweet['score'])
        
        # Create leaderboard
        leaderboard = []
        for username, stats in user_stats.items():
            scores = stats['scores']
            leaderboard.append({
                'username': username,
                'avg_score': round(sum(scores) / len(scores), 2),
                'best_score': max(scores),
                'tweet_count': len(scores),
                'profile_url': stats['profile_url']
            })
        
        # Sort by average score
        leaderboard.sort(key=lambda x: x['avg_score'], reverse=True)
        leaderboard = leaderboard[:limit]
        
        # Add ranks
        for i, user in enumerate(leaderboard):
            user['rank'] = i + 1
        
        return jsonify({
            'success': True,
            'leaderboard': leaderboard,
            'stats': {
                'total_contributors': len(user_stats),
                'showing': len(leaderboard)
            }
        })
        
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
        
        # For Vercel demo, return mock scoring
        # In production, this would call the actual Nation Agent API
        mock_score = min(2.0, max(0.0, len(text) / 100))  # Simple mock scoring
        
        return jsonify({
            'success': True,
            'score': round(mock_score, 2),
            'interpretation': get_score_interpretation(mock_score),
            'note': 'Demo mode - connect to real Nation Agent API for production'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/system-status', methods=['GET'])
def get_system_status():
    """Get system status - Vercel version"""
    try:
        return jsonify({
            'success': True,
            'status': {
                'platform': 'Vercel',
                'mode': 'Demo',
                'data_source': 'Mock Data',
                'pipeline_ready': True,
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

# Vercel serverless handler
def handler(request):
    return app(request.environ, lambda *args: None)

if __name__ == '__main__':
    app.run(debug=True)
