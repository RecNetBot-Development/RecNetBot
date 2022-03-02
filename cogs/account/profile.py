from base_commands.base_posts import base_posts
from utility import load_cfg
from discord.commands import slash_command, Option # Importing the decorator that makes slash commands.
from base_commands.base_profile import base_profile

cfg = load_cfg()

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="profile",
    description="The base command for RecNet profiles."
)
async def profile(
    self, 
    ctx, 
    username: Option(str, "Enter user's username", required=True),
    specified: Option(str, "Choose specific information", choices=["Profile", "Profile Picture", "Banner", "Platforms", "Bio", "Junior", "Level"], required=False, default="Profile")
):
    await ctx.interaction.response.defer()
    embed, view = await base_profile(self.bot.rec_net, ctx, username, specified)
    await ctx.respond(embed=embed, view=view)
