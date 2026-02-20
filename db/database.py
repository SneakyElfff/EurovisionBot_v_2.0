import sqlite3
import logging
from config import DB_FILE

logger = logging.getLogger(__name__)

def init_db():
    logger.info('Initializing database')

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS config (key TEXT PRIMARY KEY, value TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS subscribers (chat_id INTEGER PRIMARY KEY)")
        cursor.execute("INSERT OR IGNORE INTO config (key, value) VALUES ('last_video_id', '')")

        conn.commit()