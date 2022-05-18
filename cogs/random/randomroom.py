from utility import load_cfg, respond
from discord.commands import slash_command# Importing the decorator that makes slash commands.
from embeds import RandomRoom

cfg = load_cfg()

@slash_command(
    debug_guilds=cfg['test_guild_ids'],
    name="room",
    description="Find a random room!"
)
async def randomroom(
    self, 
    ctx
):
    await ctx.interaction.response.defer()
    view, embed = await RandomRoom(ctx, self.bot.rec_net).start()
    await respond(ctx, embed=embed, view=view)   