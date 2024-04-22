import discord
from discord.commands import slash_command
from discord.ext.bridge import BridgeOption as Option
from utils.converters import FetchRoom
from utils import format_json_block, shorten
from utils.autocompleters import room_searcher
from exceptions import RoomNotFound
from embeds import get_default_embed

@slash_command(
    name="data",
    description="Get raw JSON data of a room."
)
async def data(
    self, 
    ctx: discord.ApplicationContext, 
    room: Option(FetchRoom, name="name", description="Enter RR room", required=False, autocomplete=room_searcher),
    _id: Option(int, name="id", description="Enter room ID instead", default=None, required=False)
):
    await ctx.interaction.response.defer()

    if not room and not _id:
        em = get_default_embed()
        em.description = "Please fill either `room` or `id` parameter."
        return await ctx.respond(embed=em)

    # Prioritize IDs
    if _id:
        room = await ctx.bot.RecNet.rooms.fetch(_id)
        if not room: raise RoomNotFound
    
    # Make sure there's enough characters to post
    remove = ("Roles", "SubRooms", "Scores")
    for key in remove:
        if key in room.data:
            room.data.pop(key)

    json_block = format_json_block(room.data)
    if len(json_block) > 2000:
        shortened = shorten(json_block, 1950)[:-2] 
        json_block = shortened + "...\n}```Cut off short due to the amount of data."

    await ctx.respond(content=json_block)