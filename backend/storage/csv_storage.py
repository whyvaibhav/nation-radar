import csv
import os

class CSVStorage:
    def __init__(self, filename="tweets.csv"):
        self.filename = filename
        self.existing_ids = set()
        if os.path.exists(self.filename) and os.path.getsize(self.filename) > 0:
            with open(self.filename, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        self.existing_ids.add(row[0])

    def append_row(self, tweet):
        if tweet["id"] in self.existing_ids:
            return False
        with open(self.filename, "a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Construct tweet URL
            tweet_url = f"https://x.com/{tweet['username']}/status/{tweet['id']}"
            # Get the full tweet text, ensuring it's not truncated
            tweet_text = tweet.get('text', '').replace('\n', ' ').strip()
            writer.writerow([
                tweet["id"],
                tweet["username"],
                tweet_text,
                f"{tweet.get('score', 0.0):.2f}",
                tweet_url
            ])
        self.existing_ids.add(tweet["id"])
        return True 