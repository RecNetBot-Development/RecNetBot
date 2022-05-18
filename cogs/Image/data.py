from utility import load_cfg
from discord.commands import slash_command, Option # Importing the decorator that makes slash commands.
from base_commands.base_api import base_api

cfg = load_cfg()

@slash_command(
    debug_guilds=cfg['test_guild_ids'],
    name="data",
    description="Fetch raw image data."
)
async def data(
    self, 
    ctx, 
    id: Option(str, "Enter image id", required=True)
):
    await base_api(rec_net=self.bot.rec_net.rec_net, ctx=ctx, type="Image", name=id, is_id=True)