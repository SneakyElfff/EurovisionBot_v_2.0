import os
from dotenv import load_dotenv

load_dotenv()

DB_FILE = 'bot.db'

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE_CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID')

PHRASES = [p.strip() for p in os.getenv('PHRASES', '').split(',') if p.strip()]
CHECK_INTERVAL_MINUTES = int(os.getenv('CHECK_INTERVAL_MINUTES', 10))

if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN must be set")

if not YOUTUBE_API_KEY:
    raise RuntimeError("YOUTUBE_API_KEY must be set")

if not YOUTUBE_CHANNEL_ID:
    raise RuntimeError("YOUTUBE_CHANNEL_ID must be set")