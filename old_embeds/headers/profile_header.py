from utility import get_emoji
from utility.rec_net_helpers import img_url, profile_url

def profile_header(user, embed, client=None):
    embed.set_author(
        name = f"{get_emoji('link', client) if client else get_emoji('default_link')} @{user.username}",
        url = profile_url(user.username),
        icon_url=img_url(user.profile_image, crop_square=True, resolution=180)
    )
    
    return embed