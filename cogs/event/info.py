from rec_net.exceptions import EventNotFound
from utility import load_cfg, respond
from discord.commands import slash_command, Option # Importing the decorator that makes slash commands.
from embeds import event_embed

cfg = load_cfg()

@slash_command(
    debug_guilds=cfg['test_guild_ids'],
    name="info",
    description="Lookup an event and see details about it!"
)
async def info(
    self,
    ctx,
    name: Option(str, "Enter the event's name", required=True),
    is_id: Option(bool, "If it's an id, specify it here. If unspecified, it will be assumed", required=False)
):
    await ctx.interaction.response.defer()

    event = await self.bot.rec_net.event(name=name, includes=["creator", "room"])
    if not event: raise EventNotFound(name)
    
    await respond(ctx, embed=event_embed(event[0]))
    #room = await self.bot.rec_net.room(name=name, info=["tags", "subrooms", "roles", "scores"], includes=["roles", "creator"])