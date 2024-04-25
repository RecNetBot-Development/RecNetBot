import discord
from recnetpy.dataclasses.room import Room
from recnetpy.dataclasses.account import Account
from recnetpy.rest.exceptions import BadRequest
from typing import List
from database import ConnectionManager
from utils import shorten
    
async def room_searcher(ctx: discord.AutocompleteContext) -> List[str]:
    """
    Returns a list of matching RR rooms
    """

    query = ctx.value.strip().replace("^", "")
    rooms: List[Room] = []
    if len(query) > 0 and query.isascii():
        try:
            rooms = await ctx.bot.RecNet.rooms.search(query=query)
        except BadRequest:
            rooms = []

    # Check if the user is linked
    if not rooms and ctx.bot.RecNet:
        cm: ConnectionManager = ctx.bot.cm
        rr_id = await cm.get_discord_connection(ctx.interaction.user.id)
        if rr_id:
            # If they are, show their created rooms
            user: Account = await ctx.bot.RecNet.accounts.fetch(rr_id)
            rooms = await user.get_owned_rooms()
        else:
            # If no rooms, just show hot ones
            rooms = await ctx.bot.RecNet.rooms.hot(take=20)
    
    # Return results
    return [shorten(room.name, 80) for room in rooms]
