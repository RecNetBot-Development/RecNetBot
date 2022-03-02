from utility import load_cfg
from discord.commands import slash_command, Option # Importing the decorator that makes slash commands.
from embeds import room_embed

cfg = load_cfg()

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="room",
    description="Lookup a room and see details about it!"
)
async def room(
    self,
    ctx,
    name: Option(str, "Enter the room's name", required=True)
):
    await ctx.interaction.response.defer()
    room = await self.bot.rec_net.room(name=name, info=["tags", "subrooms", "roles", "scores"], includes=["roles", "creator"])
    hot_rooms = await self.bot.rec_net.rec_net.rooms.rooms.hot.get(params={"take": 1000}).fetch()
    await ctx.respond(embed=room_embed(ctx, room, hot_rooms.data['Results']))
    