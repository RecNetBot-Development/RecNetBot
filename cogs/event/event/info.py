import discord
from discord.commands import slash_command, Option
from utils.converters import FetchEvent
from embeds import fetch_event_embed

@slash_command(
    name="info",
    description="View an event's details."
)
async def info(
    self, 
    ctx: discord.ApplicationContext, 
    event: Option(FetchEvent, name="event", description="Enter a RecNet link or id", required=True)
):
    await ctx.interaction.response.defer()

    em = await fetch_event_embed(event)
    await ctx.respond(embed=em)
