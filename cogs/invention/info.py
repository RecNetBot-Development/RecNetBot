import discord
from discord.commands import slash_command, Option
from utils.converters import FetchInvention
from embeds import fetch_invention_embed

@slash_command(
    name="invention",
    description="Search and view a Rec Room invention's details and statistics."
)
async def info(
    self, 
    ctx: discord.ApplicationContext, 
    invention: Option(FetchInvention, name="name", description="Enter RR invention name", required=True)
):
    await ctx.interaction.response.defer()

    #view = SearchView(self.bot, invention, "Invention", lock=True)
    #em = await view.initialize()
    cached_stats = self.bot.icm.get_cached_stats(ctx.author.id, invention.id)
    if cached_stats:
        self.bot.icm.update_cached_stats(ctx.author.id, invention.id, invention)
    else:
        self.bot.icm.cache_stats(ctx.author.id, invention.id, invention)
        
    em = await fetch_invention_embed(invention, cached_stats)
        
    await ctx.respond(embed=em)

    
    

        

        
