from typing import Union
from .date_to_unix import date_to_unix

def unix_timestamp(timestamp: int, format=str) -> str:
    """
    Generates a Discord supported unix timestamp
    """
    
    allowed_formats = ["", "t", "T", "d", "D", "f", "F", "R"]
    if format not in allowed_formats:
        format = "f"
    format = f":{format}"
    
    if isinstance(timestamp, int):
        return f"<t:{timestamp}{format}>"
    elif isinstance(timestamp, str):
        return f"<t:{date_to_unix(timestamp)}{format}>"
    else:
        return f"<t:{0}{format}>"