import os
import json
import sys
import time
from datetime import datetime

"""This script contains global functions for all other scripts!"""

def unix_timestamp(timestamp):
    return f"<t:{timestamp}:f>"

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
        
# Command log
def log(ctx):
    user, server, command = ctx.author, ctx.guild.name, ctx.command
    print(f"{user} ran /{ctx.command.name} in {ctx.guild} at {datetime.utcnow()} UTC")


# Remove list duplicates
def remove_dupes_from_list(list_):
    pure = []
    [pure.append(x) for x in list_ if x not in pure]
    return pure

def handle_filters(filters):
    if type(filters) is not str: return [filters]
    pure_filters = list(filter(None, filters.split(" ")))
    return pure_filters