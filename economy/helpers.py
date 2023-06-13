import discord
import json
from enum import Enum
from typing import List, Optional
from .dataclasses.box import Box, create_box_dataclass
from .dataclasses.item import Item, create_item_dataclass
from .dataclasses.item_categories import ItemCategories, get_category
#from .dataclasses import ItemCategories, Item, Box, create_item_dataclass, get_category

def get_rarity_color(rarity = 1) -> discord.Color:
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

""" Load all items and make Item dataclasses for them """
with open("economy/items.json") as items:
    RAW_ITEMS: list = json.load(items)
    ITEMS: List[Item] = []
    for i in RAW_ITEMS:
        item = create_item_dataclass(i)
        ITEMS.append(item)

def load_items() -> List[Item]:
    """
    Load all econ item data
    """

    return ITEMS


def get_item(item_name: str = None, item_id: int = None) -> Optional[Item]:
    """
    Get an item by its name or ID
    """
    for item in ITEMS:
        if item_name:
            if item.name.lower() == item_name.lower():
                return item
            
        elif item_id:
            if item.id == item_id:
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


""" Load all boxes and make Box dataclasses for them """
with open("economy/boxes.json") as boxes:
    RAW_BOXES: list = json.load(boxes)
    BOXES: List[Box] = []
    for i in RAW_BOXES:
        box = create_box_dataclass(i)
        BOXES.append(box)

def load_boxes() -> List[Box]:
    """
    Load all box data
    """
    return BOXES

def get_box(box_name: str = None, box_id: int = None) -> Optional[Box]:
    """
    Get a box by its name or ID
    """
    for box in BOXES:
        if box_name:
            if box.name.lower() == box_name.lower():
                return box
            
        elif box_id:
            if box.id == box_id:
                return box
            
        else:
            break
        
    return None