import discord
from discord.commands import slash_command, Option
from utils.converters import FetchAccount
from exceptions import ConnectionNotFound

@slash_command(
    name="during",
    description="Filter RecNet posts by in which event they were taken in."
)
async def during(
    self, 
    ctx: discord.ApplicationContext,
    events: Option(str, name="events", description="Filter by which RR events can be featured (separate by spaces, enter event ids)", required=False, default=None),
    exclude: Option(str, name="exclude", description="Filter by which RR rooms SHOULDN'T be featured (separate by spaces, enter event ids)", required=False, default=None),
    account: Option(FetchAccount, name="username", description="Enter RR username", default=None, required=False)
):
    if any((events, exclude)):
        await ctx.interaction.response.send_message("Fill in `events` or `exclude` params!", ephemeral=True)
        return
    
    if not account:  # Check for a linked RR account
        account = await self.bot.cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
    
    group = discord.utils.get(self.__cog_commands__, name='filter')
    command = discord.utils.get(group.walk_commands(), name='custom')
    await command(ctx, events=events, exclude_events=exclude, taken_by=account)

    
    

        

        
