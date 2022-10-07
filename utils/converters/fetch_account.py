import discord
from discord.ext import commands
from exceptions import AccountNotFound

class FetchAccount(commands.Converter):
    """
    Converts a username param to a RR account
    """
    async def convert(self, ctx: discord.ApplicationContext, username: str):
        account = await ctx.bot.RecNet.accounts.get(username)
        if not account: raise AccountNotFound
        return account
    
