import discord
from discord.commands import slash_command, Option
from cogs.miscellaneous.search import SearchView

@slash_command(
    name="search",
    description="Search and view a Rec Room rooms."
)
async def search(
    self, 
    ctx: discord.ApplicationContext, 
    query: Option(str, name="search", description="Enter a RR room", required=True)
):
    await ctx.interaction.response.defer()

    view = SearchView(self.bot, query, "Room", lock=True)
    em = await view.initialize()
    await ctx.respond(view=view, embed=em)
