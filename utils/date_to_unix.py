import time
from datetime import datetime

def date_to_unix(date: str) -> int:
    """
    Converts dates from RecNet to an unix timestamp, that can be used to show dates more elegantly.
    """
    if "." in date: 
        date = date.split(".")[0]
    else:  # Cuz apparently not all dates have the damn dot!!
        date = date.split("Z")[0]
        
    return int(time.mktime(datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").timetuple()))  # Return UNIX timestamp as an int to get rid of any decimals