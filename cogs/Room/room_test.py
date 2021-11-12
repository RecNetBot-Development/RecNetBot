import requests  # For testing purposes
from scripts import load_cfg
from embeds import room_embed, finalize_embed
from discord.commands import slash_command # Importing the decorator that makes slash commands.

cfg = load_cfg()

@slash_command(guild_ids=[cfg['test_guild_id']]) # Create a slash command for the supplied guilds.
async def room_test(self, ctx, room_id: int, icons: bool = True, explanations: bool = False):
    async def get_room_data(post_id):  # Temporary for testing purposes
        url = f"https://rooms.rec.net/rooms/{room_id}?include=366"
        r = requests.get(url)
        if r.ok:
            return r.json()
        return {}

    room_data = await get_room_data(room_id)
    
    # Test post
    em = await room_embed(room_data, icons, explanations)  # Get embed
    await ctx.respond(embed=await finalize_embed(em, ctx.author))