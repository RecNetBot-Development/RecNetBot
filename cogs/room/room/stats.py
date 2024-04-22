import discord
from utils.converters import FetchRoom
from discord.commands import slash_command
from discord.ext.bridge import BridgeOption as Option
from utils.autocompleters import room_searcher

"""
async def info(
    self, 
    ctx: discord.ApplicationContext, 
    room: Option(FetchRoom, name="name", description="Enter RR room", required=True),
    only_stats: Option(bool, name="only_stats", description="Whether or not to only display statistics and leave out details", required=False, default=False)
):
"""

@slash_command(
    name="stats",
    description="View a room's statistics only."
)
async def stats(
    self, 
    ctx: discord.ApplicationContext, 
    room: Option(FetchRoom, name="name", description="Enter RR room", required=True, autocomplete=room_searcher),
):
    group = discord.utils.get(self.__cog_commands__, name='room')
    command = discord.utils.get(group.walk_commands(), name='info')
    await command(ctx, room=room, only_stats=True)

    
    

        

        
