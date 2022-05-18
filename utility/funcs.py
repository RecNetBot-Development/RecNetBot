import os
import json
import sys
import time
from datetime import datetime
from rec_net.helpers import date_to_unix

"""This script contains global functions for all other scripts!"""

def unix_timestamp(timestamp):
    if isinstance(timestamp, int):
        return f"<t:{timestamp}:f>"
    elif isinstance(timestamp, str):
        return f"<t:{date_to_unix(timestamp)}:f>"
    else:
        return f"<t:{0}:f>"

# Loads the local config file
cached_config = {}
def load_cfg():
    global cached_config
    if cached_config: return cached_config
    
    cfg = {}
    if os.path.isfile("config.json"):
        with open("config.json", "r") as file:
            cfg = json.load(file)  # Local config
        
    for key, value in cfg.items():
        cfg[key] = os.environ.get(key, value)
        if isinstance(cfg[key], str):
            try:
                cfg[key] = json.loads(cfg[key])
            except json.decoder.JSONDecodeError: 
                pass
        
        if not cfg[key]: cfg[key] = None
    
    cached_config = cfg
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