import discord
from discord.commands import slash_command, Option

@slash_command(
    name="together",
    description="Filter RecNet posts by who are tagged in them."
)
async def together(
    self, 
    ctx: discord.ApplicationContext,
    together: Option(str, name="together", description="Filter by which RR users are featured in a post (separate by spaces)", required=True),
    exclude: Option(str, name="exclude", description="Filter by which RR users SHOULDN'T be featured in a post (separate by spaces)", required=False, default=None)
):
    group = discord.utils.get(self.__cog_commands__, name='filter')
    command = discord.utils.get(group.walk_commands(), name='custom')
    await command(ctx, together=together, exclude_together=exclude)

    
    

        

        
