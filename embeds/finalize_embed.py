import datetime
from discord import Colour

"""Adds finishing touches to embeds"""
def finalize_embed(ctx, em, set_author_footer=True, set_timestamp_footer=True):
    em.colour = Colour.orange()
    if not set_author_footer and not set_timestamp_footer: 
        return em
    
    if set_timestamp_footer: em.timestamp = datetime.datetime.now()
    if ctx.author and set_author_footer:
        em.set_footer(text=f"Ran by {ctx.author.name}", icon_url=ctx.author.avatar)
    
    return em