from utility import load_cfg
from discord.commands import slash_command, Option  # Importing the decorator that makes slash commands.
from rec_net.exceptions import Error
from embeds import json_embed

cfg = load_cfg()

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="eventdata",
    description="Get raw event data from the API."
)
async def eventdata(
    self, 
    ctx, 
    event_input_type: Option(str, choices=["Event Name", "Id"], required=True),
    event: Option(str, "Enter the event", required=True)
):
    await ctx.interaction.response.defer()
    host = "https://api.rec.net/api"
    if event_input_type == "Id":
        if not event.isdigit(): raise InvalidEventId("Event id must be a digit!")  
        parsed_event_id = int(event)
        event_resp = await self.bot.rec_net.rec_net.api.playerevents.v1(parsed_event_id).get().fetch()
        endpoint = f"/playerevents/v1/{parsed_event_id}"
    else:
        event_resp = await self.bot.rec_net.rec_net.api.playerevents.v1.search().get({"query": event, "take": 1}).fetch()
        endpoint = f"/playerevents/v1/search?query={event}&take=1"

    event_data = event_resp.data
    if type(event_resp.data) is list:
        event_data = event_data[0]

    await ctx.respond(
        content = host + endpoint,
        embed=json_embed(ctx, event_data)
    )

class InvalidEventId(Error):
    ...


class EventNotFound(Error):
    ...