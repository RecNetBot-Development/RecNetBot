from rec_net.exceptions import AccountNotFound
from utility import load_cfg, respond
from discord.commands import slash_command, Option # Importing the decorator that makes slash commands.
from embeds import stats_embed

cfg = load_cfg()

@slash_command(
    debug_guilds=cfg['test_guild_ids'],
    name="stats",
    description="View a user's RecNet stats."
)
async def stats(
    self, 
    ctx, 
    username: Option(str, "Enter user's username", required=True)
):
    await ctx.interaction.response.defer()
    post_options = {
        "take": 2**16           
    }
    feed_options = {
        "take": 2**16           
    }
    user = await self.bot.rec_net.account(name=username, includes=["posts", "feed"], options={"posts": post_options, "feed": feed_options})
    if not user: raise AccountNotFound(username)
    await respond(ctx, embed=stats_embed(user))
    

