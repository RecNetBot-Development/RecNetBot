import discord
from embeds import get_default_embed
from resources import get_emoji
from utils import invention_url, img_url, unix_timestamp
from recnetpy.dataclasses.invention import Invention
from database import InventionStats

def invention_embed(invention: Invention, cached_stats: InventionStats = "None") -> discord.Embed:
    em = get_default_embed()
    em.title = invention.name
    em.url = invention_url(invention.id)
    em.description = f"```{invention.description}```"
    em.set_image(url=img_url(invention.image_name))
    
    if invention.price:
        em.description = f"{get_emoji('token')} `{invention.price:,}`\n" + em.description
    
    if invention.is_certified_invention:
        em.description = "**CERTIFIED INVENTION**\n" + em.description
    
    details = [
        f"{get_emoji('date')} {unix_timestamp(invention.first_published_at)} — Published At",
        f"{get_emoji('permission')} `{invention.general_permission}` — Permission",
        f"{get_emoji('update')} {unix_timestamp(invention.modified_at)} — Latest Update"
    ]
    
    # Don't insert tags if none exist
    tags = list(map(lambda ele: ele.tag, invention.tags)) if invention.tags else None
    if tags: details.insert(1,  
        f"{get_emoji('tag')} `{', '.join(tags)}` ({len(invention.tags)}) — Tags")
    
    
    used_in_room_dif, downloads_dif, cheer_dif, last_check = 0, 0, 0, 0
    if cached_stats not in ("None", None):
        used_in_room_dif = invention.num_players_have_used_in_room - cached_stats.num_used_in_room if invention.num_players_have_used_in_room != cached_stats.num_used_in_room else 0
        downloads_dif = invention.num_downloads - cached_stats.num_downloads if invention.num_downloads != cached_stats.num_downloads else 0
        cheer_dif = invention.cheer_count - cached_stats.cheer_count if invention.cheer_count - cached_stats.cheer_count else 0
        last_check = cached_stats.cached_timestamp
    
    statistics = [
        f"{get_emoji('download')} `{invention.num_downloads:,}`{f' *(+{downloads_dif})*' if downloads_dif else ''} — Downloads",
        f"{get_emoji('room')} `{invention.num_players_have_used_in_room:,}`{f' *(+{used_in_room_dif})*' if used_in_room_dif else ''} — Used In Rooms",
        f"{get_emoji('cheer')} `{invention.cheer_count:,}`{f' *(+{cheer_dif})*' if cheer_dif else ''} — Cheers",
    ]
    
    if last_check:
        statistics.append(f"\nYou last checked this invention out {unix_timestamp(last_check, 'R')}!")
    elif cached_stats != "None":
        statistics.append(f"\nYou can see the statistical difference the next time you view this invention!")
    
    # Only add if it exists at all
    version = []
    # Ink cost
    if invention.current_version.instantiation_cost: version.append(
        f"{get_emoji('ink')} `{invention.current_version.instantiation_cost}%` — Ink Cost"
    )
    # CV2 chips
    if invention.current_version.chips_cost: version.append(
        f"{get_emoji('cv2')} `{invention.current_version.chips_cost}` — CV2 Chips"
    )
    # Cloud variables
    if invention.current_version.cloud_variables_cost: version.append(
        f"{get_emoji('cloud')} `{invention.current_version.cloud_variables_cost}` — Cloud Variables"
    )
    # Light sources
    if invention.current_version.lights_cost: version.append(
        f"{get_emoji('light')} `{invention.current_version.lights_cost}` — Light Sources"
    )
    
    em.add_field(name="Details", value="\n".join(details), inline=False)
    if version:  # I doubt there can't be anything but just in case
        em.add_field(name="Spawn Costs", value="\n".join(version), inline=True)
    em.add_field(name="Statistics", value="\n".join(statistics), inline=False)
    
    return em


async def fetch_invention_embed(invention: Invention, *args, **kwargs) -> discord.Embed:
    """
    Fetches the necessary embed required for the embed
    """
    
    await invention.get_tags()
    return invention_embed(invention, *args, **kwargs)