import datetime
from discord import Embed
from discord import Colour
from discord.ext.commands import Context

"""Adds finishing touches to embeds"""
def finalize_embed(ctx: Context, em: Embed):
    em.timestamp = datetime.datetime.now()
    if ctx.author:
        em.set_footer(text=f"Ran by {ctx.author.name}", icon_url=ctx.author.avatar)
    em.colour = Colour.orange()

    return em