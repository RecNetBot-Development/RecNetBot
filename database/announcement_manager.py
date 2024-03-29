import sqlite3
import time
from dataclasses import dataclass
from typing import Optional
from sqlite3 import Connection
from enum import Enum

@dataclass
class Announcement:
    id: int
    title: str
    unix_timestamp: int
    description: str
    image_url: str
    expiration_timestamp: int
    

class AnnouncementManager():
    def __init__(self, database: Connection):
        self.conn = database
        self.c = self.conn.cursor()
        self.create_table()
        
    def create_table(self):
        """
        Creates the announcements table
            - id integer: id of the announcement
            - unix_timestamp integer: timestamp of when the announcement was published
            - title string: title of the announcement
            - description string: description of the announcement
            - image_url string: image url of the announcement
            - expiration_timestamp integer: timestamp of when the announcement should be discarded
        """
        
        self.c.execute(f"""CREATE TABLE IF NOT EXISTS announcements (id integer, unix_timestamp integer, title string, description string, image_url string, expiration_timestamp integer, PRIMARY KEY (id))""")

        """
        Creates the announcement_history table
            - discord_id integer: discord id of user
            - latest_announcement_id integer: id of the latest announcement they've seen
        """
        
        self.c.execute(f"""CREATE TABLE IF NOT EXISTS announcement_history (discord_id integer, latest_announcement_id integer, PRIMARY KEY (discord_id))""")


    def get_latest_announcement(self) -> Optional[Announcement]:
        self.c.execute(f"""SELECT * FROM announcements ORDER BY id DESC LIMIT 1""")
        data = self.c.fetchone()
        if not data: return None
        return Announcement(*data)

    def get_history(self, discord_id: int) -> Optional[str]:
        self.c.execute(f"""SELECT * FROM announcement_history WHERE discord_id = :discord_id""", {"discord_id": discord_id})
        data = self.c.fetchall()
        if not data: return []
        return data
    
    def get_how_many_read_latest(self) -> Optional[str]:
        announcement = self.get_latest_announcement()

        self.c.execute(f"""SELECT * FROM announcement_history WHERE latest_announcement_id = :announcement_id""", {"announcement_id": announcement.id})
        data = self.c.fetchall()
        if not data: return 0
        return len(data)

    def get_unread_announcements(self, discord_id: int) -> Optional[Announcement]:
        self.c.execute(f"""SELECT announcements.* FROM announcements INNER JOIN announcement_history ON announcements.id > announcement_history.latest_announcement_id AND announcement_history.discord_id = :discord_id ORDER BY announcements.id DESC""", {"discord_id": discord_id})
        data = self.c.fetchall()
        announcements = []
        if data: 
            for i in data:
                announcements.append(Announcement(*i))
        else:
            history = self.get_history(discord_id)
            if history: return []
            announcements.append(self.get_latest_announcement())
            if not announcements: return []

        # Mark as read
        with self.conn:
            self.c.execute(f"""REPLACE INTO announcement_history VALUES (:discord_id, :id)
                           """, 
                           {"discord_id": discord_id, "id": announcements[0].id})

        return announcements
    
    def create_announcement(self, title: str, description: str, image_url: str = "", expiration_timestamp: int = 0):
        with self.conn:
            self.c.execute(f"""INSERT INTO announcements VALUES (:id, :title, :unix_timestamp, :description, :image_url, :expiration_timestamp)""", {"id": None, "title": title, "unix_timestamp": int(time.time()), "description": description, "image_url": image_url, "expiration_timestamp": expiration_timestamp})
        
    def delete_announcement(self, id: int):
        with self.conn:
            self.c.execute(f"""DELETE FROM announcements WHERE id = :id""", {"id": id})

    
if __name__ == "__main__":
     db = sqlite3.connect(":memory:")
     cm = AnnouncementManager(db)

     cm.create_announcement("hello world", "whas gooood", "google.com")
     print(cm.get_unread_announcement(1))
     print(cm.get_unread_announcement(1))
     