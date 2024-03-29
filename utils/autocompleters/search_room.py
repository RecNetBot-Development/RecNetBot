import discord
from recnetpy.dataclasses.room import Room
from recnetpy.dataclasses.account import Account
from recnetpy.rest.exceptions import BadRequest
from typing import List
    
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
        check_discord = ctx.bot.cm.get_discord_connection(ctx.interaction.user.id)
        if check_discord:
            # If they are, show their created rooms
            user: Account = await ctx.bot.RecNet.accounts.fetch(check_discord.rr_id)
            rooms = await user.get_owned_rooms()
        else:
            # If no rooms, just show hot ones
            rooms = await ctx.bot.RecNet.rooms.hot(take=20)
    
    # Return results
    return [room.name for room in rooms]
