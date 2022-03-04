from utility import load_cfg
from discord.commands import slash_command # Importing the decorator that makes slash commands.
from embeds import LoadingScreens

cfg = load_cfg()

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="loadingscreens",
    description="View all in-game loading screens!"
)
async def loadingscreens(
    self, 
    ctx
):
    await ctx.interaction.response.defer()
    view, embed = await LoadingScreens(ctx, self.bot.rec_net).start()
    await ctx.respond(embed=embed, view=view)
    