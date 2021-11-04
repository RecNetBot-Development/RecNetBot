import discord
import sys
import os
import json
import platform
from funcs import load_cfg
from discord.ext import commands
from discord.errors import ExtensionAlreadyLoaded, ExtensionNotLoaded
from discord.commands import permissions
from discord.commands import Option

# Load config
cfg = load_cfg()

bot = commands.Bot(command_prefix=cfg['prefix'])

# Load cogs
if __name__ == "__main__":
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension '{extension}'\n{exception}")


@bot.slash_command(guild_ids=[cfg['test_guild_id']])
@permissions.has_role(cfg['dev_role'], guild_id=cfg['test_guild_id'])
async def cog(
    ctx, 
    cog: Option(str, "Choose cog", choices=bot.cogs.keys()), 
    action: Option(str, "Choose action", choices=["Load", "Unload", "Reload"], default="Reload"),
):
    cog = cog.lower()
    info = f"Cog: `{cog}`, Action: `{action}`\n"

    try:
        if action == "Load":
            bot.load_extension(f"cogs.{cog}")
        elif action == "Unload":
            bot.unload_extension(f"cogs.{cog}")
        else:
            bot.unload_extension(f"cogs.{cog}")
            bot.load_extension(f"cogs.{cog}")
    except Exception as e:
        exception = f"`Exception: {type(e).__name__}`, ```{e}```"
        return await ctx.respond(info + exception)

    await ctx.respond(info)

# The code in this even is executed when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Py-cord version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")

# The code in this event is executed every time a valid commands catches an error
@bot.event
async def on_command_error(ctx, error):
    raise error

# Run the bot
bot.run(cfg['token'])
