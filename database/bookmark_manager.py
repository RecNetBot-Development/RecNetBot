import sqlite3
from typing import Optional
from sqlite3 import Connection
from enum import Enum

class BookmarkTypes(Enum):
    ACCOUNTS = 1
    ROOMS = 2
    INVENTIONS = 3
    EVENTS = 4
    POSTS = 5

class BookmarkManager():
    def __init__(self, database: Connection):
        self.conn = database
        self.c = self.conn.cursor()
        self.create_table()
        
    def create_table(self):
        """
        Creates the linked_accounts table
            - discord_id integer: a Discord account's id
            - type int: BookmarkTypes type
            - id int: id of the bookmarked item
        """
        
        self.c.execute(f"""CREATE TABLE IF NOT EXISTS bookmarks (discord_id integer, type integer, id integer, PRIMARY KEY (discord_id, type, id))""")
        
        
    def get_bookmarks(self, discord_id: int, type: BookmarkTypes) -> Optional[str]:
        self.c.execute(f"""SELECT * FROM bookmarks WHERE discord_id = :discord_id AND type = :type""", {"discord_id": discord_id, "type": type.value})
        data = self.c.fetchall()
        if not data: return []
        return list(map(lambda bm: bm[2], data))
    
    def create_bookmark(self, discord_id: int, type: BookmarkTypes, id: int):
        with self.conn:
            self.c.execute(f"""REPLACE INTO bookmarks VALUES (:discord_id, :type, :id)""", {"discord_id": discord_id, "type": type.value, "id": id})
        
    def delete_bookmark(self, discord_id: int, type: BookmarkTypes, id: int):
        with self.conn:
            self.c.execute(f"""DELETE FROM bookmarks WHERE discord_id = :discord_id AND type = :type AND id = :id""", {"discord_id": discord_id, "type": type.value, "id": id})
            
    def delete_all_bookmarks(self, discord_id: int):
        with self.conn:
            self.c.execute(f"""DELETE FROM bookmarks WHERE discord_id = :discord_id""", {"discord_id": discord_id})
            
    def delete_all_bookmarks_by_type(self, discord_id: int, type: BookmarkTypes):
        with self.conn:
            self.c.execute(f"""DELETE FROM bookmarks WHERE discord_id = :discord_id AND type = :type""", {"discord_id": discord_id, "type": type.value})

    
if __name__ == "__main__":
     db = sqlite3.connect(":memory:")
     cm = BookmarkManager(db)
     
     cm.create_bookmark(69, BookmarkTypes.ACCOUNTS, 1)
     cm.create_bookmark(69, BookmarkTypes.ACCOUNTS, 564)
     cm.create_bookmark(69, BookmarkTypes.ROOMS, 512464)
     print("Accounts", cm.get_bookmarks(69, BookmarkTypes.ACCOUNTS))
     print("Rooms", cm.get_bookmarks(69, BookmarkTypes.ROOMS))
     cm.delete_all_bookmarks_by_type(69, BookmarkTypes.ACCOUNTS)
     print("Accounts", cm.get_bookmarks(69, BookmarkTypes.ACCOUNTS))
     print("Rooms", cm.get_bookmarks(69, BookmarkTypes.ROOMS))