import discord
from discord.commands import slash_command
from discord.ext.bridge import BridgeOption as Option
from utils.converters import FetchAccount
from utils import format_json_block
from exceptions import ConnectionNotFound, AccountNotFound
from utils.autocompleters import account_searcher
from database import ConnectionManager

@slash_command(
    name="data",
    description="Get raw JSON data of a player."
)
async def data(
    self, 
    ctx: discord.ApplicationContext, 
    account: Option(FetchAccount, name="username", description="Enter RR username", default=None, required=False, autocomplete=account_searcher),
    _id: Option(str, name="id", description="Enter RR account ID instead", default=None, required=False)
):
    await ctx.interaction.response.defer()

    # Prioritize IDs
    if _id:
        account = await ctx.bot.RecNet.accounts.fetch(_id)
        if not account: raise AccountNotFound
        return await ctx.respond(content=format_json_block(account.data))

    if not account:  # Check for a linked RR account
        cm: ConnectionManager = self.bot.cm
        account = await cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound

    await ctx.respond(content=format_json_block(account.data))