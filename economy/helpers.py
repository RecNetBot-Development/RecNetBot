import discord
import json

def get_rarity_color(rarity = 1):
    """ Returns the Discord color for each rarity """

    match rarity:
        case 5:
            color = discord.Color.orange()
        case 4:
            color = discord.Color.purple()
        case 3:
            color = discord.Color.blue()
        case 2:
            color = discord.Color.green()
        case _:
            color = discord.Color.dark_gray()

    return color


with open("economy/items.json") as items:
    ITEMS: list = json.load(items)

def load_items():
    """
    Load all econ item data
    """
    return ITEMS


def get_item(item_name: str = None, item_id: int = None) -> dict:
    """
    Get an item by its name or ID
    """
    for item in ITEMS:
        if item_name:
            if item["name"].lower() == item_name.lower():
                return item
            
        elif item_id:
            if item["id"] == item_id:
                return item
            
        else:
            break
        
    return None


with open("economy/quests.json") as quests:
    QUESTS: list = json.load(quests)

def load_quests():
    """
    Load all quest data
    """
    return QUESTS


with open("economy/beg.json") as beg:
    BEGS: list = json.load(beg)

def load_begs():
    """
    Load all beg data
    """
    return BEGS