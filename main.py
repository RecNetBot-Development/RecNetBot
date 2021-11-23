import discord
import platform
import os
from discord.ext import commands
from bot import RecNetBot

bot = RecNetBot()

# The code in this even is executed when the bot is ready
@bot.event
async def on_ready():
    print("RNB ONLINE")
    print(f"Logged in as {bot.user.name}")
    print(f"Py-cord version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print()
#TODO: Move to Cog class
# Global error handling
@bot.event
async def on_application_command_error(ctx: commands.Context, error):
    raise_error = False
    if isinstance(error.original, AccountNotFound):
        raise_error = False

    em = error_embed(ctx, error.original)

    await ctx.respond(embed=em, ephemeral=true)
    if raise_error: raise error

# Run the bot
bot.run()