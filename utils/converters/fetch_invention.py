import discord
from discord.ext import commands
from exceptions import InventionNotFound

class FetchInvention(commands.Converter):
    """
    Converts a username param to a RR invention
    """
    async def convert(self, ctx: discord.ApplicationContext, _invention: str):
        invention_id = 0
        if isinstance(_invention, str):
            if _invention.isdigit(): 
                invention_id = _invention
            else:
                # This is fucking crazy and I can't believe I wrote this shit
                url = _invention.split("/")
                invention_id = list(filter(lambda piece: piece.isdigit(), url))
                if invention_id:
                    invention_id = invention_id[0]
                else:
                    raise InventionNotFound
        
        invention = await ctx.bot.RecNet.inventions.fetch(invention_id)
        if not invention: raise InventionNotFound
        return invention
    
