import discord
from resources import get_emoji
from recnetpy.dataclasses.account import Account
from discord.commands import slash_command, Option # Importing the decorator that makes slash commands.

@slash_command(
    name="profile",
    description="The base command for RecNet profiles."
)
async def profile(
    self, 
    ctx: discord.ApplicationContext, 
    username: Option(str, "Enter RR username", required=True)
):
    await ctx.respond(username)

        
