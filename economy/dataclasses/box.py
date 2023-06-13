from typing import List
from dataclasses import dataclass
from .item_categories import ItemCategories, get_category
from .item import create_item_dataclass, Item

@dataclass
class Box:
    id: int
    name: str
    description: str
    emoji_icon: str
    img_url: str
    # Rewards
    categories: List[ItemCategories]
    rarities: List[int]
    items: List[Item]

def create_box_dataclass(raw_box: dict) -> Box:
    # Create item dataclasses
    raw_items, items = raw_box["rewards"]["items"], []
    for i in raw_items:
        items.append(create_item_dataclass(i))

    # Get categories
    raw_categories, categories = raw_box["rewards"]["categories"], []
    for i in raw_categories:
        categories.append(get_category(i))

    box = Box(
        id=raw_box["id"],
        name=raw_box["name"],
        description=raw_box["description"],
        emoji_icon=raw_box["emoji_icon"],
        img_url=raw_box["img_url"],
        categories=categories,
        rarities=raw_box["rewards"]["rarities"],
        items=items
    )
    
    return box
