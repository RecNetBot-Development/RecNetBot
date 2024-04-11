import discord
from discord.commands import slash_command

@slash_command(
    name="ping",
    description="Returns RecNetBot's latency"
)
async def ping(
    self,   
    ctx: discord.ApplicationContext
):
    await ctx.interaction.response.defer(invisible=True)
    
    ping = f"Ping: {round(self.bot.latency * 1000)} ms\n"
    for i in self.bot.latencies:
        ping += f"Shard {i[0]+1}: {round(i[1]*1000)} ms\n"

    await ctx.respond(ping)