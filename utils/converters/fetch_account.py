import discord
from discord.ext import commands
from exceptions import AccountNotFound
from recnetpy.dataclasses.account import Account
from database import ConnectionManager

class FetchAccount(commands.Converter):
    """
    Converts a username param to a RR account
    """
    async def convert(self, ctx: discord.ApplicationContext, _account: str | Account):
        if isinstance(_account, Account):
            return _account
        
        # Check if Discord mention
        if _account.startswith("<@") and _account.endswith(">"):
            # This should be a Discord mention!
            discord_id = _account.split("<@")[1].split(">")[0]
            cm: ConnectionManager = ctx.bot.cm
            linked_account = await cm.get_linked_account(ctx.bot.RecNet, discord_id)
            if not linked_account: raise AccountNotFound(_account)
            return linked_account
        else:
            # Sanitize input
            account_name = _account.strip().replace("@", "")
            
            if account_name and account_name.isascii():
                account = await ctx.bot.RecNet.accounts.get(account_name)
            else:
                account = None

            if not account: raise AccountNotFound(_account)
            return account
    
