from utility import load_cfg
from discord.commands import slash_command, Option  # Importing the decorator that makes slash commands.
from base_commands.base_posts import base_posts

cfg = load_cfg()

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="latest",
    description="Get a user's latest photo / appearance."
)
async def latest(
    self, 
    ctx, 
    type: Option(str, choices=["Photos", "Feed"], required=True),
    username: Option(str, "Enter the username", required=True),
    raw: Option(bool, "Send raw images", required=False, default=False)
):
    await ctx.interaction.response.defer()
    view, embeds = await base_posts(self.bot.rec_net, ctx, type=type, username=username, sort="Newest to Oldest", raw=raw)
    await ctx.respond(embeds=embeds, view=view)
