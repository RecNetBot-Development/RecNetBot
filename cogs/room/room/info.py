import discord
from utils.converters import FetchRoom
from discord.commands import slash_command, Option
from embeds import room_embed

@slash_command(
    name="info",
    description="View a Rec Room room's information and statistics."
)
async def info(
    self, 
    ctx: discord.ApplicationContext, 
    room: Option(FetchRoom, name="name", description="Enter RR room", required=True),
    only_stats: Option(bool, name="only_stats", description="Whether or not to only display statistics and leave out details", required=False, default=False)
):
    await ctx.interaction.response.defer()
    
    cached_stats = self.bot.rcm.get_cached_stats(ctx.author.id, room.id)
    self.bot.rcm.cache_stats(ctx.author.id, room.id, room)

    await ctx.respond(embed=room_embed(room, cached_stats, only_stats))

    
    

        

        