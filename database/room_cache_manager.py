from dataclasses import dataclass
import sqlite3
import asyncio
import time
from typing import Optional
from sqlite3 import Connection
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
    def __init__(self, database: Connection):
        self.conn = database
        self.c = self.conn.cursor()
        self.create_table()
        
    def create_table(self):
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
        
        sqlite3.register_adapter(RoomStats, adapt_room_stats)
        sqlite3.register_converter('RoomStats', convert_room_stats)
        self.c.execute(f"""CREATE TABLE IF NOT EXISTS room_cache (discord_id integer, room_id integer, room_stats RoomStats, PRIMARY KEY (discord_id, room_id))""")
        
    def get_cached_stats(self, discord_id: int, room_id: int) -> Optional[RoomStats]:
        self.c.execute(f"""SELECT * FROM room_cache WHERE discord_id = :discord_id AND room_id = :room_id""", 
                       {"discord_id": discord_id, "room_id": room_id})
        data = self.c.fetchone()
        if data: return data[2]
        return None
    
    def cache_stats(self, discord_id: int, room_id: int, room: Room):
        stats = self.create_stats_dataclass(room)
        
        with self.conn:
            self.c.execute(f"""REPLACE INTO room_cache VALUES (:discord_id, :room_id, :room_stats)
                           """, 
                           {"discord_id": discord_id, "room_id": room_id, "room_stats": stats})
            
    def delete_cached_stats(self, discord_id: int):
        with self.conn:
            self.c.execute(f"""DELETE FROM room_cache WHERE discord_id = :discord_id""", {"discord_id": discord_id})
            
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
       
       
async def main():
    db = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
    cm = RoomCacheManager(db)
    
    RecNet = Client()
    room = await RecNet.rooms.get("RecCenter")
    
    discord_id = 69
    room_id = 420
    
    cm.cache_stats(discord_id, room_id, room)
    print(cm.get_cached_stats(2, 4))
    
    db.close()
    await RecNet.close()

  

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())     