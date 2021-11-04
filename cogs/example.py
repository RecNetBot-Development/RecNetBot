from funcs import load_cfg
from discord.ext import commands
from discord.commands import slash_command # Importing the decorator that makes slash commands.

cfg = load_cfg()

class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 
    @slash_command(guild_ids=[cfg['test_guild_id']]) # Create a slash command for the supplied guilds.
    async def hello(self, ctx):
        await ctx.respond("Hi, this is a slash command from a cog!")


    @slash_command() # Not passing in guild_ids creates a global slash command (might take an hour to register).
    async def hi(self, ctx):
        await ctx.respond(f"Hi, this is a global slash command from a cog!")

def setup(bot):
    bot.add_cog(Example(bot))