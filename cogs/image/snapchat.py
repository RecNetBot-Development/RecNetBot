import discord
import aiohttp
import io
from discord.commands import slash_command, Option
from utils.converters import FetchImage
from utils import snapchat_caption, img_url

@slash_command(
    name="snapchat",
    description="Add a Snapchat caption to a RecNet photo."
)
async def data(
    self, 
    ctx: discord.ApplicationContext, 
    image: Option(FetchImage, name="photo", description="Enter a RecNet link or ID, img.rec.net link or image name", required=True),
    caption: Option(str, name="caption", description="Enter Snapchat caption", required=True)
):
    await ctx.interaction.response.defer()

    # Fetch image
    url = img_url(image.image_name, resolution=1080)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.read()

    # Respond with edited image
    await ctx.respond(file=snapchat_caption(io.BytesIO(data), caption)[0])