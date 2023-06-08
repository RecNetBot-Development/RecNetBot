from dataclasses import dataclass
from .item_categories import ItemCategories, get_category

@dataclass
class Item:
    id: int
    name: str
    tokens: int
    category: ItemCategories
    rarity: int
    img_url: str
    emoji_icon: str
    wearable: bool
    purchasable: bool
    tradable: bool
    sellable: bool

def create_item_dataclass(raw_item: dict) -> Item:
    # Create dataclass
    item = Item(
        id=raw_item["id"],
        name=raw_item["name"],
        tokens=raw_item["tokens"],
        category=get_category(raw_item["category"]),
        rarity=raw_item["rarity"],
        img_url=raw_item["img_url"],
        emoji_icon=raw_item["emoji_icon"],
        wearable=raw_item["wearable"],
        purchasable=raw_item["purchasable"],
        tradable=raw_item["tradable"],
        sellable=raw_item["sellable"]
    )

    return item