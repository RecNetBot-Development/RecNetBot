import requests  # For testing purposes
from scripts import load_cfg
from discord.commands import slash_command # Importing the decorator that makes slash commands.

cfg = load_cfg()

@slash_command() # Not passing in guild_ids creates a global slash command (might take an hour to register).
async def hi(self, ctx):
    await ctx.respond(f"Hi, this is a global slash command from a cog!")

@slash_command(guild_ids=[cfg['test_guild_id']]) # Create a slash command for the supplied guilds.
async def test(self, ctx, name: str):
    await ctx.respond("hi " + name)