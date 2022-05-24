from discord.errors import Forbidden

failure = f"""
Hey, looks like I was unable to respond to your command! Please make sure my permissions are unchanged.
"""

message_failure = """
Hey, seems like I can't send any message in {channel} on {guild}
May you inform the server team about this issue? :slight_smile:
"""

async def send(ctx, **kwargs):
    await push(ctx.send, context=ctx, **kwargs)
            
async def respond(ctx, **kwargs):
    await push(ctx.respond, context=ctx, **kwargs)
            
async def edit_message(interaction, **kwargs):
    await push(interaction.response.edit_message, interaction=interaction, **kwargs)
            
async def push(function, **kwargs):
    context = kwargs.pop("interaction", None)
    context = kwargs.pop("context", None)
    
    try:
        await function(**kwargs)
    except Forbidden:
        try:
            await function(failure)
        except Forbidden:
            channel, guild = "UNKNOWN", "UNKNOWN"
            if context:
                channel = context.channel.name
                guild = context.guild.name
            
            await function(message_failure.format(channel=channel, guild=guild))
            

