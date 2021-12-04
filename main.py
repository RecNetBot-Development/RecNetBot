import discord
import platform
import os
from bot import RecNetBot

bot = RecNetBot()

# The code in this event is executed when the bot is ready
@bot.event
async def on_ready():
    print()
    print("RNB ONLINE")
    print(f"Logged in as {bot.user.name}")
    print(f"PyCord version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print()

# Run the bot
bot.run()