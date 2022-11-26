import discord
from utils.converters import FetchRoom
from discord.commands import slash_command, Option
from embeds import room_embed
from bot import RecNetBot
from recnetpy.dataclasses.room import Room
from exceptions import RoomNotFound

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
    description="View a Rec Room room's statistics only."
)
async def stats(
    self, 
    ctx: discord.ApplicationContext, 
    room: Option(FetchRoom, name="name", description="Enter RR room", required=True),
):
    group = discord.utils.get(self.__cog_commands__, name='room')
    command = discord.utils.get(group.walk_commands(), name='info')
    await command(ctx, room=room, only_stats=True)

    
    

        

        
