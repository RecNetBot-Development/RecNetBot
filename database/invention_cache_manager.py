from dataclasses import dataclass
import sqlite3
import aiosqlite
import asyncio
import time
from typing import Optional
from aiosqlite import Connection
from recnetpy.dataclasses.invention import Invention
from recnetpy import Client

@dataclass
class InventionStats:
    invention_id: int
    num_used_in_room: int
    num_downloads: int
    cheer_count: int
    cached_timestamp: int
    

class InventionCacheManager():
    def __init__(self, database: Connection):
        self.conn = database

    async def init(self):
        await self.create_table()
        
    async def create_table(self):
        """
        Creates the invention_cache table
            - discord_id integer: a Discord account's id
            - stats InventionStats: an invention's cached stats
        """
        
        def adapt_invention_stats(stats: InventionStats) -> str:
            return f"{stats.invention_id};{stats.num_used_in_room};{stats.num_downloads};{stats.cheer_count};{stats.cached_timestamp}".encode("utf-8")
            
        def convert_invention_stats(str_stats: str) -> InventionStats:
            invention_id, num_used_in_room, num_downloads, cheer_count, cached_timestamp = list(map(int, str_stats.split(b";")))
            return InventionStats(invention_id, num_used_in_room, num_downloads, cheer_count, cached_timestamp)
        
        aiosqlite.register_adapter(InventionStats, adapt_invention_stats)
        aiosqlite.register_converter('InventionStats', convert_invention_stats)
        await self.conn.execute(f"""CREATE TABLE IF NOT EXISTS invention_cache (discord_id integer, invention_id integer, invention_stats InventionStats, PRIMARY KEY (discord_id, invention_id))""")
        await self.conn.commit()

    async def get_cached_stats(self, discord_id: int, invention_id: int) -> Optional[InventionStats]:
        async with await self.conn.execute(f"""SELECT * FROM invention_cache WHERE discord_id = :discord_id AND invention_id = :invention_id""", 
                       {"discord_id": discord_id, "invention_id": invention_id}) as cursor:
            data = await cursor.fetchone()
        if data: return data[2]
        return None
    
    async def cache_stats(self, discord_id: int, invention_id: int, invention: Invention):
        stats = self.create_stats_dataclass(invention)
        
        await self.conn.execute(f"""REPLACE INTO invention_cache VALUES (:discord_id, :invention_id, :invention_stats)""", 
                           {"discord_id": discord_id, "invention_id": invention_id, "invention_stats": stats})
        await self.conn.commit()    
        
    async def delete_cached_stats(self, discord_id: int):
        await self.conn.execute(f"""DELETE FROM invention_cache WHERE discord_id = :discord_id""", {"discord_id": discord_id})
        await self.conn.commit()

    def create_stats_dataclass(self, invention: Invention) -> InventionStats:
        """
        Creates an invention stat dataclass that gets saved to the database
        """
        
        return InventionStats(
            invention.id,
            invention.num_players_have_used_in_room,
            invention.num_downloads,
            invention.cheer_count,
            int(time.time())
        )
       
       
async def main():
    db = sqlite3.connect("testtest.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cm = InventionCacheManager(db)
    
    RecNet = Client()
    invention = await RecNet.inventions.fetch(3382028701921496594)
    
    discord_id = 69
    invention_id = 420
    
    cm.cache_stats(discord_id, invention_id, invention)
    print(cm.get_cached_stats(discord_id, invention_id))
    
    db.close()
    await RecNet.close()

  

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())     