import discord
from embeds import get_default_embed
from resources import get_emoji, get_icon
from utils import unix_timestamp, room_url, img_url
from utils.formatters import format_warnings
from recnetpy.dataclasses.room import Room
from database import RoomStats

def room_embed(room: Room, cached_stats: RoomStats = "None", hide_details: bool = False) -> discord.Embed:
    """
    Makes an embed for a single room
    """
    
    em = get_default_embed()
    em.title = f"^{room.name}"
    em.url = room_url(room.name)
    
    warnings = None
    if not hide_details: 
        em.set_image(url=img_url(room.image_name))
        em.description = f"```{room.description}```"
        thumbnail_url = get_icon("rro") if room.is_rro else get_icon("ugc")
        em.set_thumbnail(url=thumbnail_url)
        
        # Warnings
        warnings = format_warnings(room.warnings)
        custom_warning = f"```{room.custom_warning}```"
        
        if warnings: em.add_field(name="Warnings", value=" ".join(warnings), inline=False)
        if room.custom_warning: em.add_field(name="Custom Warning", value=custom_warning, inline=False)
    else:
        em.set_thumbnail(url=img_url(room.image_name))
    
    # Player retention    
    retention = round(room.visit_count / room.visitor_count, 2) if room.visitor_count > 0 else 0
    
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
        f"{get_emoji('cheervisitor')} `{cheer_ratio}%` — Cheer to Visitor Ratio",
        f"{get_emoji('revisit')} `{retention}` — Average Revisits",
    ]
    
    if last_check:
        statistics.append(f"\nYou last checked this room out {unix_timestamp(last_check, 'R')}!")
    elif cached_stats != "None":
        statistics.append(f"\nYou can see the statistical difference the next time you view this room!")
        
    if statistics:
        em.add_field(name="Statistics", value="\n".join(statistics), inline=False)
    
    em.set_footer(text="Information is cut due to API limitations. We are working with Rec Room to bring back data.", icon_url=get_icon("rectnet"))

    return em


async def fetch_room_embed(room: Room, *args, **kwargs) -> discord.Embed:
    """
    Fetches the necessary data and returns the embed
    """
    room = await room.client.rooms.fetch(room.id, 78)
    return room_embed(room, *args, **kwargs)