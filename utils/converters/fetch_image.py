import discord
from discord.ext import commands
from exceptions import ImageNotFound, InvalidURL
from urllib.parse import urlparse

class FetchImage(commands.Converter):
    """
    Converts a room name param to a RR image
    """
    async def convert(self, ctx: discord.ApplicationContext, _image: str | int):
        image = None
        image_id = 0
        if isinstance(_image, str):
            # Sanitize input
            _image = _image.strip()
            
            if _image.isdigit():  # If it's a stringified id
                image_id = _image
                if int(image_id) > 0:
                    image = await ctx.bot.RecNet.images.fetch(image_id)
            else:
                url = urlparse(_image)
                
                if url.netloc == "rec.net":  # If RecNet post url
                    if "image/" in url.path:
                        image_id = url.path.split("image/")[1]
                    elif "image=" in url.query:
                        image_id = url.query.split("image=")[1]
                    else:
                        raise InvalidURL(path="/image/...")
                    
                    if image_id.isdigit() and int(image_id) > 0:
                        image = await ctx.bot.RecNet.images.fetch(image_id)
                    
                elif url.netloc == "img.rec.net":  # If img.rec.net url
                    image_name = url.path.replace("/", "")

                    if image_name and image_name.isascii():
                        image = await ctx.bot.RecNet.images.get(image_name)
                    
                else:
                    if _image and _image.isascii():
                        if not _image.startswith('-'):
                            image = await ctx.bot.RecNet.images.get(_image)  # Test if the param is just the image name
                    if not image: raise InvalidURL
                    
        if not image: raise ImageNotFound
        return image
    
