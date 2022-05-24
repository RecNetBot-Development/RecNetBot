from utility import load_cfg
from discord.commands import slash_command, Option  # Importing the decorator that makes slash commands.
from base_commands.base_api import base_api

cfg = load_cfg()
    
@slash_command(
    debug_guilds=cfg['test_guild_ids'],
    name="data",
    description="Get raw data from the API."
)
async def data(
    self, 
    ctx, 
    type: Option(str, "Enter what type of data you want", choices=["account", "room", "event", "image"], required=True),
    name: Option(str, "Enter the unique name or id", required=True),
    is_id: Option(bool, "Is the name argument an id or not? If unspecified, it will be assumed. Images are always id's.", required=False)
):
    await base_api(rec_net=self.bot.rec_net.rec_net, ctx=ctx, type=type, name=name, is_id=is_id)