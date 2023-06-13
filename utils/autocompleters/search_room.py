import discord
from recnetpy.dataclasses.room import Room
from recnetpy.rest.exceptions import BadRequest
from typing import List
    
async def room_searcher(ctx: discord.AutocompleteContext) -> List[str]:
    """
    Returns a list of matching RR rooms
    """

    try:
        rooms: List[Room] = await ctx.bot.RecNet.rooms.search(query=ctx.value)
    except BadRequest:
        return []

    # Return results
    return [room.name for room in rooms]
