import discord
from discord.ext import commands
from exceptions import InventionNotFound, InvalidURL
from urllib.parse import urlparse

class FetchInvention(commands.Converter):
    """
    Converts a username param to a RR invention
    """
    async def convert(self, ctx: discord.ApplicationContext, _invention: str):
        invention_id = 0
        if isinstance(_invention, str):
            # Sanitize input
            _invention = _invention.strip()
            
            if _invention.isdigit(): 
                invention_id = _invention
            else:
                url = urlparse(_invention)
                
                if url.netloc != "rec.net":
                    raise InvalidURL
                
                if "invention/" in url.path:
                    invention_id = url.path.split("invention/")[1]
                else:
                    raise InvalidURL("/invention/...")
        
        invention = await ctx.bot.RecNet.inventions.fetch(invention_id)
        if not invention: raise InventionNotFound
        return invention
    
