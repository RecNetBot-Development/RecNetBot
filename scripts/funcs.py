import os
import json
import sys
import time
from datetime import datetime

"""This script contains global functions for all other scripts!"""

def unix_timestamp(unix: int):
    return f"<t:{unix}:f>"

# Loads the local config file
def load_cfg():
    if os.path.isfile("config.json"):
        with open("config.json", "r") as file:
            l_cfg = json.load(file)  # Local config
    
    cfg = {
        "dev_role": os.environ.get('DEV_ROLE', l_cfg['dev_role']),
        "test_guild_id": int(os.environ.get('TEST_GUILD_ID', l_cfg['test_guild_id'])),
        "prefix": os.environ.get('PREFIX', l_cfg['prefix']),
        "token": os.environ.get('DISCORD_TOKEN', l_cfg['token']),
        "redis_url": os.environ.get('REDIS_URL', l_cfg['redis_url'])
    }  # Prioritize env variables

    for key in cfg:
        if not cfg[key]:  # If some key is missing, the config is invalid
            sys.exit("Invalid config!")
    return cfg


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


# Command log
def log(ctx):
    user, server, command = ctx.author, ctx.guild.name, ctx.command
    print(f"{user} ran /{ctx.command.name} in {ctx.guild} at {datetime.utcnow()} UTC")


# Remove list duplicates
def remove_dupes_from_list(list_):
    pure = []
    [pure.append(x) for x in list_ if x not in pure]
    return pure
