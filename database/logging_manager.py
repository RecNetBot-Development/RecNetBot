import sqlite3
import aiosqlite
from aiosqlite import Connection
import datetime
import hashlib

class LoggingManager():
    def __init__(self, database: Connection = None):
        self.conn = database
        
    async def init(self, database: Connection):
        self.conn = database
        await self.create_table()
        return self

    async def create_table(self):
        """
        Creates the logging table
            - discord_hash text: a Discord account's ID as sha256
            - command_mention text: a ran command's mention
            - timestamp integer: when was this command ran
        """
        await self.conn.execute(f"""CREATE TABLE IF NOT EXISTS logging (discord_hash text, command_mention text, timestamp integer)""")
        await self.conn.commit()

    async def get_total_command_count(self) -> int:
        async with await self.conn.execute("SELECT COUNT(1) FROM logging") as cursor:
            data = await cursor.fetchone()
        if not data: return 0
        return data[0]
    
    async def get_command_count(self, command_mention: str) -> int:
        async with await self.conn.execute(
            f"""SELECT COUNT(1) FROM logging WHERE command_mention = :command_mention""", 
            {"command_mention": command_mention}
        ) as cursor:
            data = await cursor.fetchone()
        if not data: return 0
        return data[0]
    
    async def get_first_entry_timestamp(self) -> int:
        async with await self.conn.execute(
            f"""SELECT timestamp FROM logging order by timestamp asc limit 1"""
        ) as cursor:
            data = await cursor.fetchall()
        if not data: return 0
        return data[0][0]
    
    async def get_ran_commands_by_user_after_timestamp(self, timestamp_after: int, discord_id: id) -> dict:
        discord_hash = self.hash_discord_id(discord_id)

        async with await self.conn.execute(
            f"""
            SELECT * FROM logging
            WHERE timestamp >= :timestamp_after
            AND discord_hash = :discord_hash
            """, 
            {"timestamp_after": timestamp_after, "discord_hash": discord_hash}
        ) as cursor:
            data = await cursor.fetchall()
        if not data: return {}

        log = {"specific": {}, "total_usage": 0, "first_date": data[0][2]}
        for i in data:
            cmd_mention, timestamp = i[1], i[2]

            if not cmd_mention.startswith("other:"):
                cmd_mention = cmd_mention.split("<")[1].split(":")[0]

            if cmd_mention in log["specific"]:
                log["specific"][cmd_mention].append(timestamp)
            else:
                log["specific"][cmd_mention] = [timestamp]

            log["total_usage"] += 1

        return log

    async def get_ran_commands_after_timestamp(self, timestamp_after: int) -> dict:
        async with await self.conn.execute(
            f"""
            SELECT * FROM logging
            WHERE timestamp >= :timestamp_after 
            """, 
            {"timestamp_after": timestamp_after}
        ) as cursor:
            data = await cursor.fetchall()
        if not data: return {}

        log = {}
        for i in data:
            user_hex, cmd_mention, timestamp = i[0], i[1], i[2]

            if ":" not in cmd_mention: continue

            if not cmd_mention.startswith("other:"):
                cmd_mention = cmd_mention.split("<")[1].split(":")[0]

            if user_hex in log:
                if cmd_mention in log[user_hex]["specific"]:
                    log[user_hex]["specific"][cmd_mention].append(timestamp)
                else:
                    log[user_hex]["specific"][cmd_mention] = [timestamp]

                log[user_hex]["total_usage"] += 1
            else:
                log[user_hex] = {"specific": {cmd_mention: [timestamp]}, "total_usage": 1}

        return log
    
    async def log_command_usage(self, discord_id: int, command_mention: str):
        """
        Logs a command being ran. Keeps the user anonymous.
        """

        # Hash user's discord id
        discord_hash = self.hash_discord_id(discord_id)

        # Get current timestamp
        timestamp = int(datetime.datetime.now().timestamp())

        await self.conn.execute(
            f"""INSERT INTO logging VALUES (:discord_hash, :command_mention, :timestamp)""", 
            {"discord_hash": discord_hash, "command_mention": command_mention, "timestamp": timestamp}
        )
        await self.conn.commit()
            
    def hash_discord_id(self, discord_id: int) -> str:
        # Hash user's discord id
        m = hashlib.sha256()
        m.update(str.encode(str(discord_id)))
        return m.hexdigest()
    
    async def close(self):
        await self.conn.close()

import asyncio

async def main():
    db = await aiosqlite.connect("test.db")
    cm = LoggingManager()
    await cm.init(db)
    
    print(await cm.get_total_command_count())
    print(await cm.get_command_count("</logs:1214848908623224833>"))

if __name__ == "__main__":
    asyncio.run(main())
    
     
    

    
