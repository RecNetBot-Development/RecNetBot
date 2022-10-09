import discord
from discord.ext import commands
from exceptions import EventNotFound

class FetchEvent(commands.Converter):
    """
    Converts a event param to a RR event
    """
    async def convert(self, ctx: discord.ApplicationContext, event_id: int):
        event = await ctx.bot.RecNet.events.fetch(event_id)
        if not event: raise EventNotFound
        return event
    
