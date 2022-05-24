from embeds.base.embed import DefaultEmbed as Embed
from embeds.headers.room_header import room_header
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
    
    em = room_header(room, em)
    return em