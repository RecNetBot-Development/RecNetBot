from dataclasses import dataclass
import sqlite3
from typing import Optional
from sqlite3 import Connection

@dataclass
class Connections:
    discord_id: int = None
    rr_id: int = None
    status: int = None # (0/1/2) - (done / pending cheer / pending uncheer)

class ConnectionManager():
    def __init__(self, database: Connection):
        self.conn = database
        self.c = self.conn.cursor()
        self.create_table()
        
    def create_table(self):
        """
        Creates the linked_accounts table
            - discord_id integer: a Discord account's id
            - rr_id integer: a Rec Room account's id
            - status integer: (0/1/2) - (done / pending cheer / pending uncheer)
        """
        self.c.execute(f"""CREATE TABLE IF NOT EXISTS linked_accounts (discord_id integer PRIMARY KEY, rr_id integer, status integer)""")
        
    def get_discord_connection(self, discord_id: int, require_done: bool = True) -> Optional[Connections]:
        self.c.execute(f"""SELECT * FROM linked_accounts WHERE discord_id = :discord_id {'AND status = 0' if require_done else ''}""", {"discord_id": discord_id})
        data = self.c.fetchone()
        if not data: return
        return Connections(*data)
    
    def get_rec_room_connection(self, rr_id: int, require_done: bool = True) -> Optional[Connections]:
        self.c.execute(f"""SELECT * FROM linked_accounts WHERE rr_id = :rr_id {'AND status = 0' if require_done else ''}""", {"rr_id": rr_id})
        data = self.c.fetchone()
        if not data: return
        return Connections(*data)
    
    def get_connection_status(self, discord_id: int) -> int:
        self.c.execute(f"""SELECT * FROM linked_accounts WHERE discord_id = :discord_id""", {"discord_id": discord_id})
        data = self.c.fetchone()
        if not data: return -1
        return data[2]
    
    def create_connection(self, discord_id: int, rr_id: int, status: int):
        with self.conn:
            self.c.execute(f"""INSERT OR IGNORE INTO linked_accounts VALUES (:discord_id, :rr_id, :status)""", {"discord_id": discord_id, "rr_id": rr_id, "status": status})
            
    def update_connection(self, discord_id: int, rr_id: int, status: int):
        with self.conn:
            self.c.execute(f"""UPDATE linked_accounts SET rr_id = :rr_id, status = :status WHERE discord_id = :discord_id""", {"rr_id": rr_id, "discord_id": discord_id, "status": status})
            
    def delete_connection(self, discord_id: int):
        with self.conn:
            self.c.execute(f"""DELETE FROM linked_accounts WHERE discord_id = :discord_id""", {"discord_id": discord_id})
       
if __name__ == "__main__":
     db = sqlite3.connect(":memory:")
     cm = ConnectionManager(db)
     
     cm.create_connection(69, 420)
     print(cm.get_discord_connection(69))