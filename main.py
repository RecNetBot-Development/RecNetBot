import discord
import sys
import os
import redis
import json
import platform
import logging
from scripts import load_cfg
from rest import Client
from discord.ext import commands
from discord.commands import permissions, Option
from modules.CogManager import CogManager
from rest.wrapper.exceptions import AccountNotFound
from embeds import error_embed

# Setup logger
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Load config
cfg = load_cfg()

# Setup redis
redis_url = cfg['redis_url']
assert redis_url, "Redis database is missing!"
rnb_db = redis.from_url(redis_url)

# RecNet API client
rn_client = Client()

# Setup bot
bot = commands.Bot(command_prefix=cfg['prefix'])
cogManager = CogManager(bot, rnb_db, rn_client)  # include database and client for all cogs to use

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

# Global error handling
@bot.event
async def on_application_command_error(ctx: commands.Context, error):
    raise_error = True
    if isinstance(error.original, AccountNotFound):
        raise_error = False
        
    em = error_embed(ctx, error.original)

    await ctx.respond(embed=em)
    if raise_error: raise error

# Run the bot
bot.run(cfg['token'])