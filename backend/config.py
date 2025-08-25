import os
from dotenv import load_dotenv
import yaml

load_dotenv()

# Load YAML config
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.yaml')
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# API Keys (set these in a .env file for security)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'x')
SOCIALDATA_API_KEY = os.getenv('SOCIALDATA_API_KEY', 'x')
GOOGLE_SHEETS_CREDENTIALS = os.getenv('GOOGLE_SHEETS_CREDENTIALS', 'credentials.json')
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', 'YOUR_RAPIDAPI_KEY')
NATION_AGENT_API_KEY = os.getenv('NATION_AGENT_API_KEY', 'YOUR_NATION_AGENT_API_KEY')

# Configuration for Nation Radar Pipeline

# Keywords to search for
KEYWORDS = [
    "Crestal",
    "Crestal Network", 
    "Nation.fun",
    "$NATION"
]

# How many days back to search
DAYS_LOOKBACK = 21
# CSV_FILENAME removed - using SQLite database instead

# Other settings
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False') == 'True'