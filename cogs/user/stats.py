from pstats import Stats
from utility import load_cfg
from discord.commands import slash_command, Option # Importing the decorator that makes slash commands.
from embeds.account.stats.stats_view import StatsView

cfg = load_cfg()

@slash_command(
    debug_guilds=cfg['test_guild_ids'],
    name="stats",
    description="Gather statistics of a user!"
)
async def stats(
    self, 
    ctx, 
    username: Option(str, "Enter user's username", required=True),
):
    view = StatsView(self.bot.rec_net, username)
    await view.respond(ctx)