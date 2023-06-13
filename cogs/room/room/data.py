import discord
from discord.commands import slash_command, Option
from utils.converters import FetchRoom
from utils import format_json_block, shorten
from utils.autocompleters import room_searcher

@slash_command(
    name="data",
    description="Get raw JSON data of a room."
)
async def data(
    self, 
    ctx: discord.ApplicationContext, 
    room: Option(FetchRoom, name="name", description="Enter RR room", required=True, autocomplete=room_searcher)
):
    await ctx.interaction.response.defer()

    # Make sure there's enough characters to post
    remove = ("Roles", "SubRooms", "Scores")
    for key in remove:
        room.data.pop(key)

    json_block = format_json_block(room.data)
    if len(json_block) > 2000:
        shortened = shorten(json_block, 1950)[:-2] 
        json_block = shortened + "...\n}```Cut off short due to the amount of data."

    await ctx.respond(content=json_block)