from utility import get_emoji
from utility.rec_net_helpers import img_url, room_url

def room_header(room, embed, client=None):
    embed.set_author(
        name = f"{get_emoji('link', client) if client else get_emoji('default_link')} ^{room.name}",
        url = room_url(room.name),
        icon_url=img_url(room.image_name, crop_square=True, resolution=180)
    )
    
    return embed