import discord
from recnetpy.dataclasses.account import Account
from recnetpy.rest.exceptions import BadRequest
from typing import List
    
async def account_searcher(ctx: discord.AutocompleteContext) -> List[str]:
    """
    Returns a list of matching RR accounts
    """

    accounts: List[Account] = []
    if len(ctx.value) > 0:
        try:
            accounts: List[Account] = await ctx.bot.RecNet.accounts.search(query=ctx.value)
        except BadRequest:
            accounts = []

    # If there's no results, push the linked account first
    if not accounts:
        linked_account = await ctx.bot.cm.get_linked_account(ctx.bot.RecNet, ctx.interaction.user.id)
        return [linked_account.username] if linked_account else []

    # Otherwise return results
    return [
        f"@{account.username}" for account in accounts
    ]
