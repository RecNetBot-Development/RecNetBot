from rec_net.exceptions import RoomNotFound
from utility import load_cfg, respond
from discord.commands import slash_command, Option # Importing the decorator that makes slash commands.
from embeds import room_embed

cfg = load_cfg()

@slash_command(
    debug_guilds=cfg['test_guild_ids'],
    name="info",
    description="Lookup a room and see details about it!"
)
async def info(
    self,
    ctx,
    name: Option(str, "Enter the room's name", required=True)
):
    await ctx.interaction.response.defer()
    room = await self.bot.rec_net.room(name=name, info=["tags", "subrooms", "roles", "scores"], includes=["roles", "creator"])
    if not room: raise RoomNotFound(name)
    hot_rooms = await self.bot.rec_net.rec_net.rooms.rooms.hot.get(params={"take": 1000}).fetch()
    await respond(ctx, embed=room_embed(room, hot_rooms.data['Results']))
    