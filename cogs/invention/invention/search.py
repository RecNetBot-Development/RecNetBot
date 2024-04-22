import discord
from discord.commands import slash_command
from discord.ext.bridge import BridgeOption as Option
from cogs.miscellaneous.search import SearchView
from exceptions import Disabled

@slash_command(
    name="search",
    description="Search for inventions."
)
async def search(
    self, 
    ctx: discord.ApplicationContext, 
    invention: Option(str, name="name", description="Enter RR invention name", required=True)
):
    await ctx.interaction.response.defer()

    # Broken command
    raise Disabled

    view = SearchView(self.bot, invention, "Invention", lock=True)
    em = await view.initialize()
    await ctx.respond(view=view, embed=em)

    
    

        

        
