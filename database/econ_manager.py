import sqlite3
import json
from typing import Optional
from sqlite3 import Connection
from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from economy import get_item, load_items

ITEMS: list = load_items()

@dataclass
class Profile:
    discord_id: int
    tokens: int
    join_date: int

class EconManager():
    def __init__(self, database: Connection):
        self.conn = database
        self.c = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """
        Creates the econ tables
        """

        """
        econ_profile
        - discord_id integer: a Discord account's id
        - tokens: the user's balance
        - join_date: the user's first time playing economy
        """
        self.c.execute(f"""CREATE TABLE IF NOT EXISTS econ_profile (discord_id integer PRIMARY KEY, tokens integer, join_date integer)""")

        """
        econ_inventory
        - discord_id integer: a Discord account's id
        - item_id: an item's ID
        - amount: the amount the user has
        """
        self.c.execute(f"""CREATE TABLE IF NOT EXISTS econ_inventory (discord_id integer, item_id integer, amount, PRIMARY KEY (discord_id, item_id))""")

        """
        econ_penalty
        - discord_id integer: a Discord account's id
        - penalty integer: the user's penalty
        """
        self.c.execute(f"""CREATE TABLE IF NOT EXISTS econ_penalty (discord_id integer PRIMARY KEY, penalty integer)""")

    def get_profile(self, discord_id: int) -> Optional[Profile]:
        """
        Fetch a user's economy profile
        """
        self.c.execute(f"""SELECT * FROM econ_profile WHERE discord_id = :discord_id""", 
                       {"discord_id": discord_id})
        data = self.c.fetchone()
        if data: 
            profile = Profile(*data)
            return profile
        return None
    
    def get_inventory(self, discord_id: int) -> Optional[dict]:
        """
        Fetch a user's inventory with data + amount
        """
        self.c.execute(f"""SELECT item_id, amount FROM econ_inventory WHERE discord_id = :discord_id""", 
                       {"discord_id": discord_id})
        data = self.c.fetchall()
        if data: 
            # Form the data
            inventory = []
            for i in data:
                item = get_item(item_id=i[0])
                inventory.append(
                    {
                        "item": item,
                        "amount": i[1]
                    }
                )
            return inventory
            
        return []
    
    def get_item_amount(self, discord_id: int, item_id: int) -> int:
        """
        Get the amount of items a user has based on its item ID
        """
        self.c.execute(f"""SELECT amount FROM econ_inventory WHERE discord_id = :discord_id AND item_id = :item_id""", 
                       {"discord_id": discord_id, "item_id": item_id})
        data = self.c.fetchone()
        if data: return data[0]
        return 0
    
    def add_item(self, discord_id: int, item_id: int, amount: int) -> None:
        """
        Add an item to a user's inventory
        """
        with self.conn:
            self.c.execute(
                f"""INSERT INTO econ_inventory (discord_id, item_id, amount) 
                    VALUES (:discord_id, :item_id, :amount)
                    ON CONFLICT(discord_id, item_id)
                    DO UPDATE SET amount = amount + :amount
                """, 
                {"amount": amount, "discord_id": discord_id, "item_id": item_id}
            )

    def add_tokens(self, discord_id: int, tokens: int) -> None:
        """
        Add tokens to user's balance
        """
        with self.conn:
            self.c.execute(
                f"""UPDATE econ_profile SET tokens = tokens + :tokens WHERE discord_id = :discord_id 
                """, 
                {"tokens": tokens, "discord_id": discord_id}
            )

    def set_penalty(self, discord_id: int, minutes: int) -> None:
        """
        Set penalty
        """
        seconds = 60 * minutes
        with self.conn:
            self.c.execute(
                f"""INSERT INTO econ_penalty (discord_id, penalty) 
                    VALUES (:discord_id, :penalty)
                    ON CONFLICT(discord_id)
                    DO UPDATE SET penalty = :penalty
                """, 
                {"discord_id": discord_id, "penalty": int(datetime.now().timestamp() + seconds)}
            )

    def get_penalty(self, discord_id: int) -> None:
        """
        Get penalty
        """
        self.c.execute(f"""SELECT penalty FROM econ_penalty WHERE discord_id = :discord_id""", 
                       {"discord_id": discord_id})
        data = self.c.fetchone()
        if data: return data[0]
        return 0
    
    def create_profile(self, discord_id: int):
        """
        Create an economy profile for a Discordian
        """
        with self.conn:
            self.c.execute(f"""REPLACE INTO econ_profile VALUES (:discord_id, :tokens, :join_date)""", 
                           {"discord_id": discord_id, "tokens": 0, "join_date": int(datetime.now().timestamp())})

if __name__ == "__main__":
    db = sqlite3.connect(":memory:")
    cm = EconManager(db)

    cm.set_penalty(1337, 5)
    print(cm.get_penalty(1337))

    """
    adapt = adapt_box_instance(instance)
    print(adapt)
    convert = convert_box_instance(adapt)
    print(convert)
    """

    

    """
    print(cm.get_latest_read(1))
    cm.mark_as_read(1, 32, 45)
    print(cm.get_latest_read(1))
    """

    """
    cm = BookmarkManager(db)
    
    cm.create_bookmark(69, BookmarkTypes.ACCOUNTS, 1)
    cm.create_bookmark(69, BookmarkTypes.ACCOUNTS, 564)
    cm.create_bookmark(69, BookmarkTypes.ROOMS, 512464)
    print("Accounts", cm.get_bookmarks(69, BookmarkTypes.ACCOUNTS))
    print("Rooms", cm.get_bookmarks(69, BookmarkTypes.ROOMS))
    cm.delete_all_bookmarks_by_type(69, BookmarkTypes.ACCOUNTS)
    print("Accounts", cm.get_bookmarks(69, BookmarkTypes.ACCOUNTS))
    print("Rooms", cm.get_bookmarks(69, BookmarkTypes.ROOMS))
    """