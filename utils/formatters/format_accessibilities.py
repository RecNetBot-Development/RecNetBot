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

def format_ele(ele: dict) -> str:
    return f"{ele['icon']} `{ele['format']}`"

def format_accessibilities(room: Room) -> Tuple[List[str], List[str]]:
    """
    Formats the playable and unplayable modes in a room
    This, is, pain.
    """
    
    supported, unsupported = [], []
    if room.supports_screens:
        supported.append(format_ele(ACCESSIBILITY[0]))
    else:
        unsupported.append(format_ele(ACCESSIBILITY[0]))
        
    if room.supports_walk_vr:
        supported.append(format_ele(ACCESSIBILITY[1]))
    else:
        unsupported.append(format_ele(ACCESSIBILITY[1]))
        
    if room.supports_teleport_vr:
        supported.append(format_ele(ACCESSIBILITY[2]))
    else:
        unsupported.append(format_ele(ACCESSIBILITY[2]))
        
    if room.supports_vr_low:
        supported.append(format_ele(ACCESSIBILITY[3]))
    else:
        unsupported.append(format_ele(ACCESSIBILITY[3]))
        
    if room.supports_quest_two:
        supported.append(format_ele(ACCESSIBILITY[4]))
    else:
        unsupported.append(format_ele(ACCESSIBILITY[4]))
        
    if room.supports_mobile:
        supported.append(format_ele(ACCESSIBILITY[5]))
    else:
        unsupported.append(format_ele(ACCESSIBILITY[5]))
        
    if room.supports_juniors:
        supported.append(format_ele(ACCESSIBILITY[6]))
    else:
        unsupported.append(format_ele(ACCESSIBILITY[6]))
        
    return (supported, unsupported)
