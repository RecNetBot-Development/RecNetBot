import discord
from discord.commands import slash_command, Option
from utils.converters import FetchImage
from utils import format_json_block

@slash_command(
    name="data",
    description="View a Rec Room image's raw API data."
)
async def data(
    self, 
    ctx: discord.ApplicationContext, 
    image: Option(FetchImage, name="image", description="Enter a RecNet link or id, img.rec.net link or image name", required=True)
):
    await ctx.interaction.response.defer()

    await ctx.respond(content=format_json_block(image.data))