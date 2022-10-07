from recnetpy.dataclasses.role import Role
from typing import List
from resources import get_emoji


def format_roles(roles: List[Role]) -> List[str]:
    """
    Formats roles for the room embed
    """
    
    role_counts = {
        "co-owner": len(list(filter(lambda role: role.role == "Co-Owner", roles))),
        "moderator": len(list(filter(lambda role: role.role == "Moderator", roles))),
        "host": len(list(filter(lambda role: role.role == "Member", roles)))
    }
    
    formatted = []
    if role_counts['co-owner']: formatted.append(f"{get_emoji('role_owner')} `{role_counts['co-owner']}` — Co-Owners")
    if role_counts['moderator']: formatted.append(f"{get_emoji('role_mod')} `{role_counts['moderator']}` — Moderators")
    if role_counts['host']: formatted.append(f"{get_emoji('role_host')} `{role_counts['host']}` — Hosts")
    
    return formatted