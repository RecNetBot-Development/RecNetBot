import discord
from discord.commands import slash_command, Option
from utils.converters import FetchAccount
from exceptions import ConnectionNotFound

@slash_command(
    name="minmax",
    description="Filter RecNet posts by a minimum or maximum amount of cheers, comments or tags."
)
async def minmax(
    self, 
    ctx: discord.ApplicationContext,
    account: Option(FetchAccount, name="username", description="Enter RR username", default=None, required=False),
    min_cheers: Option(int, name="minimum_cheers", description="Filter out posts that don't have at least this many cheers", default=0, required=False, min_value=0),
    max_cheers: Option(int, name="maximum_cheers", description="Filter out posts that exceed this many cheers", default=10**10, required=False, min_value=0),
    min_comments: Option(int, name="minimum_comments", description="Filter out posts that don't have at least this many comments", default=0, required=False, min_value=0),
    max_comments: Option(int, name="maximum_comments", description="Filter out posts that exceed this many comments", default=10**10, required=False, min_value=0),
    min_tags: Option(int, name="minimum_tags", description="Filter out posts that don't have at least this many tags", default=0, required=False, min_value=0),
    max_tags: Option(int, name="maximum_tags", description="Filter out posts that exceed this many tags", default=10**10, required=False, min_value=0),
):
    if not account:  # Check for a linked RR account
        account = await self.bot.cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
        
    group = discord.utils.get(self.__cog_commands__, name='filter')
    command = discord.utils.get(group.walk_commands(), name='custom')
    await command(
        ctx, 
        taken_by=account,
        min_cheers=min_cheers,
        max_cheers=max_cheers,
        min_comments=min_comments,
        max_comments=max_comments,
        min_tags=min_tags,
        max_tags=max_tags
    )

    
    

        

        
