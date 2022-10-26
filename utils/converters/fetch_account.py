import discord
from discord.ext import commands
from exceptions import AccountNotFound
from recnetpy.dataclasses.account import Account

class FetchAccount(commands.Converter):
    """
    Converts a username param to a RR account
    """
    async def convert(self, ctx: discord.ApplicationContext, account: str | Account):
        if isinstance(account, Account):
            return account
        
        account = await ctx.bot.RecNet.accounts.get(account)
        if not account: raise AccountNotFound
        return account
    
