import discord
from discord.commands import slash_command, Option
from cogs.miscellaneous.search import SearchView

@slash_command(
    name="search",
    description="Search and view a Rec Room profiles."
)
async def search(
    self, 
    ctx: discord.ApplicationContext, 
    query: Option(str, name="search", description="Enter a RR profile", required=True)
):
    await ctx.interaction.response.defer()

    view = SearchView(self.bot, query, "Account", lock=True)
    em = await view.initialize()
    await ctx.respond(view=view, embed=em)
