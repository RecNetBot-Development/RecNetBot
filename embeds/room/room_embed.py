from embeds.base.embed import DefaultEmbed as Embed
from utility.emojis import get_emoji
from utility.funcs import unix_timestamp
from utility.rec_net_helpers import img_url, profile_url

"""Makes an embed for a single room"""
def room_embed(room, hot_rooms = {}):
    accessibility = [
        {"mode": "`Screen`", "supported": 'screen' in room.supported_platforms, "icon": get_emoji('screen')},
        {"mode": "`Walk`", "supported": 'walk' in room.supported_platforms, "icon": get_emoji('walk')},
        {"mode": "`Teleport`", "supported": 'teleport' in room.supported_platforms, "icon": get_emoji('teleport')},
        {"mode": "`Quest 1`", "supported": 'vr low' in room.supported_platforms, "icon": get_emoji('quest1')},
        {"mode": "`Quest 2`", "supported": 'quest 2' in room.supported_platforms, "icon": get_emoji('quest2')},
        {"mode": "`Mobile`", "supported": 'mobile' in room.supported_platforms, "icon": get_emoji('mobile')},
        {"mode": "`Juniors`", "supported": 'juniors' in room.supported_platforms, "icon": get_emoji('junior')}
    ]

    # Sub rooms
    subroom_list = [subroom.name for subroom in room.sub_rooms[:10]] if room.sub_rooms else ["None!"]
    if len(room.sub_rooms) > 10:
        subroom_list.append("...")

    # Supported
    supported_list, unsupported_list = [], []
    for mode in accessibility:  # Goes through all accessibility options
        mode_name = f"{mode['icon']} {mode['mode']}"

        if mode['supported']:
            supported_list.append(mode_name)
            continue
        unsupported_list.append(mode_name)
        
    # Roles
    role_counts = {
        "co-owner": len(list(filter(lambda role: role.role == "co-owner", room.roles))),
        "moderator": len(list(filter(lambda role: role.role == "moderator", room.roles))),
        "host": len(list(filter(lambda role: role.role == "host", room.roles)))
    }
    
    role_pieces = []
    
    if role_counts['co-owner']: role_pieces.append(f"`{role_counts['co-owner']}` — Co-Owners")
    if role_counts['moderator']: role_pieces.append(f"`{role_counts['moderator']}` — Moderators")
    if role_counts['host']: role_pieces.append(f"`{role_counts['host']}` — Hosts")
    
    supported = ', '.join(supported_list) if supported_list else None
    unsupported = ', '.join(unsupported_list) if unsupported_list else None
    
    description = f"""
by [`@{room.creator.username}`]({profile_url(room.creator.username)})
```{room.description}```
    """
    
    # Room hot placement
    placement = 0
    if hot_rooms: 
        if isinstance(hot_rooms, dict):
            placement = f"{next((i for (i, _room) in enumerate(hot_rooms) if _room['RoomId'] == room.id), 0):,}"
        elif isinstance(hot_rooms, int):
            placement = f"{hot_rooms:,}"
            
    # Room engagement
    score = 0
    if room.scores: score = round((sum([i.score for i in room.scores]) / len(room.scores)) * 100)
    
    details = f"""
{get_emoji('date')} {unix_timestamp(room.created_at)} — Created At
{get_emoji('tag')} `{', '.join(room.tags) if room.tags else '...'}` ({len(room.tags)}) — Tags
{get_emoji('subrooms')} `{", ".join(subroom_list)}` ({len(room.sub_rooms)}) — Subrooms
{get_emoji('limit')} `{room.max_players}` — Player Limit
    """
    
    statistics = f"""
{get_emoji('cheer')} `{room.cheer_count:,}` — Cheers
{get_emoji('favorite')} `{room.favorite_count:,}` — Favorites
{get_emoji('visitors')} `{room.visitor_count:,}` — Visitors
{get_emoji('visitor')} `{room.visit_count:,}` — Visits
{get_emoji('hot')} `#{placement if placement else '>1,000'}` — Hot Placement
{get_emoji('engagement')} `{score}%` — Engagement
    """
    
    roles = None
    if role_pieces:
        roles = "\r".join(role_pieces)
    
    warnings_str_list, warnings, custom_warning = [], "", f"```{room.custom_warning}```"
    warning_icons = {
        "Spooky/scary themes": get_emoji('spooky'),
        "Mature themes": get_emoji('mature'),
        "Bright/flashing lights": get_emoji('bright'),
        "Intense motion": get_emoji('motion'),
        "Gore/violence": get_emoji('gore')
    }
    if room.warnings:  # Check if it's none
        for warning in room.warnings:
            warnings_str_list.append(f"{warning_icons.get(warning, get_emoji('unknown'))} `{warning}`")
        warnings = ', '.join(warnings_str_list)
    
    # Define embed
    em = Embed(
        title = f"^{room.name} {'(RRO)' if room.is_rro else ''}",
        description = description,
        url=f"https://rec.net/room/{room.name}"
    )
    
    if details: em.add_field(name="Details", value=details, inline=False)
    if supported: em.add_field(name="Supported Modes", value=supported, inline=False)
    if unsupported: em.add_field(name="Unsupported Modes", value=unsupported, inline=False)
    if warnings: em.add_field(name="Warnings", value=warnings, inline=False)
    if room.custom_warning: em.add_field(name="Custom Warning", value=custom_warning, inline=False)
    if roles: em.add_field(name="Roles", value=roles, inline=False)
    if statistics: em.add_field(name="Statistics", value=statistics, inline=False)

    # Set the room's thumbnail as image
    em.set_image(url=img_url(room.image_name))
    # Set the creator's pfp as thumbnail
    em.set_thumbnail(url=img_url(room.creator.profile_image, True, 180))
    
    return em  # Return the embed.