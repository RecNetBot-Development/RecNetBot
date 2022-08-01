from email.policy import default
from rec_net.exceptions import RoomNotFound
from utility import load_cfg, respond
from discord.commands import slash_command, Option # Importing the decorator that makes slash commands.
from embeds.room.room_role_embed import room_role_embed

cfg = load_cfg()

@slash_command(
    debug_guilds=cfg['test_guild_ids'],
    name="roles",
    description="Lookup a room's roles and the players who have them."
)
async def roles(
    self,
    ctx,
    name: Option(str, "Enter the room's name", required=True)
):
    await ctx.interaction.response.defer()
    room = await self.bot.rec_net.room(name=name, info=["roles"], includes=["roles", "creator"])
    if not room: raise RoomNotFound(name)
    await respond(ctx, embed=room_role_embed(room))
    