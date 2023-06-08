import discord
import json
from enum import Enum
from typing import List
from .dataclasses.box import Box
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


def get_item(item_name: str = None, item_id: int = None) -> Item:
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


with open("economy/boxes.json") as boxes:
    RAW_BOXES: list = json.load(boxes)
    BOXES: List[Box] = []
    for i in BOXES:
        # Create item dataclasses
        raw_items, items = i["rewards"]["items"], []
        for i in raw_items:
            items.append(create_item_dataclass(i))

        # Get categories
        raw_categories, categories = i["rewards"]["categories"], []
        for i in raw_categories:
            categories.append(get_category(i))

        box = Box(
            id=i["id"],
            name=i["name"],
            description=i["description"],
            emoji_icon=i["emoji_icon"],
            img_url=i["img_url"],
            reward_categories=categories,
            reward_rarities=i["rewards"]["rarities"],
            reward_items=items
        )

        BOXES.append(box)

def load_boxes() -> List[Box]:
    """
    Load all box data
    """
    return BOXES