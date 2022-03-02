from tracemalloc import start
from utility import load_cfg, filter_posts
from discord.commands import slash_command, Option # Importing the decorator that makes slash commands.
from embeds import ImageUI
from random import randint

cfg = load_cfg()

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="randomimage",
    description="Find a random image!"
)
async def randomimage(
    self, 
    ctx, 
    type: Option(str, choices=["by", "of"], required=True),
    username: Option(str, "Enter the username", required=True)
):
    await ctx.interaction.response.defer()
    
    post_options = {
        "take": 2**16,
        #"includes": ["creator", "room"]           
    }
    
    if type == "by":
        options = {"posts": post_options}
        user = await self.bot.rec_net.account(name=username, includes=["posts"], options=options)
        posts = user.posts
    else:
        options = {"feed": post_options}
        user = await self.bot.rec_net.account(name=username, includes=["feed"], options=options)
        posts = user.feed
        
    random_index = randint(0, len(posts))
    view, embeds = await ImageUI(ctx=ctx, user=user, posts=posts, interaction=ctx.interaction, start_index=random_index).start()
    await ctx.respond(view=view, embeds=embeds)