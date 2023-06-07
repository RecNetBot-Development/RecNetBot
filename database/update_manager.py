import sqlite3
from typing import Optional
from sqlite3 import Connection
from enum import Enum

class UpdateManager():
    def __init__(self, database: Connection):
        self.conn = database
        self.c = self.conn.cursor()
        self.create_table()
        
    def create_table(self):
        """
        Creates the update table
            - discord_id integer: a Discord account's id
            - update int: The latest read update timestamp
            - announcement int: The latest read announcement timestamp
        """
        
        self.c.execute(f"""CREATE TABLE IF NOT EXISTS updates (discord_id integer PRIMARY KEY, latest integer, announcement integer)""")
        
    def get_latest_read(self, discord_id: int) -> Optional[str]:
        self.c.execute(f"""SELECT * FROM updates WHERE discord_id = :discord_id""", {"discord_id": discord_id})
        data = self.c.fetchall()
        if not data: return ()
        return data[0]
    
    def mark_as_read(self, discord_id: int, latest_update: int, latest_announcement: int):
        with self.conn:
            self.c.execute(f"""REPLACE INTO updates VALUES (:discord_id, :update, :announcement)""", {"discord_id": discord_id, "update": latest_update, "announcement": latest_announcement})

    
if __name__ == "__main__":
    db = sqlite3.connect(":memory:")
    cm = UpdateManager(db)

    print(cm.get_latest_read(1))
    cm.mark_as_read(1, 32, 45)
    print(cm.get_latest_read(1))

    """
    cm = BookmarkManager(db)
    
    cm.create_bookmark(69, BookmarkTypes.ACCOUNTS, 1)
    cm.create_bookmark(69, BookmarkTypes.ACCOUNTS, 564)
    cm.create_bookmark(69, BookmarkTypes.ROOMS, 512464)
    print("Accounts", cm.get_bookmarks(69, BookmarkTypes.ACCOUNTS))
    print("Rooms", cm.get_bookmarks(69, BookmarkTypes.ROOMS))
    cm.delete_all_bookmarks_by_type(69, BookmarkTypes.ACCOUNTS)
    print("Accounts", cm.get_bookmarks(69, BookmarkTypes.ACCOUNTS))
    print("Rooms", cm.get_bookmarks(69, BookmarkTypes.ROOMS))
    """