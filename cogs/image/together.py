from utility import load_cfg, respond
from discord.commands import slash_command, Option  # Importing the decorator that makes slash commands.
from base_commands.base_posts import base_posts

cfg = load_cfg()

@slash_command(
    debug_guilds=cfg['test_guild_ids'],
    name="together",
    description="Get all posts where certain users are tagged together."
)
async def filter(
    self, 
    ctx,
    with_users: Option(str, "Tagged users (separate by a space)", required=True)
):
    await ctx.interaction.response.defer()
    view, embeds = await base_posts(self.bot.rec_net, ctx, type="Feed", with_users=with_users, sort="Newest to Oldest")
    await respond(ctx, embeds=embeds, view=view)
