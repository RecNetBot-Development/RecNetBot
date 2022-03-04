from re import I
from discord import Embed
from embeds.finalize_embed import finalize_embed
from utility import Emoji, unix_timestamp, img_url, profile_url

"""Makes an embed for a single room"""
def room_embed(ctx, room, hot_rooms = {}):
    accessibility = [
        {"mode": "`Screen`", "supported": 'screen' in room.supported_platforms, "icon": Emoji.screen},
        {"mode": "`Walk`", "supported": 'walk' in room.supported_platforms, "icon": Emoji.walk},
        {"mode": "`Teleport`", "supported": 'teleport' in room.supported_platforms, "icon": Emoji.teleport},
        {"mode": "`Quest 1`", "supported": 'vr low' in room.supported_platforms, "icon": Emoji.quest1},
        {"mode": "`Quest 2`", "supported": 'quest 2' in room.supported_platforms, "icon": Emoji.quest2},
        {"mode": "`Mobile`", "supported": 'mobile' in room.supported_platforms, "icon": Emoji.mobile},
        {"mode": "`Juniors`", "supported": 'juniors' in room.supported_platforms, "icon": Emoji.junior}
    ]

    # Sub rooms
    subroom_list = [subroom.name for subroom in room.sub_rooms] if room.sub_rooms else ["None!"]

    # Supported
    supported_list, unsupported_list = [], []
    for mode in accessibility:  # Goes through all accessibility options
        mode_name = f"{mode['icon']} {mode['mode']}"

        if mode['supported']:
            supported_list.append(mode_name)
            continue
        unsupported_list.append(mode_name)
        
    # Roles
    roles = {
        "co-owner": len(list(filter(lambda role: role.role == "co-owner", room.roles))),
        "moderator": len(list(filter(lambda role: role.role == "moderator", room.roles))),
        "host": len(list(filter(lambda role: role.role == "host", room.roles)))
    }
    co_owners = f"`{roles['co-owner']}` — Co-Owners" if roles['co-owner'] else ""
    moderators = f"`{roles['moderator']}` — Moderators" if roles['moderator'] else ""
    hosts = f"`{roles['host']}` — Hosts" if roles['host'] else ""
    
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
            placement = next((i for (i, _room) in enumerate(hot_rooms) if _room["RoomId"] == room.id), 0)
        elif isinstance(hot_rooms, int):
            placement = hot_rooms
            
    # Room engagement
    score = 0
    if room.scores: score = round((sum([i.score for i in room.scores]) / len(room.scores)) * 100)
    
    details = f"""
{Emoji.date} {unix_timestamp(room.created_at)} — Created At
{Emoji.tag} `{', '.join(room.tags)}` ({len(room.tags)}) — Tags
{Emoji.subrooms} `{", ".join(subroom_list)}` ({len(subroom_list)}) — Subrooms
{Emoji.visitors} `{room.max_players}` — Player Limit
    """
    
    statistics = f"""
{Emoji.cheer} `{room.cheer_count:,}` — Cheers
{Emoji.favorite} `{room.favorite_count:,}` — Favorites
{Emoji.visitors} `{room.visitor_count:,}` — Visitors
{Emoji.visitor} `{room.visit_count:,}` — Visits
{Emoji.hot} `#{placement:, if placement else '>1,000'}` — Hot Placement
{Emoji.engagement} `{score}%` — Engagement
    """
    
    roles = None
    if co_owners or moderators or hosts:
        roles = f"""
{co_owners}
{moderators}
{hosts}
        """
    
    warnings_str_list, warnings, custom_warning = [], "", f"```{room.custom_warning}```"
    warning_icons = {
        "Spooky/scary themes": Emoji.spooky,
        "Mature themes": Emoji.mature,
        "Bright/flashing lights": Emoji.bright,
        "Intense motion": Emoji.motion,
        "Gore/violence": Emoji.gore
    }
    if room.warnings:  # Check if it's none
        for warning in room.warnings:
            warnings_str_list.append(f"{warning_icons.get(warning, Emoji.unknown)} `{warning}`")
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
    em = finalize_embed(ctx, em)
    
    return em  # Return the embed.