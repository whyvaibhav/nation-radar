import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import GOOGLE_SHEETS_CREDENTIALS

class GoogleSheetsStorage:
    def __init__(self, sheet_name, sheet_tab="Sheet1"):
        if not sheet_name:
            raise ValueError("sheet_name is required for Google Sheets storage")
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_CREDENTIALS, scope)
        self.sheet = gspread.authorize(creds).open(sheet_name).worksheet(sheet_tab)
        self.existing_ids = set(self.sheet.col_values(1))

    def append_row(self, tweet):
        if tweet["id"] in self.existing_ids:
            return False
        self.sheet.append_row([
            tweet["id"],
            tweet["username"],
            tweet["text"],
            f"{tweet.get('score', 0.0):.2f}",
            tweet.get("created_at", ""),
            tweet.get("profile_pic", "")
        ], value_input_option="RAW")
        self.existing_ids.add(tweet["id"])
        return True 