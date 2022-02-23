from utility import load_cfg
from discord.commands import slash_command, Option  # Importing the decorator that makes slash commands.
from rec_net.exceptions import Error
from embeds import json_embed

cfg = load_cfg()

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="roomdata",
    description="Get raw room data from the API."
)
async def roomdata(
    self, 
    ctx, 
    room_input_type: Option(str, choices=["Room Name", "Id"], required=True),
    room: Option(str, "Enter the room", required=True)
):
    await ctx.interaction.response.defer()
    host = "https://rooms.rec.net"
    if room_input_type == "Id":
        if not room.isdigit(): raise InvalidRoomId("Room id must be a digit!")  
        parsed_room_id = int(room)
        room_resp = await self.bot.rec_net.rec_net.rooms.rooms(parsed_room_id).get().fetch()
        endpoint = f"/rooms/{parsed_room_id}"
    else:
        room_resp = await self.bot.rec_net.rec_net.rooms.rooms().get({"name": room}).fetch()
        endpoint = f"/rooms?name={room}"

    await ctx.respond(
        content = host + endpoint,
        embed=json_embed(ctx, room_resp.data)
    )

class InvalidRoomId(Error):
    ...


class RoomNotFound(Error):
    ...