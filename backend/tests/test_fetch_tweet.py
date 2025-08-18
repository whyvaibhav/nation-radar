import requests

# Replace with your actual FastAPI server URL if different
API_URL = "http://localhost:8000/fetch_tweet"

# Replace with a real tweet URL you want to test
# Example: Elon Musk tweet (replace with a valid one if needed)
tweet_url = "https://x.com/WilkinsMor82048/status/1950096641316229613"

params = {"tweet_url": tweet_url}
response = requests.get(API_URL, params=params)

if response.status_code == 200:
    data = response.json()
    print("Tweet Text:")
    print(data.get("tweet_text", "N/A"))
    print("\nEngagement Metrics:")
    for k, v in data.get("engagement", {}).items():
        print(f"{k}: {v}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)