import discord

def DefaultEmbed(**kwargs):
    em = discord.Embed(
        color=discord.Color.orange(),
        **kwargs
    )
    
    return em