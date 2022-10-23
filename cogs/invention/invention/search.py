import discord
from discord.commands import slash_command, Option
from cogs.miscellaneous.search import SearchView

@slash_command(
    name="search",
    description="Search and view a Rec Room invention's details and statistics."
)
async def search(
    self, 
    ctx: discord.ApplicationContext, 
    invention: Option(str, name="name", description="Enter RR invention name", required=True)
):
    await ctx.interaction.response.defer()

    view = SearchView(self.bot, invention, "Invention", lock=True)
    em = await view.initialize()
    await ctx.respond(view=view, embed=em)

    
    

        

        
