import discord
from embeds.base.embed import DefaultEmbed as Embed
from aiohttp import ClientConnectorError
from rec_net.exceptions import NameServerUnavailable
from utility import load_cfg, respond, Emoji
from discord.commands import slash_command # Importing the decorator that makes slash commands.

cfg = load_cfg()

@slash_command(
    debug_guilds=cfg['test_guild_ids'],
    name="status",
    description="Check the status of Rec Room's API's."
)
async def apistatus(
    self, 
    ctx
):
    await ctx.interaction.response.defer()

    embed = Embed(
        title="API Status Results"
    )

    namespace_resp = await self.bot.rec_net.rec_net.namespace.get().fetch()
    if not isinstance(namespace_resp.data, dict): raise NameServerUnavailable()
    namespace = namespace_resp.data
    healthy_count = 0
    health_list = []

    ignored_hosts = [
        "CDN"
    ]
    
    for host in namespace:
        if host in ignored_hosts: continue
        try:
            status_resp = await self.bot.rec_net.rec_net.custom(namespace[host] + "/").health.get().fetch()
            status = Emoji.correct if status_resp.success else Emoji.incorrect
            if status_resp.success: healthy_count += 1
        except ClientConnectorError:
            status = Emoji.incorrect
            
        health_list.append(f"{status} `{host}`")
    
    embed.add_field(
        name="Statuses",
        value="\n".join(health_list)
    )
    embed.description = f"`{healthy_count}/{len(namespace) - len(ignored_hosts)}` are up and running!"
    
    await respond(
        ctx,
        embed=embed,
    )