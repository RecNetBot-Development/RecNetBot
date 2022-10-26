import discord
from discord.commands import slash_command, Option
from utils.converters import FetchInvention
from utils import format_json_block

@slash_command(
    name="data",
    description="View a Rec Room invention's raw API data."
)
async def data(
    self, 
    ctx: discord.ApplicationContext, 
    invention: Option(FetchInvention, name="name", description="Enter a RecNet link or id", required=True)
):
    await ctx.interaction.response.defer()

    await ctx.respond(content=format_json_block(invention.data))