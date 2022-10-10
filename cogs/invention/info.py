import discord
from discord.commands import slash_command, Option
from embeds import invention_embed
from utils.converters import FetchInvention
from cogs.miscellaneous.search import SearchView

@slash_command(
    name="invention",
    description="View a Rec Room invention's details."
)
async def info(
    self, 
    ctx: discord.ApplicationContext, 
    invention: Option(FetchInvention, name="name", description="Enter RR invention", required=True)
):
    await ctx.interaction.response.defer()

    await invention.get_tags()
    em = invention_embed(invention)
    
    await ctx.respond(embed=em)

    
    

        

        
