import requests
from datetime import datetime, timezone, timedelta
from config import SOCIALDATA_API_KEY, DAYS_LOOKBACK

class SocialDataFetcher:
    def __init__(self, days_lookback=None):
        self.api_key = SOCIALDATA_API_KEY
        self.days_lookback = days_lookback if days_lookback is not None else DAYS_LOOKBACK

    def fetch(self, keyword):
        tweets, cursor = [], None
        since_dt = datetime.now(timezone.utc) - timedelta(days=self.days_lookback)
        since_date = since_dt.strftime("%Y-%m-%d_%H:%M:%S_UTC")
        while True:
            params = {
                "query": f"{keyword} since:{since_date}",
                "type": "Latest"
            }
            if cursor:
                params["cursor"] = cursor
            headers = {"Authorization": f"Bearer {self.api_key}"}
            try:
                r = requests.get("https://api.socialdata.tools/twitter/search", params=params, headers=headers)
                if r.status_code != 200:
                    break
                data = r.json()
                page = data.get("tweets", [])
                if not page:
                    break
                for item in page:
                    tid  = item.get("id_str")
                    text = item.get("full_text", "")
                    user = item.get("user", {})
                    username = user.get("screen_name", "unknown")
                    profile_pic_url = user.get("profile_image_url_https", "")
                    created_at = item.get("tweet_created_at")
                    if profile_pic_url:
                        profile_pic_url = profile_pic_url.replace("_normal", "_400x400")
                    tweets.append({
                        "id": tid,
                        "text": text.strip(),
                        "username": username,
                        "profile_pic": profile_pic_url,
                        "created_at": created_at
                    })
                cursor = data.get("next_cursor")
                if not cursor:
                    break
            except Exception:
                break
        return tweets 