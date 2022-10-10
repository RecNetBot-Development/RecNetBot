import discord
from discord.ext import commands
from exceptions import InventionNotFound

class FetchInvention(commands.Converter):
    """
    Converts a username param to a RR invention
    """
    async def convert(self, ctx: discord.ApplicationContext, invention_id: str):
        invention = await ctx.bot.RecNet.inventions.fetch(invention_id)
        if not invention: raise InventionNotFound
        return invention
    
