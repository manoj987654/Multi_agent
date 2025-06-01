import sqlite3
from datetime import datetime

class SharedMemory:
    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()
    
    def _create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS context (
            id INTEGER PRIMARY KEY,
            conversation_id TEXT,
            format TEXT,
            intent TEXT,
            sender TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.conn.commit()
    
    def store_context(self, conversation_id, format, intent, sender, content):
        self.conn.execute("""
        INSERT INTO context (conversation_id, format, intent, sender, content)
        VALUES (?, ?, ?, ?, ?)
        """, (conversation_id, format, intent, sender, content))
        self.conn.commit()
    
    def get_context(self, conversation_id):
        cursor = self.conn.execute("""
        SELECT * FROM context WHERE conversation_id = ?
        """, (conversation_id,))
        return cursor.fetchone()