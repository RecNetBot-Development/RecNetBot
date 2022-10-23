import discord
from discord.ext import commands
from exceptions import EventNotFound

class FetchEvent(commands.Converter):
    """
    Converts a event param to a RR event
    """
    async def convert(self, ctx: discord.ApplicationContext, _event: str | int):
        event_id = 0
        if isinstance(_event, str):
            if _event.isdigit(): 
                event_id = _event
            else:
                # This is fucking crazy and I can't believe I wrote this shit
                url = _event.split("/")
                event_id = list(filter(lambda piece: piece.isdigit(), url))
                if event_id:
                    event_id = event_id[0]
                else:
                    raise EventNotFound
                
        event = await ctx.bot.RecNet.events.fetch(event_id)
        if not event: raise EventNotFound
        return event
