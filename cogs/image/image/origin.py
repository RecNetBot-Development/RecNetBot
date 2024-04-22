import discord
from discord.commands import slash_command
from discord.ext.bridge import BridgeOption as Option
from utils.converters import FetchImage
from embeds import fetch_image_embed

@slash_command(
    name="origin",
    description="Find a public post by its RecNet link, id, img.rec.net link or image name."
)
async def origin(
    self, 
    ctx: discord.ApplicationContext, 
    image: Option(FetchImage, name="image", description="Enter a RecNet link, ID, img.rec.net link or image name.", required=True)
):
    await ctx.interaction.response.defer()

    em = await fetch_image_embed(image)
    await ctx.respond(embed=em)