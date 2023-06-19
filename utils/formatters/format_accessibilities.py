from resources import get_emoji
from recnetpy.dataclasses.room import Room
from typing import List, Tuple


ACCESSIBILITY = [
    {"format": "Screen", "icon": get_emoji('screen')},
    {"format": "Walk", "icon": get_emoji('walk')},
    {"format": "Teleport", "icon": get_emoji('teleport')},
    {"format": "Quest 1", "icon": get_emoji('quest1')},
    {"format": "Quest 2", "icon": get_emoji('quest2')},
    {"format": "Mobile", "icon": get_emoji('mobile')},
    {"format": "Juniors", "icon": get_emoji('junior')}
]

def format_ele(ele: dict, allowed: bool) -> str:
    emoji = get_emoji("correct") if allowed else get_emoji("incorrect")
    return f"`{emoji} {ele['format']} `"

def format_accessibilities(room: Room) -> Tuple[List[str], List[str]]:
    """
    Formats the playable and unplayable modes in a room
    This, is, pain.
    """
    
    supported = []
    supported.insert(0 if room.supports_screens else len(supported), format_ele(ACCESSIBILITY[0], room.supports_screens))
    supported.insert(0 if room.supports_walk_vr else len(supported), format_ele(ACCESSIBILITY[1], room.supports_walk_vr))
    supported.insert(0 if room.supports_teleport_vr else len(supported), format_ele(ACCESSIBILITY[2], room.supports_teleport_vr))
    supported.insert(0 if room.supports_vr_low else len(supported), format_ele(ACCESSIBILITY[3], room.supports_vr_low))
    supported.insert(0 if room.supports_quest_two else len(supported), format_ele(ACCESSIBILITY[4], room.supports_quest_two))
    supported.insert(0 if room.supports_mobile else len(supported), format_ele(ACCESSIBILITY[5], room.supports_mobile))
    supported.insert(0 if room.supports_juniors else len(supported), format_ele(ACCESSIBILITY[6], room.supports_juniors))
        
    return supported
