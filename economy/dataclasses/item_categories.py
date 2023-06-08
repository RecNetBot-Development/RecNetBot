from enum import Enum

class ItemCategories(Enum):
    NONE = 0
    PIZZA = 1
    DONUTS = 2
    CAKE = 3
    DRINKS = 4
    FILM = 5
    KO = 6
    OTHER = 7
    POTIONS = 8

def get_category(raw_category: str) -> ItemCategories:
    match raw_category:
        case "pizza":
            category = ItemCategories.PIZZA
        case "donuts":
            category = ItemCategories.DONUTS
        case "cake":
            category = ItemCategories.CAKE
        case "drinks":
            category = ItemCategories.DRINKS
        case "film":
            category = ItemCategories.FILM
        case "ko":
            category = ItemCategories.KO
        case "other":
            category = ItemCategories.OTHER
        case "potions":
            category = ItemCategories.POTIONS
        case _:
            category = ItemCategories.NONE

    return category