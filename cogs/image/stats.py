from utility import load_cfg
from discord.commands import slash_command, Option # Importing the decorator that makes slash commands.
from embeds import stats_embed

cfg = load_cfg()

@slash_command(
    guild_ids=[cfg['test_guild_id']],
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
    await ctx.respond(embed=stats_embed(ctx, user))
    

