import discord
from discord.commands import slash_command, Option
from utils.converters import FetchInvention
from embeds import fetch_invention_embed

@slash_command(
    name="info",
    description="View an invention's details and statistics."
)
async def info(
    self, 
    ctx: discord.ApplicationContext, 
    invention: Option(FetchInvention, name="name", description="Enter a RecNet link or ID", required=True)
):
    await ctx.interaction.response.defer()

    cached_stats = self.bot.icm.get_cached_stats(ctx.author.id, invention.id)
    self.bot.icm.cache_stats(ctx.author.id, invention.id, invention)
        
    em = await fetch_invention_embed(invention, cached_stats)
        
    await ctx.respond(embed=em)

    
    

        

        
