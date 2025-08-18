#!/usr/bin/env python3
"""
Test script to debug SocialData API
"""

import requests
import os
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()

def test_socialdata_api():
    api_key = os.getenv('SOCIALDATA_API_KEY')
    print(f"API Key: {api_key[:10]}..." if api_key else "No API key found")
    
    # Test with a simple query
    since_dt = datetime.now(timezone.utc) - timedelta(days=7)
    since_date = since_dt.strftime("%Y-%m-%d_%H:%M:%S_UTC")
    
    test_keywords = ["@375ai_", "gradient", "AI", "crypto"]
    
    for keyword in test_keywords:
        print(f"\n🔍 Testing keyword: {keyword}")
        params = {
            "query": f"{keyword} since:{since_date}",
            "type": "Latest"
        }
        headers = {"Authorization": f"Bearer {api_key}"}
        
        try:
            print(f"Request URL: https://api.socialdata.tools/twitter/search")
            print(f"Params: {params}")
            
            r = requests.get("https://api.socialdata.tools/twitter/search", params=params, headers=headers)
            print(f"Status Code: {r.status_code}")
            
            if r.status_code == 200:
                data = r.json()
                tweets = data.get("tweets", [])
                print(f"Found {len(tweets)} tweets")
                
                if tweets:
                    print("Sample tweet:")
                    sample = tweets[0]
                    print(f"  ID: {sample.get('id_str')}")
                    print(f"  Text: {sample.get('full_text', '')[:100]}...")
                    print(f"  User: @{sample.get('user', {}).get('screen_name', 'unknown')}")
                else:
                    print("No tweets found")
            else:
                print(f"Error response: {r.text}")
                
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    test_socialdata_api() 