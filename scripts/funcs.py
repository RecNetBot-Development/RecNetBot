import os
import json
import sys
import time
import datetime

"""This script contains global functions for all other scripts!"""

# Loads the local config file
def load_cfg():
    if not os.path.isfile("config.json"):
        sys.exit("'config.json' not found! Please add it and try again.")
    else:
        with open("config.json", "r") as file:
            cfg = json.load(file)
        
    return cfg


# Converts dates from RecNet to an unix timestamp, that can be used to show dates more elegantly
def date_to_unix(date):
    # We only want the date from 2020-12-15T04:56:54.4519046Z
    date = date.split(".")[0]
    return int(time.mktime(datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").timetuple()))  # Return UNIX timestamp as an int to get rid of any decimals