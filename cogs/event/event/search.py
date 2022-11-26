import discord
from discord.commands import slash_command, Option
from cogs.miscellaneous.search import SearchView

@slash_command(
    name="search",
    description="Search for events."
)
async def search(
    self, 
    ctx: discord.ApplicationContext, 
    event: Option(str, name="name", description="Enter RR event", required=True)
):
    await ctx.interaction.response.defer()

    view = SearchView(self.bot, event, "Event", lock=True)
    em = await view.initialize()
    await ctx.respond(view=view, embed=em)
