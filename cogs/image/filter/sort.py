import discord
from discord.commands import slash_command, Option
from utils.converters import FetchAccount
from exceptions import ConnectionNotFound
from utils.autocompleters import account_searcher

@slash_command(
    name="sort",
    description="Sort a player's posts by cheers, comments, tags or date and browse through them."
)
async def sort(
    self, 
    ctx: discord.ApplicationContext,
    _sort: Option(str, name="sort", description="Choose what to sort by", required=True, choices=[
        "Oldest to Newest", 
        "Cheers: Highest to Lowest",
        "Comments: Highest to Lowest",
        "Tags: Highest to Lowest",
    ]),
    account: Option(FetchAccount, name="username", description="Enter RR username", default=None, required=False, autocomplete=account_searcher)
):
    if not account:  # Check for a linked RR account
        account = await self.bot.cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
    
    group = discord.utils.get(self.__cog_commands__, name='filter')
    command = discord.utils.get(group.walk_commands(), name='custom')
    await command(ctx, _sort=_sort, taken_by=account)

    
    

        

        
