import datetime
from discord import Colour

"""Adds finishing touches to embeds"""
def finalize_embed(ctx, em, set_author_footer=True):
    em.timestamp = datetime.datetime.now()
    if ctx.author and set_author_footer:
        em.set_footer(text=f"Ran by {ctx.author.name}", icon_url=ctx.author.avatar)
    em.colour = Colour.orange()

    return em