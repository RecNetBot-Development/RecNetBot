import discord
from embeds import get_default_embed
from resources import get_emoji
from utils import invention_url, img_url, unix_timestamp
from recnetpy.dataclasses.invention import Invention

def invention_embed(invention: Invention) -> discord.Embed:
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
    
    statistics = [
        f"{get_emoji('download')} `{invention.num_downloads:,}` — Downloads",
        f"{get_emoji('room')} `{invention.num_players_have_used_in_room:,}` — Used In Rooms",
        f"{get_emoji('cheer')} `{invention.cheer_count:,}` — Cheers",
    ]
    
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