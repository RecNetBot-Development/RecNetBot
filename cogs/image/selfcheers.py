from rec_net.exceptions import AccountNotFound
from utility import load_cfg, respond
from discord.commands import slash_command, Option  # Importing the decorator that makes slash commands.
from discord.utils import MISSING
from embeds import self_cheers_embed
from embeds import ImageUI
import time

cfg = load_cfg()

@slash_command(
    debug_guilds=cfg['test_guild_ids'],
    name="selfcheers",
    description="Get self-cheered posts by a user."
)
async def selfcheers(
    self, 
    ctx,
    username: Option(str, "Enter the username", required=True)
):
    await ctx.interaction.response.defer()
    posts_options = {
        "includes": ["cheers"],
        "take": 2**16           
    }
    start_time = time.perf_counter()
    user = await self.bot.rec_net.account(name=username, includes=["posts"], options={"posts": posts_options})
    if not user: raise AccountNotFound(username)
    
    self_cheers, self_cheered_posts = 0, []
    for post in user.posts:
        if user.id in post.cheers: 
            self_cheers += 1
            self_cheered_posts.append(post)
    end_time = time.perf_counter()
    
    image_ui_view = MISSING
    if self_cheered_posts:
        image_ui_view, embeds = await ImageUI(ctx=ctx, user=user, posts=self_cheered_posts, interaction=ctx.interaction, original_embeds=[self_cheers_embed(ctx, user, self_cheers)], rec_net=self.bot.rec_net).start()
    else:
        embeds = [self_cheers_embed(ctx, user, self_cheers)]
    await respond(ctx, content=f"Time elapsed: `{round(end_time-start_time, 2)}s`", embeds=embeds, view=image_ui_view)