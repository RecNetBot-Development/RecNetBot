from base_commands.base_posts import base_posts
from utility import load_cfg, respond
from discord.commands import slash_command, Option # Importing the decorator that makes slash commands.
from base_commands.base_profile import base_profile
from owoify import owoify
from owoify.owoify import Owoness

cfg = load_cfg()

@slash_command(
    debug_guilds=cfg['test_guild_ids'],
    name="owoify",
    description=owoify("The base command for RecNet profiles.", Owoness.Owo)
)
async def owoify(
    self, 
    ctx, 
    username: Option(str, owoify("Enter user's username", Owoness.Owo), required=True),
):
    await ctx.interaction.response.defer()
    embed, view = await base_profile(self.bot.rec_net, ctx, username, owo=True)
    await respond(ctx, embed=embed, view=view)
