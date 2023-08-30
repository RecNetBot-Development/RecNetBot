from resources import get_emoji
from typing import List

WARNING_ICONS = {
    "Spooky/scary themes": get_emoji('spooky'),
    "Mature themes": get_emoji('mature'),
    "Bright/flashing lights": get_emoji('bright'),
    "Intense motion": get_emoji('motion'),
    "Gore/violence": get_emoji('gore')
}

def format_warnings(warnings: List[str]):
    """Formats room warnings for the room embed"""
    
    formatted = []
        
    for ele in warnings:
        formatted.append(f"{WARNING_ICONS.get(ele, get_emoji('unknown'))}\u00a0`{ele}`")
            
    return formatted