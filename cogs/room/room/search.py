import discord
from discord.commands import slash_command
from discord.ext.bridge import BridgeOption as Option
from cogs.miscellaneous.search import SearchView
from utils.autocompleters import room_searcher

@slash_command(
    name="search",
    description="Search for rooms."
)
async def search(
    self, 
    ctx: discord.ApplicationContext, 
    query: Option(str, name="search", description="Enter a RR room", required=True, autocomplete=room_searcher)
):
    await ctx.interaction.response.defer()

    view = SearchView(self.bot, query, "Room", lock=True)
    em = await view.initialize()
    await ctx.respond(view=view, embed=em)
