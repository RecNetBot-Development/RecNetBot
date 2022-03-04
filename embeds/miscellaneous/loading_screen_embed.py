from pydoc import resolve
from discord import Embed
from embeds.finalize_embed import finalize_embed
from utility import img_url, Emoji, create_platforms_section, unix_timestamp

def loading_screen_embed(ctx, loading_screen_data):
    lsd = loading_screen_data  # mhmm
    em = Embed(
        title=lsd['Title'],
        description=lsd['Message']
    )
    em.set_image(url=img_url(lsd['ImageName']))
    
    em.add_field(name="Details", value=f"""
{Emoji.correct if lsd['Visibility'] else Emoji.incorrect} Visible?
{Emoji.correct if lsd['AllowCycling'] else Emoji.incorrect} Allows Cycling?    
{Emoji.correct if lsd['RestrictToNewUsers'] else Emoji.incorrect} Restricted to New Users?              
"""
    )
    
    em.add_field(name="Introduced At", value=unix_timestamp(lsd['CreatedAt']))
    
    platforms = create_platforms_section(platform_mask=lsd['PlatformMask'])
    em.add_field(name="Targeted Platforms", value=platforms, inline=False)
    
    if lsd['RoomNames']:
        em.add_field(name="Associated Room(s)", value=', '.join(lsd['RoomNames']))
    em = finalize_embed(ctx, em)
    return em