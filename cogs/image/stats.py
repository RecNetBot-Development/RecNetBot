from scripts import load_cfg
from discord.commands import slash_command, Option # Importing the decorator that makes slash commands.
from embeds import stats_embed, loading_embed

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
    msg = await ctx.respond(embed=loading_embed(ctx))
    post_options = {
        "take": 2**16           
    }
    feed_options = {
        "take": 2**16           
    }
    user = await self.bot.rec_net.account(name=username, includes=["posts", "feed"], options={"posts": post_options, "feed": feed_options})
    await msg.edit_original_message(embed=stats_embed(ctx, user))
    

