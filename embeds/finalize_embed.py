import discord
import datetime

"""Adds finishing touches to embeds"""
async def finalize_embed(em: discord.Embed, author: discord.Member = None):
    em.timestamp = datetime.datetime.now()
    if author:
        em.set_footer(text=f"Ran by {author.name}", icon_url=author.avatar)
    em.colour = discord.Colour.orange()

    return em