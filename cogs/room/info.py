import discord
from utils.converters import FetchRoom
from discord.commands import slash_command, Option
from embeds import room_embed

@slash_command(
    name="room",
    description="View a Rec Room room's information and statistics."
)
async def info(
    self, 
    ctx: discord.ApplicationContext, 
    room: Option(FetchRoom, name="name", description="Enter RR room", required=True)
):
    await ctx.interaction.response.defer()
    
    # Get and cache stats
    cached_stats = self.bot.rcm.get_cached_stats(ctx.author.id, room.id)
    if cached_stats:
        self.bot.rcm.update_cached_stats(ctx.author.id, room.id, room)
    else:
        self.bot.rcm.cache_stats(ctx.author.id, room.id, room)

    await ctx.respond(embed=room_embed(room, cached_stats))

    
    

        

        
