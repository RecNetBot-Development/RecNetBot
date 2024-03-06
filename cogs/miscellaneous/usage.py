import discord
from datetime import datetime
from discord.commands import slash_command
from utils import unix_timestamp
from embeds import get_default_embed
from resources import get_icon, get_emoji

@slash_command(
    name="usage",
    description="Find out how much you have used RecNetBot!"
)
async def usage(
    self, 
    ctx: discord.ApplicationContext
):
    first_entry_timestamp = self.bot.lcm.get_first_entry_timestamp()
    logs = self.bot.lcm.get_ran_commands_by_user_after_timestamp(first_entry_timestamp, ctx.author.id)

    em = get_default_embed()

    # Never used RNB before
    if not logs:
        em.title = "Uh oh!"
        em.description = "You have never used RecNetBot before! Run some commands and try again."
        em.set_thumbnail(url=get_icon("rectnet"))
        await ctx.respond(embed=em)
        return

    # Process ran commands
    command_ran = {}
    for cmd, usage in logs["specific"].items():
        command_ran[cmd] = len(usage)

    # Sort by usage
    usage_sort = {k: v for k, v in sorted(command_ran.items(), key=lambda item: item[1], reverse=True)}

    # Top 5 most used commands
    top_5_used_commands = list(usage_sort.items())[:5]

    # Top 5 least used commands
    top_5_least_commands = list(usage_sort.items())[-5:]

    # Total ran commands
    total_ran = logs["total_usage"]

    # First time used
    first_timestamp = logs["first_date"]

    # Create embed
    em.title = "Your RecNetBot Statistics"
    em.description = "\n".join((
        f"You first started using RecNetBot on {unix_timestamp(first_timestamp, 'D')}.",
        f"You have ran commands `{total_ran:,}` times."
    ))
    em.set_thumbnail(url=get_icon("rotating_logo"))

    first_entry_datetime = datetime.fromtimestamp(first_entry_timestamp)
    em.set_footer(text=f"Data since {first_entry_datetime.strftime('%B, %d %Y')}")

    fav_commands = ""
    for cmd, usage in top_5_used_commands:
        fav_commands += f"- {cmd}: {usage:,}\n"
    em.add_field(name=f"{get_emoji('cheer_host')} Your Favorite Commands", value=fav_commands)

    least_fav_commands = ""
    for cmd, usage in top_5_least_commands:
        least_fav_commands += f"- {cmd}: {usage:,}\n"
    em.add_field(name=f"{get_emoji('rectnet')} Your Least Used Commands", value=least_fav_commands)

    await ctx.respond(embed=em)
    

    
    

        

        
