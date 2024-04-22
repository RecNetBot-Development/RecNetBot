import discord
from discord.commands import slash_command
from discord.ext.bridge import BridgeOption as Option
from utils.converters import FetchInvention
from utils import format_json_block
from exceptions import Disabled

@slash_command(
    name="data",
    description="Get raw JSON data of an event."
)
async def data(
    self, 
    ctx: discord.ApplicationContext, 
    invention: Option(FetchInvention, name="name", description="Enter a RecNet link or ID", required=True)
):
    await ctx.interaction.response.defer()

    # Broken command
    raise Disabled

    await ctx.respond(content=format_json_block(invention.data))