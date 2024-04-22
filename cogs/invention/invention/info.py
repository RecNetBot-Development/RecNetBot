import discord
from discord.commands import slash_command
from discord.ext.bridge import BridgeOption as Option
from utils.converters import FetchInvention
from embeds import fetch_invention_embed
from exceptions import Disabled

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

    # Broken command
    raise Disabled

    cached_stats = self.bot.icm.get_cached_stats(ctx.author.id, invention.id)
    self.bot.icm.cache_stats(ctx.author.id, invention.id, invention)
        
    em = await fetch_invention_embed(invention, cached_stats)
        
    await ctx.respond(embed=em)

    
    

        

        
