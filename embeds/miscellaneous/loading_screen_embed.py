from discord import Embed
from utility.image.finalize_embed import finalize_embed
from utility.emojis import get_emoji
from utility.rec_net_helpers import img_url
from utility.account.create_platform_section import create_platforms_section
from utility.funcs import unix_timestamp

def loading_screen_embed(loading_screen_data):
    lsd = loading_screen_data  # mhmm
    em = Embed(
        title=lsd['Title'],
        description=lsd['Message']
    )
    em.set_image(url=img_url(lsd['ImageName']))
    
    em.add_field(name="Details", value=f"""
{get_emoji('correct') if lsd['Visibility'] else get_emoji('incorrect')} Visible?
{get_emoji('correct') if lsd['AllowCycling'] else get_emoji('incorrect')} Allows Cycling?    
{get_emoji('correct') if lsd['RestrictToNewUsers'] else get_emoji('incorrect')} Restricted to New Users?              
"""
    )
    
    em.add_field(name="Introduced At", value=unix_timestamp(lsd['CreatedAt']))
    
    platforms = create_platforms_section(platform_mask=lsd['PlatformMask'])
    em.add_field(name="Targeted Platforms", value=platforms, inline=False)
    
    if lsd['RoomNames']:
        em.add_field(name="Associated Room(s)", value=', '.join(lsd['RoomNames']))

    return em