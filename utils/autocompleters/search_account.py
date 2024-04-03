import discord
from recnetpy.dataclasses.account import Account
from recnetpy.rest.exceptions import BadRequest
from typing import List
from database import ConnectionManager
    
async def account_searcher(ctx: discord.AutocompleteContext) -> List[str]:
    """
    Returns a list of matching RR accounts
    """

    query = ctx.value.strip().replace("@", "")
    accounts: List[Account] = []
    if len(query) > 0 and query.isascii():
        try:
            accounts: List[Account] = await ctx.bot.RecNet.accounts.search(query=query)
        except BadRequest:
            accounts = []

    # Check for unlisted accounts
    if accounts:
        account_ids = [acc.id for acc in accounts]
        accounts = await ctx.bot.RecNet.accounts.fetch_many(account_ids)

    # If there's no results, push the linked account first
    if not accounts:
        cm: ConnectionManager = ctx.bot.cm
        linked_account = await cm.get_linked_account(ctx.bot.RecNet, ctx.interaction.user.id)
        return [linked_account.username] if linked_account else []
    
    # Otherwise return results
    return [
        account.username for account in accounts
    ]
