from dataclasses import dataclass
import sqlite3
import asyncio
import aiosqlite
import time
from typing import Optional, List, Dict
from aiosqlite import Connection
from enum import Enum

@dataclass
class FeedTypes(Enum):
    IMAGE = 1
    ROOM = 2
    EVENT = 3

@dataclass
class FeedData:
    discord_id: int
    webhook_id: int
    type: FeedTypes
    rr_id: int

class FeedManager():
    def __init__(self, database: Connection = None):
        self.conn = database

    async def init(self, database: Connection):
        self.conn = database
        await self.create_table()
        return self
        
    async def create_table(self):
        """
        Creates the feed table
            - id int
            - creator_id int
            - server_id int
            - webhook_id int
            - channel_id int
            - type TypeEnum(image, room, event)
            - rr_id int
                        """

        await self.conn.execute(f"""CREATE TABLE IF NOT EXISTS feed (id integer primary key not null, creator_id integer, server_id integer, webhook_id integer, channel_id integer, type integer, rr_id integer)""")
        await self.conn.commit()

    async def get_feeds_based_on_type(self, type: FeedTypes) -> Dict[int, List[int]]:
        """
        Returns feeds based on type. Dict[rr_id, List[webhook_id]]
        """
        async with await self.conn.execute(f"""SELECT webhook_id, rr_id FROM feed WHERE type = :type""", 
                       {"type": type.value}) as cursor:
            data = await cursor.fetchall()

        feeds = {}
        for row in data:
            webhook_id = row[0]
            rr_id = row[1]

            # Append to feed
            if rr_id in feeds:
                feeds[rr_id].append(webhook_id)
                continue
            
            # Create a new one
            feeds[rr_id] = [webhook_id]

        return feeds
    
    async def get_all_rr_ids_based_on_type(self, type: FeedTypes) -> List[int]:
        """
        Returns RR ids of feeds with a specific type
        """
        async with await self.conn.execute(
            f"""SELECT rr_id FROM feed WHERE type = :type""", 
            {"type": type.value}
        ) as cursor:
            cursor.row_factory = lambda cursor, row: row[0]
            data = await cursor.fetchall()
        return list(set(data))
    
    async def get_channel_id_of_feed(self, webhook_id: int) -> Optional[int]:
        """
        Returns channel id of feed if found
        """
        async with await self.conn.execute(
            f"""SELECT channel_id FROM feed WHERE webhook_id = :webhook_id""", 
            {"webhook_id": webhook_id}
        ) as cursor:
            cursor.row_factory = lambda cursor, row: row[0]
            data = await cursor.fetchone()
        return data

    async def get_feeds_in_server(self, server_id: int) -> Optional[List]:
        """
        Returns feeds in a server
        """
        async with await self.conn.execute(
            f"""SELECT server_id, webhook_id, channel_id, id, rr_id FROM feed WHERE server_id = :server_id""", 
            {"server_id": server_id}
        ) as cursor:
            cursor.row_factory = lambda cursor, row: {"server_id": row[0], "webhook_id": row[1], "channel_id": row[2], "id": row[3], "rr_id": row[4]}
            data = await cursor.fetchall()
        return data
    
    async def get_feed_count_by_user(self, creator_id: int) -> Optional[int]:
        """
        Returns amount of feeds made by a user
        """
        async with await self.conn.execute(
            f"""SELECT COUNT(1) FROM feed WHERE creator_id = :creator_id""", 
            {"creator_id": creator_id}
        ) as cursor:
            cursor.row_factory = lambda cursor, row: row[0]
            data = await cursor.fetchone()
        return data
    
    async def get_feeds_by_user(self, creator_id: int) -> Optional[List]:
        """
        Returns feeds made by a user
        """
        async with await self.conn.execute(
            f"""SELECT server_id, webhook_id, channel_id, id, rr_id FROM feed WHERE creator_id = :creator_id""", 
            {"creator_id": creator_id}
        ) as cursor:
            cursor.row_factory = lambda cursor, row: {"server_id": row[0], "webhook_id": row[1], "channel_id": row[2], "id": row[3], "rr_id": row[4]}
            data = await cursor.fetchall()
        return data
    
    async def get_feed_rr_ids_in_channel(self, channel_id: int) -> Optional[int]:
        """
        Returns feed rr ids in channel
        """
        async with await self.conn.execute(
            f"""SELECT rr_id FROM feed WHERE channel_id = :channel_id""", 
            {"channel_id": channel_id}
        ) as cursor:
            cursor.row_factory = lambda cursor, row: row[0]
            data = await cursor.fetchall()
        return data

    def raw_to_dataclasses(self, data: list) -> List[FeedData]:
        # Turn database data into dataclasses
        dataclasses = [] 
        for i in data:
            feed = FeedData(*i)
            feed.type = FeedTypes(feed.type)
            dataclasses.append(feed)
        return dataclasses

    async def create_feed(self, creator_id: int, server_id: int, webhook_id: int, channel_id: int, type: FeedTypes, rr_id: int):
        await self.conn.execute(
            f"""INSERT INTO feed VALUES (NULL, :creator_id, :server_id, :webhook_id, :channel_id, :type, :rr_id)""", 
            {"creator_id": creator_id, "server_id": server_id, "webhook_id": webhook_id, "channel_id": channel_id, "type": type.value, "rr_id": rr_id})
        await self.conn.commit()

    async def delete_feed_with_id(self, feed_id: int):
        await self.conn.execute(f"""DELETE FROM feed WHERE id = :id""", {"id": feed_id})
        await self.conn.commit()

    async def delete_feed_with_webhook_id(self, webhook_id: int):
        await self.conn.execute(f"""DELETE FROM feed WHERE webhook_id = :webhook_id""", {"webhook_id": webhook_id})
        await self.conn.commit()

    async def close(self):
        await self.conn.close()
       
async def main():
    db = await aiosqlite.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
    cm = FeedManager()
    await cm.init(db)
    
    await cm.create_feed(1, 1, 1, FeedTypes.IMAGE, 1)
    print(await cm.get_channel_id_of_feed(1))
    
    await db.close()

  

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())     