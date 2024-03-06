from dataclasses import dataclass
import sqlite3
import asyncio
from typing import Optional, List
from sqlite3 import Connection
from enum import Enum

@dataclass
class FeedTypes(Enum):
    IMAGE = 1
    ROOM = 2
    EVENT = 3

@dataclass
class FeedData:
    discord_id: int
    channel_id: int
    type: FeedTypes
    rr_id: int

class FeedManager():
    def __init__(self, database: Connection):
        self.conn = database
        self.c = self.conn.cursor()
        self.create_table()
        
    def create_table(self):
        """
        Creates the feed table
            - id int
            - discord_id int
            - channel_id int
            - type TypeEnum(image, room, event)
            - rr_id int
                        """

        self.c.execute(f"""CREATE TABLE IF NOT EXISTS feed (id integer, discord_id integer, channel_id integer, type integer, rr_id integer, PRIMARY KEY (id, channel_id, type))""")

        """
        Creates the feed history table
            - feed_id int
            - creation_unix int
                        """

        self.c.execute(f"""CREATE TABLE IF NOT EXISTS feed_history (feed_id integer, creation_unix integer, PRIMARY KEY (feed_id))""")
        
    def get_feeds_in_channel(self, channel_id: int) -> List[FeedData]:
        self.c.execute(f"""SELECT * FROM feed WHERE channel_id = :channel_id""", 
                       {"channel_id": channel_id})
        data = self.c.fetchall()
        return self.raw_to_dataclasses(data)
    
    def get_all_feeds(self) -> List[FeedData]:
        self.c.execute(f"""SELECT * FROM feed""")
        data = self.c.fetchall()
        return self.raw_to_dataclasses(data)
    
    def raw_to_dataclasses(self, data: list) -> List[FeedData]:
        # Turn database data into dataclasses
        dataclasses = [] 
        for i in data:
            feed = FeedData(*i)
            feed.type = FeedTypes(feed.type)
            dataclasses.append(feed)
        return dataclasses
    
    def update_history(self, feed_id: int, unix_timestamp: int):
        with self.conn:
            self.c.execute(f"""REPLACE INTO feed_history VALUES (:creation_unix) WHERE feed_id = :feed_id
                           """, 
                           {"feed_id": feed_id, "creation_unix": unix_timestamp})

    def create_feed(self, discord_id: int, channel_id: int, type: FeedTypes, rr_id: int):
        with self.conn:
            self.c.execute(f"""REPLACE INTO feed VALUES (:discord_id, :channel_id, :type, :rr_id)
                           """, 
                           {"discord_id": discord_id, "channel_id": channel_id, "type": type.value, "rr_id": rr_id})
            
    def delete_feed(self, channel_id: int, type: int):
        with self.conn:
            self.c.execute(f"""DELETE FROM feed WHERE channel_id = :channel_id AND type = :type""", {"channel_id": channel_id, "type": type.value})

       
async def main():
    db = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
    cm = FeedManager(db)
    
    discord_id = 69
    channel_id = 420
    type = FeedTypes.ROOM
    rr_id = 2141244

    cm.create_feed(discord_id, channel_id, type, rr_id)
    cm.create_feed(discord_id, channel_id+2, type, rr_id)

    print(cm.get_all_feeds())

    cm.delete_feed(channel_id, type)

    print(cm.get_all_feeds())
    
    db.close()

  

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())     