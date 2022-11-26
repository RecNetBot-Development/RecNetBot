import discord
import json
from discord.commands import slash_command, Option
from utils.converters import FetchEvent
from utils import format_json_block

@slash_command(
    name="data",
    description="Get raw JSON data of an event."
)
async def data(
    self, 
    ctx: discord.ApplicationContext, 
    event: Option(FetchEvent, name="event", description="Enter a RecNet link or id", required=True)
):
    await ctx.interaction.response.defer()

    await ctx.respond(content=format_json_block(event.data))