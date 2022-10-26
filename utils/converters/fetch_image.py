import discord
from discord.ext import commands
from exceptions import ImageNotFound, InvalidURL
from urllib.parse import urlparse

class FetchImage(commands.Converter):
    """
    Converts a room name param to a RR image
    """
    async def convert(self, ctx: discord.ApplicationContext, _image: str | int):
        image_id = 0
        if isinstance(_image, str):
            if _image.isdigit(): 
                image_id = _image
            else:
                url = urlparse(_image)
                
                if url.netloc != "rec.net":
                    raise InvalidURL
                
                if "image/" in url.path:
                    image_id = url.path.split("image/")[1]
                elif "image=" in url.query:
                    image_id = url.query.split("image=")[1]
                else:
                    raise InvalidURL("/image/...")
                
                
        image = await ctx.bot.RecNet.images.fetch(image_id)
        if not image: raise ImageNotFound
        return image
    
