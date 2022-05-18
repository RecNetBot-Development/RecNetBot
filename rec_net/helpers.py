from multidict import MultiDict
import time
from datetime import datetime
def data_to_multidict(dictionary):
    multi = MultiDict()

    key = iter(dictionary)
    values = next(iter(dictionary.values()))

    for value in values:
        multi.add(key=key, value=value)

    return multi

def split_bulk(bulk: list):
    # Split bulk in groups of 150
    split = 150  
    split_points = [i for i in range(0, len(bulk), split)]
    split_groups = [bulk[ind:ind + split] for ind in split_points]

    return split_groups

# Converts dates from RecNet to an unix timestamp, that can be used to show dates more elegantly
def date_to_unix(date):
    # Split example: 2020-12-15T04:56:54 <-> .4519046Z
    if not date: return 0
    if type(date) is int: return date
    if "." in date: 
        date = date.split(".")[0]
    else:  # Cuz apparently not all dates have the damn dot!!
        date = date.split("Z")[0]
        
    return int(time.mktime(datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").timetuple()))  # Return UNIX timestamp as an int to get rid of any decimals