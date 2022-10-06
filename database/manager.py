import sqlite3
from typing import List, Union
  
class DatabaseManager():
    """
    The database manager that handles all RNB's storage needs.
    """
    
    def __init__(self, database_name: str):
        self.con = sqlite3.connect(database_name)
        self.c = self.con.cursor()


    def insert(self, table: str, values: Union[list, tuple]):
        """Inserts a value into a table

        Args:
            table (str): The table's name
            values (dict): The values {"column": value}
        """
        
        placeholders = ', '.join(["?"]*len(values))
        command = f"INSERT OR IGNORE INTO {table} VALUES ({placeholders})"
        
        with self.con:
            self.c.execute(command, values)
    
        
    def select(self, table: str, column: str, value: Union[str, int, float]):
        """Selects a value from a table

        Args:
            table (str): The table's name
            column (str): The column's name
            value (Union[str, int, float]): What value is being looked for
        """
        command = f"SELECT * FROM {table} WHERE {column}=:{column}"
        query = {column: value}
        
        self.c.execute(command, query)
        
        
    def update(self, table: str, column: str, find: str, value: Union[str, int, float]):
        command = f"UPDATE {table} SET {column} = ? WHERE {}"
        with self.con:
            
        
        
    def create_table(self, table: str, columns: tuple):
        """Creates a table in the database

        Args:
            table (str): The table's name
            columns (tuple): Values within the table ("name text", "number integer")
        """
        formatted = str(columns).replace("'", "")
        command = f"CREATE TABLE IF NOT EXISTS {table} {formatted}"
        
        self.c.execute(command)
        
        
    def fetch_all(self) -> List:
        """Fetches everything from selected columns

        Returns:
            List: Found values
        """
        
        return self.c.fetchall()
    
    
    def fetch_one(self) -> Union[str, int, float]:
        """Fetches a single value from selected column

        Returns:
            List: Found values
        """
        
        return self.c.fetchone()
        
        
#manager = DatabaseManager("rnb.db")
#manager.create_table("linked_accounts", ("discord_id integer PRIMARY KEY", "rr_id integer"))
#manager.insert("linked_accounts", {"discord_id": 123, "rr_id": 456})
#manager.select("linked_accounts", "discord_id", 123)
#print(manager.fetch_all())






























