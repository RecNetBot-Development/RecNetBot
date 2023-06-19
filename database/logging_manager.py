from dataclasses import dataclass
import sqlite3
from typing import Optional
from sqlite3 import Connection
from recnetpy.dataclasses.account import Account
from recnetpy import Client
import datetime
import hashlib

class LoggingManager():
    def __init__(self, database: Connection):
        self.conn = database
        self.c = self.conn.cursor()
        self.create_table()
        
    def create_table(self):
        """
        Creates the logging table
            - discord_hash text: a Discord account's ID as sha256
            - command_mention text: a ran command's mention
            - timestamp integer: when was this command ran
        """
        self.c.execute(f"""CREATE TABLE IF NOT EXISTS logging (discord_hash text, command_mention text, timestamp integer)""")
    
    def get_total_command_count(self) -> int:
        self.c.execute(f"""SELECT * FROM logging""")
        data = self.c.fetchall()
        if not data: return 0
        return len(data)
    
    def get_command_count(self, command_mention: str) -> int:
        self.c.execute(
            f"""SELECT * FROM logging WHERE command_mention = :command_mention""", 
            {"command_mention": command_mention}
        )
        data = self.c.fetchall()
        if not data: return 0
        return len(data)
    
    def get_ran_commands_after_timestamp(self, timestamp_after: int) -> dict:
        self.c.execute(
            f"""
            SELECT * FROM logging
            WHERE timestamp > :timestamp_after 
            """, 
            {"timestamp_after": timestamp_after}
        )
        data = self.c.fetchall()
        if not data: return {}

        log = {}
        for i in data:
            user_hex, cmd_mention, timestamp = i[0], i[1], i[2]

            if user_hex in log:
                if cmd_mention in log[user_hex]["specific"]:
                    log[user_hex]["specific"][cmd_mention].append(timestamp)
                else:
                    log[user_hex]["specific"][cmd_mention] = [timestamp]

                log[user_hex]["total_usage"] += 1
            else:
                log[user_hex] = {"specific": {cmd_mention: [timestamp]}, "total_usage": 1}

        return log
    
    def log_command_usage(self, discord_id: int, command_mention: str):
        """
        Logs a command being ran. Keeps the user anonymous.
        """

        # Hash user's discord id
        m = hashlib.sha256()
        m.update(str.encode(str(discord_id)))
        discord_hash = m.hexdigest()

        # Get current timestamp
        timestamp = int(datetime.datetime.now().timestamp())

        with self.conn:
            self.c.execute(
                f"""INSERT INTO logging VALUES (:discord_hash, :command_mention, :timestamp)""", 
                {"discord_hash": discord_hash, "command_mention": command_mention, "timestamp": timestamp}
            )
            
    
if __name__ == "__main__":
    db = sqlite3.connect("test.db")
    cm = LoggingManager(db)
     
    for i in range(5):
        cm.log_command_usage(i+2, f"/hello{i}")

    logs = cm.get_ran_commands_after_timestamp(1686853570)
    print(logs)

    total = 0
    for i in logs.values():
        total += i["total_usage"]

    print(total / len(logs.keys()))
