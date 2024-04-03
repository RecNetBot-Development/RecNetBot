from dataclasses import dataclass
import aiosqlite
import sqlite3
from typing import Optional
from aiosqlite import Connection
from recnetpy.dataclasses.account import Account
from recnetpy import Client

@dataclass
class Connections:
    discord_id: int = None
    rr_id: int = None

class ConnectionManager():
    def __init__(self, database: Connection = None):
        self.conn = database
        
    async def init(self, database: Connection):
        self.conn = database
        await self.create_table()
        return self

    async def create_table(self):
        """
        Creates the linked_accounts table
            - discord_id integer: a Discord account's id
            - rr_id integer: a Rec Room account's id
        """
        await self.conn.execute(f"""CREATE TABLE IF NOT EXISTS linked_accounts (discord_id integer PRIMARY KEY, rr_id integer)""")
        await self.conn.execute(f"""CREATE INDEX IF NOT EXISTS idx_linked_accounts_discord ON linked_accounts (discord_id)""")
        await self.conn.commit()

    async def get_discord_connection(self, discord_id: int) -> Optional[int]:
        """Returns RR ID if connection found via Discord ID"""
        async with await self.conn.execute(f"""SELECT rr_id FROM linked_accounts WHERE discord_id = :discord_id""", {"discord_id": discord_id}) as cursor:
            data = await cursor.fetchone()
        if not data: return None
        return data[0]
    
    async def get_rec_room_connection(self, rr_id: int) -> Optional[int]:
        """Return Discord ID if connection found via RR ID"""
        async with await self.conn.execute(f"""SELECT discord_id FROM linked_accounts WHERE rr_id = :rr_id""", {"rr_id": rr_id}) as cursor:
            data = await cursor.fetchone()
        if not data: return None
        return data[0]
    
    async def get_connection_count(self) -> int:
        async with await self.conn.execute("SELECT COUNT(1) FROM linked_accounts") as cursor:
            data = await cursor.fetchone()
        if not data: return 0
        return data[0]
    
    async def create_connection(self, discord_id: int, rr_id: int):
        await self.conn.execute(f"""INSERT OR IGNORE INTO linked_accounts VALUES (:discord_id, :rr_id)""", {"discord_id": discord_id, "rr_id": rr_id})
        await self.conn.commit()

    async def update_connection(self, discord_id: int, rr_id: int):
        await self.conn.execute(f"""UPDATE linked_accounts SET rr_id = :rr_id WHERE discord_id = :discord_id""", {"rr_id": rr_id, "discord_id": discord_id})
        await self.conn.commit()

    async def delete_connection(self, discord_id: int):
        await self.conn.execute(f"""DELETE FROM linked_accounts WHERE discord_id = :discord_id""", {"discord_id": discord_id})
        await self.conn.commit()
        
    async def get_linked_account(self, RecNet: Client, discord_id: int) -> Optional[Account]:
        """
        Fetches the linked Rec Room account of a Discord account
        """
        rr_id = await self.get_discord_connection(discord_id)
        if not rr_id: return None
        account = await RecNet.accounts.fetch(rr_id)
        return account
    
    async def close(self):
        await self.conn.close()
    
import asyncio

async def main():
    db = await aiosqlite.connect("SEX.db")
    cm = ConnectionManager()
    await cm.init(db)
     
    await cm.create_connection(69, 420)
    print(await cm.get_discord_connection(69))

    await cm.close()

if __name__ == "__main__":
    asyncio.run(main())