import discord
from datetime import datetime
from discord.commands import slash_command, Option
from utils import unix_timestamp, load_config
from database import LoggingManager

config = load_config(is_production=True)

@slash_command(
    name="logs"
)
async def logs(
    self, 
    ctx: discord.ApplicationContext,
    timestamp: Option(int, name="timestamp_after", required=False, default=None)
):
    await ctx.interaction.response.defer(invisible=True)

    # dev check
    if not ctx.author.id in config.get("developers", []):
        return await ctx.respond("nuh uh!")

    lcm: LoggingManager = self.bot.lcm

    # Default to first recorded log
    if not timestamp:
        timestamp = await lcm.get_first_entry_timestamp()

    logs = await lcm.get_ran_commands_after_timestamp(timestamp)

    total_ran, total_users, command_ran = 0, 0, {}
    for user, data in logs.items():
        total_users += 1
        total_ran += data["total_usage"]

        # Calculate how many times each command has been ran
        for cmd, usage in data["specific"].items():
            if cmd in command_ran:
                command_ran[cmd] += len(usage)
            else:
                command_ran[cmd] = len(usage)

    # Sort by usage
    usage_sort = {k: v for k, v in sorted(command_ran.items(), key=lambda item: item[1], reverse=True)}
    leaderboard = ""
    limit, i = 20, 0
    for cmd, usage in usage_sort.items():
        if i >= limit: break
        leaderboard += f"- {cmd}: {usage:,}\n"
        i += 1

    # How many commands has each user ran on average
    if logs.keys():
        on_average = total_ran / len(logs.keys())
    else:
        on_average = 0
    
    """
    # Send database & logs
    files = []

    
    try:
        files.append(discord.File(r"rnb.db"))
    except FileNotFoundError:
        ...
    

    try:
        files.append(discord.File(r"error.log"))
    except FileNotFoundError:
        ...
    """

    delta = datetime.now() - datetime.fromtimestamp(timestamp)
    await ctx.respond(
        f"Statistics since {unix_timestamp(timestamp, 'R')}\n\n" \
        f"Commands ran per user on average: {round(on_average, 2)}\n" \
        f"Commands ran daily on average: {round((total_ran + 1) / (delta.days + 1))}\n" \
        f"Total commands ran: {total_ran}\n" \
        f"Total unique users: {total_users}\n" \
        f"Servers: {len(self.bot.guilds):,}\n" \
        f"Linked users: {await self.bot.cm.get_connection_count():,}\n\n" \
        f"Top commands by usage:\n{leaderboard}"
    )


    
    

        

        
