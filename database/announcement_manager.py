import time
import asyncio
import aiosqlite
from dataclasses import dataclass
from typing import Optional
from aiosqlite import Connection

@dataclass
class Announcement:
    id: int
    title: str
    unix_timestamp: int
    description: str
    image_url: str
    expiration_timestamp: int
    

class AnnouncementManager():
    def __init__(self, database: Connection = None):
        self.conn = database

    async def init(self, database: Connection):
        self.conn = database
        await self.create_table()
        return self

    async def create_table(self):
        """
        Creates the announcements table
            - id integer: id of the announcement
            - unix_timestamp integer: timestamp of when the announcement was published
            - title string: title of the announcement
            - description string: description of the announcement
            - image_url string: image url of the announcement
            - expiration_timestamp integer: timestamp of when the announcement should be discarded
        """
        
        await self.conn.execute(f"""CREATE TABLE IF NOT EXISTS announcements (id integer, unix_timestamp integer, title string, description string, image_url string, expiration_timestamp integer, PRIMARY KEY (id))""")
        await self.conn.commit()

        """
        Creates the announcement_history table
            - discord_id integer: discord id of user
            - latest_announcement_id integer: id of the latest announcement they've seen
        """
        
        await self.conn.execute(f"""CREATE TABLE IF NOT EXISTS announcement_history (discord_id integer, latest_announcement_id integer, PRIMARY KEY (discord_id))""")
        await self.conn.commit()

    async def get_latest_announcement(self) -> Optional[Announcement]:
        async with await self.conn.execute(f"""SELECT * FROM announcements ORDER BY id DESC LIMIT 1""") as cursor:
            data = await cursor.fetchone()
        if not data: return None
        return Announcement(*data)

    async def get_history(self, discord_id: int) -> Optional[str]:
        async with await self.conn.execute(f"""SELECT * FROM announcement_history WHERE discord_id = :discord_id""", {"discord_id": discord_id}) as cursor:
            data = await cursor.fetchall()
        if not data: return []
        return data
    
    async def get_how_many_read_latest(self) -> Optional[str]:
        announcement = await self.get_latest_announcement()

        async with await self.conn.execute(f"""SELECT * FROM announcement_history WHERE latest_announcement_id = :announcement_id""", {"announcement_id": announcement.id}) as cursor:
            data = await cursor.fetchall()
        if not data: return 0
        return len(data)

    async def get_unread_announcements(self, discord_id: int) -> Optional[Announcement]:
        async with await self.conn.execute(f"""SELECT announcements.* FROM announcements INNER JOIN announcement_history ON announcements.id > announcement_history.latest_announcement_id AND announcement_history.discord_id = :discord_id ORDER BY announcements.id DESC""", {"discord_id": discord_id}) as cursor:
            data = await cursor.fetchall()

        announcements = []
        if data: 
            for i in data:
                announcements.append(Announcement(*i))
        else:
            history = await self.get_history(discord_id)
            if history: return []
            latest_announcement = await self.get_latest_announcement()
            if not latest_announcement: return []
            announcements.append(latest_announcement)

        # Mark as read
        await self.conn.execute(f"""REPLACE INTO announcement_history VALUES (:discord_id, :id)
                        """, 
                        {"discord_id": discord_id, "id": announcements[0].id})
        await self.conn.commit()

        return announcements
    
    async def create_announcement(self, title: str, description: str, image_url: str = "", expiration_timestamp: int = 0):
        await self.conn.execute(f"""INSERT INTO announcements VALUES (:id, :title, :unix_timestamp, :description, :image_url, :expiration_timestamp)""", {"id": None, "title": title, "unix_timestamp": int(time.time()), "description": description, "image_url": image_url, "expiration_timestamp": expiration_timestamp})
        await self.conn.commit()

    async def delete_announcement(self, id: int):
        await self.conn.execute(f"""DELETE FROM announcements WHERE id = :id""", {"id": id})
        await self.conn.commit()

    async def close(self):
        await self.conn.close()


async def main():
    db = await aiosqlite.connect(":memory:")
    cm = AnnouncementManager(db)
    await cm.init()

    await cm.create_announcement("hello world", "whas gooood", "google.com")
    print(await cm.get_latest_announcement())

    await cm.close()

if __name__ == "__main__":
    asyncio.run(main())
     