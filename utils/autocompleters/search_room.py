import discord
from recnetpy.dataclasses.room import Room
from recnetpy.dataclasses.account import Account
from recnetpy.rest.exceptions import BadRequest
from typing import List
    
async def room_searcher(ctx: discord.AutocompleteContext) -> List[str]:
    """
    Returns a list of matching RR rooms
    """

    rooms: List[Room] = []

    try:
        rooms = await ctx.bot.RecNet.rooms.search(query=ctx.value)
    except BadRequest:
        # Check if the user is linked
        check_discord = ctx.bot.cm.get_discord_connection(ctx.interaction.user.id)
        if check_discord:
            # If they are, show their created rooms
            user: Account = await ctx.bot.RecNet.accounts.fetch(check_discord.rr_id)
            rooms = await user.get_owned_rooms()

    # If no rooms, just show hot ones
    if not rooms:
        rooms = await ctx.bot.RecNet.rooms.hot(take=20)

    # Return results
    return [room.name for room in rooms]
