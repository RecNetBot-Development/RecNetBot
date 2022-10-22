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
    event_id: Option(str, "Enter the event's id", required=True)
):
    await ctx.interaction.response.defer()

    event = await self.bot.rec_net.event(id=event_id, includes=["creator", "room"])
    if not event: raise EventNotFound(event_id)
    
    await respond(ctx, embed=event_embed(event))
    #room = await self.bot.rec_net.room(name=name, info=["tags", "subrooms", "roles", "scores"], includes=["roles", "creator"])