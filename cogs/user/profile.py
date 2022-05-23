from base_commands.base_posts import base_posts
from utility import load_cfg, respond
from discord.commands import slash_command, Option # Importing the decorator that makes slash commands.
from base_commands.base_profile import base_profile

cfg = load_cfg()

@slash_command(
    debug_guilds=cfg['test_guild_ids'],
    name="profile",
    description="The base command for RecNet profiles."
)
async def profile(
    self, 
    ctx, 
    username: Option(str, "Enter user's username", required=True),
    specified: Option(str, "Choose specific information", choices=["profile", "profile picture", "banner", "platforms", "bio", "junior", "level", "identities", "pronouns"], required=False, default="Profile")
):
    await ctx.interaction.response.defer()
    embed, view = await base_profile(self.bot.rec_net, ctx, username, specified.capitalize())
    await respond(ctx, embed=embed, view=view)
