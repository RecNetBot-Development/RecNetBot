import discord
import sys
import os
import json
import platform
import logging
from scripts import load_cfg
from discord.ext import commands
from discord.commands import permissions
from discord.commands import Option
from modules.CogManager import CogManager

# Setup logger
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Load config
cfg = load_cfg()

bot = commands.Bot(command_prefix=cfg['prefix'])
cogManager = CogManager(bot)

# Load cogs
if __name__ == "__main__":
    print("LOADING COGS")
    cogManager.buildCogs()
    print()

# This command is for loading, unloading and reloading cogs!
@bot.slash_command(guild_ids=[cfg['test_guild_id']])  # Only allow this command in the test server!
@permissions.has_role(cfg['dev_role'], guild_id=cfg['test_guild_id'])  # Only allow a developer to use it!
async def cog(
    ctx, 
    cog: Option(str, "Choose cog", choices=bot.cogs.keys()), 
    action: Option(str, "Choose action", choices=["Load", "Unload", "Reload"], default="Reload"),
):
    cog = cog.lower()  # Example -> example (so it can recognize the cog when loading/unloading!)
    info = f"Cog: `{cog}`, Action: `{action}`\n"

    try:
        if action == "Load":
            bot.load_extension(f"cogs.{cog}")
        elif action == "Unload":
            bot.unload_extension(f"cogs.{cog}")
        else:
            bot.unload_extension(f"cogs.{cog}")
            bot.load_extension(f"cogs.{cog}")
    except Exception as e:  # Something went wrong!
        exception = f"`Exception: {type(e).__name__}`, ```{e}```"
        return await ctx.respond(info + exception)  # Returns, which stops code execution

    await ctx.respond(info)

# The code in this even is executed when the bot is ready
@bot.event
async def on_ready():
    print("RNB ONLINE")
    print(f"Logged in as {bot.user.name}")
    print(f"Py-cord version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print()

# The code in this event is executed every time a valid commands catches an error
@bot.event
async def on_command_error(ctx, error):
    raise error

# Run the bot
bot.run(cfg['token'])