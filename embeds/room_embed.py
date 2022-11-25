import discord
from embeds import get_default_embed
from resources import get_emoji, get_icon
from utils import unix_timestamp, room_url, img_url
from utils.formatters import format_accessibilities, format_roles, format_warnings
from recnetpy.dataclasses.room import Room
from database import RoomStats

def room_embed(room: Room, cached_stats: RoomStats = "None", hide_details: bool = False) -> discord.Embed:
    """
    Makes an embed for a single room
    """
    
    em = get_default_embed()
    em.title = f"^{room.name}"
    em.url = room_url(room.name)
    
    details, supported, unsupported, warnings, roles = None, None, None, None, None
    if not hide_details: 
        em.set_image(url=img_url(room.image_name))
        em.description = f"```{room.description}```"
        thumbnail_url = get_icon("rro") if room.is_rro else get_icon("ugc")
        em.set_thumbnail(url=thumbnail_url)
        
        # Sub rooms
        subroom_list = [subroom.name for subroom in room.subrooms[:10]] if room.subrooms else ["None!"]
        if len(room.subrooms) > 10:
            subroom_list.append("...")

        # Find out with subroom was updated the last
        latest_updated_subroom = None
        for subroom in room.subrooms:
            if subroom.data_saved_at:
                if not latest_updated_subroom or latest_updated_subroom.data_saved_at < subroom.data_saved_at:
                    latest_updated_subroom = subroom
                    
        if not latest_updated_subroom:  # If subrooms don't have save dates
            latest_updated_subroom = sorted(room.subrooms, key=lambda ele: ele.subroom_id)[-1]
            
        # Supported
        supported_list, unsupported_list = format_accessibilities(room)
        supported = ', '.join(supported_list) if supported_list else None
        unsupported = ', '.join(unsupported_list) if unsupported_list else None
                
        # Roles
        role_pieces = format_roles(room.roles)
        roles = "\n".join(role_pieces) if role_pieces else None
        
        # Warnings
        warnings = format_warnings(room.warnings)
        custom_warning = f"```{room.custom_warning}```"
        
        # Tags
        tags = list(map(lambda ele: ele.tag, room.tags)) if room.tags else ["..."]
    
        details = [
            f"{get_emoji('date')} {unix_timestamp(room.created_at)} — Created At",
            f"{get_emoji('tag')} `{', '.join(tags)}` ({len(room.tags)}) — Tags",
            f"{get_emoji('subrooms')} `{', '.join(subroom_list)}` ({len(room.subrooms)}) — Subrooms",
            f"{get_emoji('limit')} `{room.max_players}` — Player Limit",
            f"{get_emoji('update')} In `{latest_updated_subroom.name}` at {unix_timestamp(latest_updated_subroom.data_saved_at if latest_updated_subroom.data_saved_at else room.created_at)} — Latest Update",
        ]
        
        if details: em.add_field(name="Details", value="\n".join(details), inline=False)
        if supported: em.add_field(name="Supported Modes", value=supported, inline=False)
        if unsupported: em.add_field(name="Unsupported Modes", value=unsupported, inline=False)
        if warnings: em.add_field(name="Warnings", value=" ".join(warnings), inline=False)
        if room.custom_warning: em.add_field(name="Custom Warning", value=custom_warning, inline=False)
        if roles: em.add_field(name="Roles", value=roles, inline=False)
        
        # Voice moderation check
        #if room.voice_moderated: details.insert(-1, f"{get_emoji('toxmod')} Voice Moderation enabled!")
    else:
        em.set_thumbnail(url=img_url(room.image_name))
            
    # Room engagement
    score = round((sum([i.score for i in room.scores]) / len(room.scores)) * 100) if room.scores else 0

    # Room hot placement
    #placement = 0
    #if hot_rooms: 
    #    if isinstance(hot_rooms, dict):
    #        placement = f"{next((i for (i, _room) in enumerate(hot_rooms) if _room['RoomId'] == room.id), 0):,}"
    #    elif isinstance(hot_rooms, int):
    #        placement = f"{hot_rooms:,}"
    
    # Player retention    
    retention = round((room.visitor_count / room.visit_count) * 100, 2) if room.visit_count > 0 else 0
    
    # Cheer ratio
    cheer_ratio = round((room.cheer_count / room.visitor_count) * 100, 2) if room.visitor_count > 0 else 0
    
    cheer_dif, favorite_dif, visitor_dif, visit_dif, last_check = 0, 0, 0, 0, 0
    if cached_stats not in ("None", None):
        cheer_dif = room.cheer_count - cached_stats.cheers if room.cheer_count != cached_stats.cheers else 0
        favorite_dif = room.favorite_count - cached_stats.favorites if room.favorite_count != cached_stats.favorites else 0
        visitor_dif = room.visitor_count - cached_stats.visitors if room.visitor_count - cached_stats.visitors else 0
        visit_dif = room.visit_count - cached_stats.visits if room.visit_count != cached_stats.visits else 0
        last_check = cached_stats.cached_timestamp
    
    statistics = [
        f"{get_emoji('cheer')} `{room.cheer_count:,}`{f' *(+{cheer_dif:,})*' if cheer_dif else ''} — Cheers",
        f"{get_emoji('favorite')} `{room.favorite_count:,}`{f' *(+{favorite_dif:,})*' if favorite_dif else ''} — Favorites",
        f"{get_emoji('visitors')} `{room.visitor_count:,}`{f' *(+{visitor_dif:,})*' if visitor_dif else ''} — Visitors",
        f"{get_emoji('visitor')} `{room.visit_count:,}`{f' *(+{visit_dif:,})*' if visit_dif else ''} — Visits",
        #f"{get_emoji('hot')} `#{placement if placement else '>1,000'}` — Hot Placement",
        f"{get_emoji('engagement')} `{score}%` — Engagement",
        f"{get_emoji('visitors')} `{retention}%` — Player Retention",
        f"{get_emoji('cheer')} `{cheer_ratio}%` — Cheer to Visitor Ratio"
    ]
    
    if last_check:
        statistics.append(f"\nYou last checked this room out {unix_timestamp(last_check, 'R')}!")
    elif cached_stats != "None":
        statistics.append(f"\nYou can see the statistical difference the next time you view this room!")
        
    if statistics:
        em.add_field(name="Statistics", value="\n".join(statistics), inline=False)
        em.set_footer(text="Engagement is a unofficial metric. Take it with a grain of salt.")
    
    return em


async def fetch_room_embed(room: Room, *args, **kwargs) -> discord.Embed:
    """
    Fetches the necessary data and returns the embed
    """
    room = await room.client.rooms.fetch(room.id, 78)
    return room_embed(room, *args, **kwargs)