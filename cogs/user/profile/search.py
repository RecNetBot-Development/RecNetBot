import discord
from discord.commands import slash_command, Option
from cogs.miscellaneous.search import SearchView
from utils.autocompleters import account_searcher

@slash_command(
    name="search",
    description="Search for players."
)
async def search(
    self, 
    ctx: discord.ApplicationContext, 
    query: Option(str, name="search", description="Enter a RR profile", required=True, autocomplete=account_searcher)
):
    await ctx.interaction.response.defer()

    view = SearchView(self.bot, query, "Account", lock=True)
    em = await view.initialize()
    await ctx.respond(view=view, embed=em)
