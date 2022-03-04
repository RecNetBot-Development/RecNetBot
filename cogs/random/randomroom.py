from utility import load_cfg
from discord.commands import slash_command# Importing the decorator that makes slash commands.
from embeds import RandomRoom

cfg = load_cfg()

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="randomroom",
    description="Find a random room!"
)
async def randomroom(
    self, 
    ctx
):
    await ctx.interaction.response.defer()
    view, embed = await RandomRoom(ctx, self.bot.rec_net).start()
    await ctx.respond(embed=embed, view=view)   