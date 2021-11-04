import os
import json
import sys

"""This script contains global functions for all other scripts!"""

def load_cfg():
    if not os.path.isfile("config.json"):
        sys.exit("'config.json' not found! Please add it and try again.")
    else:
        with open("config.json", "r") as file:
            cfg = json.load(file)
        
    return cfg