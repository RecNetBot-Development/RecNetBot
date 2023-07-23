import discord
from discord.ext import commands
from exceptions import AccountNotFound
from recnetpy.dataclasses.account import Account

class FetchAccount(commands.Converter):
    """
    Converts a username param to a RR account
    """
    async def convert(self, ctx: discord.ApplicationContext, _account: str | Account):
        if isinstance(_account, Account):
            return _account
        
        # Sanitize input
        account_name = _account.strip().replace("@", "")
        
        if account_name and account_name.isascii():
            account = await ctx.bot.RecNet.accounts.get(account_name)
        else:
            account = None

        if not account: raise AccountNotFound(_account)
        return account
    
