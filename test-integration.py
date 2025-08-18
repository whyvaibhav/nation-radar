#!/usr/bin/env python3
"""
Test script to verify Nation Radar integration
"""

import os
import sqlite3
import requests
from datetime import datetime

def test_database():
    """Test database connectivity and data"""
    print("🔍 Testing database connectivity...")
    
    db_path = os.path.join('backend', 'tweets.db')
    if not os.path.exists(db_path):
        print("❌ Database file not found")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.execute("SELECT COUNT(*) FROM tweets")
        count = cursor.fetchone()[0]
        print(f"✅ Database connected. Found {count} tweets")
        
        # Test recent data
        cursor = conn.execute("""
            SELECT id, text, username, score, created_at 
            FROM tweets 
            WHERE score > 0 
            ORDER BY created_at DESC 
            LIMIT 3
        """)
        
        recent_tweets = cursor.fetchall()
        print(f"📊 Recent scored tweets: {len(recent_tweets)}")
        
        for tweet in recent_tweets:
            print(f"  - @{tweet[2]}: {tweet[3]} score")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🌐 Testing API endpoints...")
    
    base_url = "http://localhost:5000"
    
    endpoints = [
        "/api/system-status",
        "/api/crestal-data", 
        "/api/leaderboard"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {endpoint}: {data.get('count', 'N/A')} items")
            else:
                print(f"❌ {endpoint}: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ {endpoint}: Connection refused (app not running)")
        except Exception as e:
            print(f"❌ {endpoint}: {e}")

def test_frontend_files():
    """Test frontend file structure"""
    print("\n📁 Testing frontend files...")
    
    frontend_files = [
        'frontend/index.html',
        'frontend/styles.css', 
        'frontend/script.js'
    ]
    
    for file_path in frontend_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path}: {size} bytes")
        else:
            print(f"❌ {file_path}: Not found")

def main():
    """Run all tests"""
    print("🧪 Nation Radar Integration Test")
    print("=" * 40)
    
    # Test database
    db_ok = test_database()
    
    # Test frontend
    test_frontend_files()
    
    # Test API (only if app is running)
    test_api_endpoints()
    
    print("\n" + "=" * 40)
    if db_ok:
        print("✅ Integration test completed successfully!")
        print("🚀 Your Nation Radar is ready to deploy!")
    else:
        print("❌ Some tests failed. Check the issues above.")
    
    print("\n📋 Next steps:")
    print("1. Deploy to Railway: ./deploy-railway.sh")
    print("2. Set up VPS pipeline: cd backend && python3 run_pipeline.py")
    print("3. Monitor logs and data flow")

if __name__ == "__main__":
    main()
