import discord
from discord.commands import slash_command, Option
from utils.converters import FetchAccount
from exceptions import ConnectionNotFound

@slash_command(
    name="in",
    description="Filter RecNet posts by in which rooms the photos are taken."
)
async def _in(
    self, 
    ctx: discord.ApplicationContext,
    rooms: Option(str, name="rooms", description="Filter by which RR rooms can be featured (separate by spaces)", required=True),
    exclude: Option(str, name="exclude_rooms", description="Filter by which RR rooms SHOULDN'T be featured (separate by spaces)", required=True),
    account: Option(FetchAccount, name="username", description="Enter RR username", default=None, required=False)
):
    if not account:  # Check for a linked RR account
        account = await self.bot.cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
    
    group = discord.utils.get(self.__cog_commands__, name='filter')
    command = discord.utils.get(group.walk_commands(), name='custom')
    await command(ctx, rooms=rooms, exclude_rooms=exclude, taken_by=account)

    
    

        

        
