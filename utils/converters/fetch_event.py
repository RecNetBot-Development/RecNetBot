import discord
from discord.ext import commands
from exceptions import EventNotFound, InvalidURL
from urllib.parse import urlparse
from recnetpy.rest.exceptions import BadRequest

class FetchEvent(commands.Converter):
    """
    Converts a event param to a RR event
    """
    async def convert(self, ctx: discord.ApplicationContext, _event: str | int):
        event = None
        event_id = 0
        if isinstance(_event, str):
            # Sanitize input
            _event = _event.strip()
            
            if _event.isdigit(): 
                event_id = _event
            else:
                url = urlparse(_event)
                
                if url.netloc != "rec.net":
                    raise InvalidURL
                
                if "event" in url.path:
                    event_id = url.path.split("event/")[1]
                else:
                    raise InvalidURL("/event/...")
                
        try:
            if event_id:
                event = await ctx.bot.RecNet.events.fetch(event_id)
        except BadRequest:  # odd edge case
            event = None
            
        if not event: raise EventNotFound
        return event
