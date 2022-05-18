from utility import load_cfg
from discord.commands import slash_command, Option # Importing the decorator that makes slash commands.
from base_commands.base_api import base_api

cfg = load_cfg()

@slash_command(
    debug_guilds=cfg['test_guild_ids'],
    name="data",
    description="Fetch raw event data."
)
async def data(
    self, 
    ctx, 
    name: Option(str, "Enter event name or id", required=True),
    is_id: Option(bool, "If it's an id, specify it here. If unspecified, it will be assumed", required=False)
):
    await base_api(rec_net=self.bot.rec_net.rec_net, ctx=ctx, type="Event", name=name, is_id=is_id)