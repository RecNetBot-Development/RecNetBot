import discord
from discord.commands import slash_command, Option
from utils.converters import FetchAccount
from exceptions import ConnectionNotFound

@slash_command(
    name="in",
    description="Browse posts taken in specified rooms."
)
async def _in(
    self, 
    ctx: discord.ApplicationContext,
    rooms: Option(str, name="rooms", description="Filter by which RR rooms can be featured (separate by spaces)", required=False, default=None),
    exclude: Option(str, name="exclude", description="Filter by which RR rooms SHOULDN'T be featured (separate by spaces)", required=False, default=None),
    account: Option(FetchAccount, name="username", description="Enter RR username", default=None, required=False)
):
    if any((rooms, exclude)):
        await ctx.interaction.response.send_message("Fill in `rooms` or `exclude` params!", ephemeral=True)
        return
    
    if not account:  # Check for a linked RR account
        account = await self.bot.cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
    
    group = discord.utils.get(self.__cog_commands__, name='filter')
    command = discord.utils.get(group.walk_commands(), name='custom')
    await command(ctx, rooms=rooms, exclude_rooms=exclude, taken_by=account)

    
    

        

        
