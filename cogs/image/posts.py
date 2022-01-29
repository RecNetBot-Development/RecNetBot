from scripts import load_cfg, img_url
from discord.commands import slash_command, Option, SlashCommandGroup # Importing the decorator that makes slash commands.
from embeds import image_embed
from scripts import img_url

cfg = load_cfg()

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="posts",
    description="View a user's RecNet posts."
)
async def posts(
    self, 
    ctx, 
    username: Option(str, "Enter user's username", required=True)
):
    user = await self.bot.rec_net.account(name=username, includes=["posts"])
    await ctx.respond(embed=image_embed(ctx, user.posts[0]))
    

