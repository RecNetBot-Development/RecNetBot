from json import load
from rest import route_manager as route
from scripts import load_cfg, log
from embeds import room_embed, finalize_embed
from discord.commands import slash_command # Importing the decorator that makes slash commands.

cfg = load_cfg()

@slash_command(guild_ids=[cfg['test_guild_id']]) # Create a slash command for the supplied guilds.
async def room_test(self, ctx, room_id: int, icons: bool = True, explanations: bool = False):
    log(ctx)

    room_data = await self.rn.rooms.rooms(room_id).get({"include": 366}).data
    
    # Test post
    em = await room_embed(room_data, icons, explanations)  # Get embed
    await ctx.respond(embed=await finalize_embed(em, ctx.author))