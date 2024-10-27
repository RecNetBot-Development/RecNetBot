import discord
import time
from recnetpy.dataclasses.room import Room
from recnetpy.dataclasses.account import Account
from recnetpy.rest.exceptions import BadRequest
from typing import List, Optional
from database import ConnectionManager
from utils import shorten

def format_room_names(rooms: List[Room]) -> List[str]:
    return [shorten(room.name, 80) for room in rooms]

async def room_searcher(ctx: discord.AutocompleteContext) -> List[str]:
    """
    Returns a list of matching RR rooms
    """

    # Sanitize room name
    query = ctx.value.strip().replace("^", "")

    # See if you can find any results with query
    if len(query) > 0 and query.isascii():
        try:
            found_rooms = await ctx.bot.RecNet.rooms.search(query=query)
            return format_room_names(found_rooms)
        except BadRequest:
            ...

    # No query results, see if you can find user's owned rooms
    cm: ConnectionManager = ctx.bot.cm
    # Returns rr_id if user has a verified RR user
    rr_id = await cm.get_discord_connection(ctx.interaction.user.id)
    if rr_id:
        # Display the user's owned rooms if no search results
        user: Account = await ctx.bot.RecNet.accounts.fetch(rr_id)
        owned_rooms = await user.get_owned_rooms()
        return format_room_names(owned_rooms)
        
    # If all else fails, show hot rooms
    hot_rooms = await ctx.bot.RecNet.rooms.hot(take=20)
    return format_room_names(hot_rooms)
