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

# Get the absolute path to the frontend directory
FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))  # Root directory

@app.route('/debug')
def debug_info():
    """Debug endpoint to check file paths and structure"""
    try:
        current_dir = os.getcwd()
        app_dir = os.path.dirname(os.path.abspath(__file__))
        frontend_exists = os.path.exists(FRONTEND_DIR)
        index_exists = os.path.exists(os.path.join(FRONTEND_DIR, 'index.html')) if frontend_exists else False
        
        debug_info = {
            "current_working_directory": current_dir,
            "app_directory": app_dir,
            "frontend_dir_path": FRONTEND_DIR,
            "frontend_dir_exists": frontend_exists,
            "index_html_exists": index_exists,
            "directory_contents": os.listdir(app_dir) if os.path.exists(app_dir) else [],
            "frontend_contents": os.listdir(FRONTEND_DIR) if frontend_exists else []
        }
        
        return jsonify(debug_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def serve_frontend():
    """Serve the main dashboard"""
    try:
        # Check if the directory exists
        if not os.path.exists(FRONTEND_DIR):
            return f"Frontend directory not found: {FRONTEND_DIR}", 500
        
        # Check if index.html exists
        index_path = os.path.join(FRONTEND_DIR, 'index.html')
        if not os.path.exists(index_path):
            return f"index.html not found in: {FRONTEND_DIR}", 500
        
        # Add CSP headers to allow JavaScript execution
        response = send_from_directory(FRONTEND_DIR, 'index.html')
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-eval' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https:;"
        return response
    except Exception as e:
        return f"Error serving frontend: {str(e)}", 500

@app.route('/<path:path>')
def serve_static(path):
    """Serve static assets"""
    try:
        # Check if the directory exists
        if not os.path.exists(FRONTEND_DIR):
            return f"Frontend directory not found: {FRONTEND_DIR}", 500
        
        # Add CSP headers for JavaScript files
        response = send_from_directory(FRONTEND_DIR, path)
        if path.endswith('.js') or path.endswith('.html'):
            response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-eval' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https:;"
        return response
    except Exception as e:
        return f"Error serving static file {path}: {str(e)}", 500

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
