import discord
from discord.ext import commands
from exceptions import ImageNotFound

class FetchImage(commands.Converter):
    """
    Converts a room name param to a RR image
    """
    async def convert(self, ctx: discord.ApplicationContext, image_id: id):
        image = await ctx.bot.RecNet.images.fetch(image_id)
        if not image: raise ImageNotFound
        return image
    
