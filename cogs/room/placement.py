import discord
from utility import load_cfg
from discord.commands import slash_command, Option # Importing the decorator that makes slash commands.
from base_commands.base_api import base_api
from rec_net.exceptions import RoomNotFound
from utility.discord_helpers.helpers import respond
from embeds.error_embed import error_embed
from embeds.room.placement_embed import placement_embed

cfg = load_cfg()

def separate_tags(_filter):
        return "#" in _filter
    
def separate_keywords(_filter):
    return "#" not in _filter

@slash_command(
    debug_guilds=cfg['test_guild_ids'],
    name="placement",
    description="Check what placement your room is in!"
)
async def placement(
    self, 
    ctx, 
    name: Option(str, "Enter the room's name", required=True),
    specify: Option(str, "Enter any #tags or keywords to filter results (separate by space)", required=False)
):
    room = await self.bot.rec_net.room(name=name, info=["tags"])
    if not room: raise RoomNotFound(name)
    if specify:
        room_resp = await self.bot.rec_net.rec_net.rooms.rooms.search.get(params={"query": specify}).fetch()
    else:
        room_resp = await self.bot.rec_net.rec_net.rooms.rooms.hot.get().fetch()
        
    rooms = room_resp.data['Results']
    
    tags, keywords = None, None
    if specify: 
        split_filters = specify.split(",")
        tags = ' '.join(list(filter(separate_tags, split_filters)))
        keywords = ' '.join(list(filter(separate_keywords, split_filters)))
        
        tags = tags if tags else 'None!'
        keywords = keywords if keywords else 'None!'
    
    if not rooms: 
        return await respond(
            ctx, 
            embed=error_embed(
                error=None,
                custom_text=f"No room found with specified keywords and #tags!\nTags: `{tags}`\nKeywords: `{keywords}`"
            )
        )
        
    index = [i for i in range(len(rooms)) if rooms[i]["Name"] == room.name] 
        
    if not index: 
        return await respond(
            ctx, 
            embed=error_embed(
                error=None,
                custom_text=f"""
Couldn't find `^{room.name}` from the hot page! Check your keywords and tags.\nTags: `{tags}`\nKeywords: `{keywords}`
                """
            )
        )
        
    
        
    await respond(
        ctx, 
        embed=placement_embed(room, index[0]+1, tags, keywords)
    )