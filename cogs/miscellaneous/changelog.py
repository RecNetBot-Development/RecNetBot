import discord
import random
import re
from embeds import get_default_embed
from discord.commands import slash_command
from utils import get_changelog

@slash_command(
    name="changelog",
    description="Check out RecNetBot's latest change log."
)
async def changelog(
    self, 
    ctx: discord.ApplicationContext
):
    await ctx.interaction.response.defer(invisible=True)

    resp = await get_changelog(self.bot)

    # Make sure no errors occured
    error = resp.get("error")

    match error:
        case 0:  # change log channel not found
            return await ctx.respond("Couldn't find the change log channel!")
        case 1:  # latest message not found
            return await ctx.respond("Couldn't find the latest change log!")
        case _:  # no errors
            ...

    # Form response
    change_log = resp.get("raw", "This is a placeholder. You are not supposed to see this.")

    # Add creation date
    change_log += f"\n\n*Updated* <t:{resp.get('created_timestamp', 0)}:R>"

    # Add edited date
    edited = resp.get('edited_timestamp', 0)
    if edited:
        change_log += f"\n*Edited* <t:{edited}:R>"

    # Send da change log
    await ctx.respond(change_log)

    
    

        

        
