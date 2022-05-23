from email.mime import image
from discord import Embed
from utility.emojis import get_emoji
from utility.rec_net_helpers import img_url, room_url

def placement_embed(room, placement, tags, keywords):
    em = Embed(
        title=f"{room.name}'s placement on hot",
        description = f"""
{get_emoji('hot')} `{placement}`
Tags: `{tags}`
Keywords: `{keywords}`
        """
    )
    em.set_author(name=f"^{room.name}", url=room_url(room.name), icon_url=img_url(room.image_name, crop_square=True))
    return em