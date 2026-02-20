import sqlite3
from config import DB_FILE

def add_subscriber(chat_id: int):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("INSERT OR IGNORE INTO subscribers (chat_id) VALUES (?)", (chat_id,))

def remove_subscriber(chat_id: int):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("DELETE FROM subscribers WHERE chat_id = ?", (chat_id,))

def get_subscribers():
    with sqlite3.connect(DB_FILE) as conn:
        return [row[0] for row in conn.execute("SELECT chat_id FROM subscribers")]