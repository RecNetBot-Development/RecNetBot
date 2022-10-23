import discord
import time
from resources import get_emoji
from embeds import get_default_embed
from discord.commands import slash_command

ignored_hosts = [
    "https://cdn.rec.net"
]

@slash_command(
    name="apistatus",
    description="View diagnostics of Rec Room servers."
)
async def apistatus(
    self, 
    ctx: discord.ApplicationContext
):
    await ctx.interaction.response.defer()
    
    em = get_default_embed()
    em.title = "Rec Room API Status"

    statuses = []
    failed = 0
    
    ns = await self.bot.RecNet.rec_net.namespace.make_request("get")
    if not ns:  # Can't fetch the nameserver
        em.description = "Couldn't fetch the nameserver, looks like the whole server is down!"
        return await ctx.respond(embed=em)
     
    for name, host in ns.data.items():
        if host in ignored_hosts: continue
        
        start_time = time.perf_counter()
        status = await self.bot.RecNet.rec_net.custom(host + "/health").make_request("get")
        end_time = time.perf_counter()
        
        status_text = "{emoji} `{host}` ({perf} secs)"
        if status and status.data == "Healthy":
            emoji = get_emoji("correct")
            statuses.append(status_text.format(emoji = emoji, host = name, perf = round(end_time - start_time, 2)))
        else:
            failed += 1
            emoji = get_emoji("incorrect")
            statuses.insert(0, status_text.format(emoji = emoji, host = name, perf = round(end_time - start_time, 2)))
            
    host_count = len(ns.data) - len(ignored_hosts)
    em.description = f"{host_count - failed}/{host_count} up and running!\n\n" + "\n".join(statuses)
    
    await ctx.respond(embed=em)

    
    

        

        
