import discord
from discord.commands import slash_command, Option
from utils.converters import FetchRoom
from utils import format_json_block

@slash_command(
    name="data",
    description="View a Rec Room room's raw API data."
)
async def data(
    self, 
    ctx: discord.ApplicationContext, 
    room: Option(FetchRoom, name="name", description="Enter RR room", required=True)
):
    await ctx.interaction.response.defer()

    # Make sure there's enough characters to post
    remove = ("Roles", "SubRooms", "Scores")
    for key in remove:
        room.data.pop(key)

    await ctx.respond(content=format_json_block(room.data))