from dataclasses import dataclass
import asyncio
import time
import sqlite3
import aiosqlite
from aiosqlite import Connection
from typing import Optional
from recnetpy.dataclasses.room import Room
from recnetpy import Client

@dataclass
class RoomStats:
    room_id: int
    cheers: int
    favorites: int
    visitors: int
    visits: int
    cached_timestamp: int
    

class RoomCacheManager():
    def __init__(self, database: Connection = None):
        self.conn = database
        
    async def init(self, database: Connection):
        self.conn = database
        await self.create_table()
        return self

    async def create_table(self):
        """
        Creates the room_cache table
            - discord_id integer: a Discord account's id
            - stats RoomStats: a room's cached stats
        """
        
        def adapt_room_stats(stats: RoomStats) -> str:
            return f"{stats.room_id};{stats.cheers};{stats.favorites};{stats.visitors};{stats.visits};{stats.cached_timestamp}".encode("utf-8")
            
        def convert_room_stats(str_stats: str) -> RoomStats:
            room_id, cheers, favorites, visitors, visits, cached_timestamp = list(map(int, str_stats.split(b";")))
            return RoomStats(room_id, cheers, favorites, visitors, visits, cached_timestamp)
        
        aiosqlite.register_adapter(RoomStats, adapt_room_stats)
        aiosqlite.register_converter('RoomStats', convert_room_stats)

        await self.conn.execute(f"""CREATE TABLE IF NOT EXISTS room_cache (discord_id integer, room_id integer, room_stats RoomStats, PRIMARY KEY (discord_id, room_id))""")
        await self.conn.commit()

    async def get_cached_stats(self, discord_id: int, room_id: int) -> Optional[RoomStats]:
        async with await self.conn.execute(f"""SELECT * FROM room_cache WHERE discord_id = :discord_id AND room_id = :room_id""", 
                    {"discord_id": discord_id, "room_id": room_id}) as cursor:
            data = await cursor.fetchone()
        if data: return data[2]
        return None
    
    async def cache_stats(self, discord_id: int, room_id: int, room: Room):
        stats = self.create_stats_dataclass(room)
        
        await self.conn.execute(f"""REPLACE INTO room_cache VALUES (:discord_id, :room_id, :room_stats)
                        """, 
                        {"discord_id": discord_id, "room_id": room_id, "room_stats": stats})
        await self.conn.commit()

    async def delete_cached_stats(self, discord_id: int):
        await self.conn.execute(f"""DELETE FROM room_cache WHERE discord_id = :discord_id""", {"discord_id": discord_id})
        await self.conn.commit()

    def create_stats_dataclass(self, room: Room) -> RoomStats:
        """
        Creates a room stat dataclass that gets saved to the database
        """
        
        return RoomStats(
            room.id,
            room.cheer_count,
            room.favorite_count,
            room.visitor_count,
            room.visit_count,
            int(time.time())
        )
    
    async def close(self):
        await self.conn.close()
       
       
async def main():
    db = await aiosqlite.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
    cm = RoomCacheManager(db)
    await cm.init()

    RecNet = Client(token)
    room = await RecNet.rooms.get("RecCenter")
    
    discord_id = 69
    room_id = 420
    
    await cm.cache_stats(discord_id, room_id, room)
    await cm.cache_stats(1, 2, room)
    await cm.cache_stats(4, 5, room)
    print(await cm.get_cached_stats(discord_id, room_id))
    print(await cm.get_cached_stats(4, 5))
    await cm.delete_cached_stats(69)
    print(await cm.get_cached_stats(discord_id, room_id))

    
    await db.close()
    await RecNet.close()

  

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())     