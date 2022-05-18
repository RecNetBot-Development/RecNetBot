from discord.errors import Forbidden
from utility.image.finalize_embed import finalize_embed

failure = f"""
Hey, looks like I was unable to respond to your command! Please make sure my permissions are unchanged.
"""

message_failure = """
Hey, seems like I can't send any message in {channel} on {guild}
May you inform the server team about this issue? :slight_smile:
"""

async def send(ctx, **kwargs):
    if "embed" in kwargs: kwargs["embed"] = finalize_embed(kwargs["embed"])
    if "embeds" in kwargs: kwargs["embeds"] = [finalize_embed(embed) for embed in kwargs["embeds"]]
    
    try:
        await ctx.send(**kwargs)
    except Forbidden:
        try:
            await ctx.send(failure)
        except Forbidden:
            await ctx.author.send(message_failure.format(channel=ctx.channel.name, guild=ctx.guild.name))
            
async def respond(ctx, **kwargs):
    if "embed" in kwargs: kwargs["embed"] = finalize_embed(kwargs["embed"])
    if "embeds" in kwargs: kwargs["embeds"] = [finalize_embed(embed) for embed in kwargs["embeds"]]
    
    try:
        await ctx.respond(**kwargs)
    except Forbidden:
        try:
            await ctx.respond(failure)
        except Forbidden:
            await ctx.author.send(message_failure.format(channel=ctx.channel.name, guild=ctx.guild.name))
            
async def edit_message(ctx, interaction, **kwargs):
    if "embed" in kwargs: kwargs["embed"] = finalize_embed(kwargs["embed"])
    if "embeds" in kwargs: kwargs["embeds"] = [finalize_embed(embed) for embed in kwargs["embeds"]]
    
    try:
        await interaction.response.edit_message(**kwargs)
    except Forbidden:
        try:
            await interaction.response.edit_message(failure)
        except Forbidden:
            await ctx.author.send(message_failure.format(channel=ctx.channel.name, guild=ctx.guild.name))
            

