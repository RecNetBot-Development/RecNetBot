from utility import load_cfg, respond
from discord.commands import slash_command, Option  # Importing the decorator that makes slash commands.
from base_commands.base_posts import base_posts

cfg = load_cfg()

@slash_command(
    debug_guilds=cfg['test_guild_ids'],
    name="photos",
    description="Browse a user's shared RecNet photos."
)
async def photos(
    self, 
    ctx,
    username: Option(str, "Enter the username", required=True)
):
    await ctx.interaction.response.defer()
    view, embeds = await base_posts(self.bot.rec_net, ctx, type="Photos", username=username, sort="Newest to Oldest")
    await respond(ctx, embeds=embeds, view=view)