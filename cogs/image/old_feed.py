import discord
from discord.commands import slash_command
from discord.ext.bridge import BridgeOption as Option
from utils.converters import FetchAccount
from exceptions import ConnectionNotFound
from utils.autocompleters import account_searcher
from exceptions import Disabled

@slash_command(
    name="feed",
    description="Browse through a player's RecNet feed."
)
async def feed(
    self, 
    ctx: discord.ApplicationContext,
    account: Option(FetchAccount, name="username", description="Enter RR username", default=None, required=False, autocomplete=account_searcher)
):
    # Broken command
    raise Disabled

    if not account:  # Check for a linked RR account
        account = await self.bot.cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
    
    group = discord.utils.get(self.__cog_commands__, name='filter')
    command = discord.utils.get(group.walk_commands(), name='custom')
    await command(ctx, together=account.username)

    
    

        

        
