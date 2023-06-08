from typing import List
from .item_categories import ItemCategories

class Box:
    id: int
    name: str
    description: str
    emoji_icon: str
    img_url: str
    reward_categories: List[ItemCategories]
    rarities: List[int]
    items: List