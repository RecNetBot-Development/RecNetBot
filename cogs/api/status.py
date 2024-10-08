import discord
import time
import recnetpy
import asyncio
from resources import get_emoji
from embeds import get_default_embed
from discord.commands import slash_command
from utils import unix_timestamp

ignored_hosts = [
    "https://cdn.rec.net"
]

cache = {
    "timestamp": 0,
    "statuses": []
}

async def get_status(host_name: str, host_url: str, recnetpy: recnetpy.Client):
    start_time = time.perf_counter()
    try:  # Stupid crashes
        status = await recnetpy.rec_net.custom(host_url + "/health").make_request("get")
    except:
        status = None
    end_time = time.perf_counter()
    return {"status": status, "name": host_name, "elapsed": round(end_time - start_time, 2)}

@slash_command(
    name="apistatus",
    description="View diagnostics of Rec Room servers."
)
async def apistatus(
    self, 
    ctx: discord.ApplicationContext
):
    await ctx.interaction.response.defer()
    
    # Initialize embed
    em = get_default_embed()
    em.title = "Rec Room API Status"
    em.description = ""

    timestamp = int(time.time())
    if not cache["statuses"] or timestamp > cache["timestamp"]:
        # Fetch namespace for hosts
        ns = await self.bot.RecNet.rec_net.namespace.make_request("get")
        if not ns:  # Can't fetch the nameserver
            em.description = "Couldn't fetch the nameserver, looks like the whole server is down!"
            return await ctx.respond(embed=em)
        
        # Create coroutines for checking host health and execute
        coroutines = []
        for name, host in ns.data.items():
            if host in ignored_hosts: continue
            coroutines.append(get_status(name, host, self.bot.RecNet)) 
        statuses = await asyncio.gather(*coroutines)

        # Cache results for the next 10 minutes
        cache["timestamp"] = timestamp + 60 * 10  # 10 mins into the future
        cache["statuses"] = statuses
    else:
        # Use cached results
        statuses = cache["statuses"]
        em.description = f"Cached, refreshing {unix_timestamp(cache['timestamp'], 'R')}\n"

    # Form an embed for results
    status_results = []
    status_text = "{emoji} `{host}` ({perf} secs)"
    total_elapsed, failed = 0, 0
    for i in statuses:
        status, name, elapsed = i["status"], i["name"], i["elapsed"]
        if status and status.data == "Healthy":
            emoji = get_emoji("correct")
            status_results.append(status_text.format(emoji = emoji, host = name, perf = elapsed))
        else:
            failed += 1
            emoji = get_emoji("incorrect")
            status_results.insert(0, status_text.format(emoji = emoji, host = name, perf = elapsed))
        total_elapsed += elapsed
            
    host_count = len(statuses)
    em.description += f"{host_count - failed}/{host_count} up and running!\n\n" + "\n".join(status_results)
    em.set_footer(text=f"Total Elapsed Time: {round(total_elapsed, 2)}s")
    
    await ctx.respond(embed=em)

    
    

        

        
