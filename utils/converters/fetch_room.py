import discord
from discord.ext import commands
from exceptions import RoomNotFound

class FetchRoom(commands.Converter):
    """
    Converts a room name param to a RR room
    """
    async def convert(self, ctx: discord.ApplicationContext, room_name: str):
        # Sanitize input
        room_name = room_name.strip().replace("^", "")
        
        room = await ctx.bot.RecNet.rooms.get(room_name, 78)
        if not room: raise RoomNotFound
        #ctx.bot.rcm.cache_stats(ctx.author.id, room.id, room)
        return room
    
