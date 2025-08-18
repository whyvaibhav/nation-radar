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
VPS_API_URL = os.environ.get('VPS_API_URL', 'http://143.198.226.161:5001')

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
    """Get latest Crestal-related data from VPS API (which reads from tweets.db)"""
    try:
        import requests
        
        # Fetch data from VPS API
        response = requests.get(f"{VPS_API_URL}/api/tweets", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            return jsonify({"error": f"VPS API error: {response.status_code}"}), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to connect to VPS API: {str(e)}"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/leaderboard')
def get_leaderboard():
    """Get top tweets by score from VPS API (which reads from tweets.db)"""
    try:
        import requests
        
        # Fetch data from VPS API
        response = requests.get(f"{VPS_API_URL}/api/leaderboard", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            return jsonify({"error": f"VPS API error: {response.status_code}"}), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to connect to VPS API: {str(e)}"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/system-status')
def get_system_status():
    """Get system status and statistics from VPS API (which reads from tweets.db)"""
    try:
        import requests
        
        # Fetch data from VPS API
        response = requests.get(f"{VPS_API_URL}/api/stats", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # Add Railway-specific info
            data['railway_status'] = 'operational'
            data['vps_connection'] = 'connected'
            return jsonify(data)
        else:
            return jsonify({"error": f"VPS API error: {response.status_code}"}), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({
            "success": False,
            "status": "degraded",
            "railway_status": "operational",
            "vps_connection": "disconnected",
            "error": f"Failed to connect to VPS API: {str(e)}"
        }), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/search')
def search_tweets():
    """Search tweets by keyword via VPS API (which reads from tweets.db)"""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({"error": "Query parameter 'q' is required"}), 400
        
        import requests
        
        # Fetch data from VPS API
        response = requests.get(f"{VPS_API_URL}/api/search?q={query}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            return jsonify({"error": f"VPS API error: {response.status_code}"}), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to connect to VPS API: {str(e)}"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=os.environ.get('DEBUG') == '1', host='0.0.0.0', port=port)
