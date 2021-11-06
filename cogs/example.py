import requests  # For testing purposes
from scripts import load_cfg, image_embed
from discord.ext import commands
from discord.commands import slash_command # Importing the decorator that makes slash commands.

cfg = load_cfg()

class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 
    @slash_command(guild_ids=[cfg['test_guild_id']]) # Create a slash command for the supplied guilds.
    async def image_test(self, ctx, post_id: int):
        async def get_post_data(post_id):  # Temporary for testing purposes
            url = f"https://api.rec.net/api/images/v4/{post_id}"
            r = requests.get(url)
            if r.ok:
                return r.json()
            return {}

        post_data = await get_post_data(post_id)

        # Test post
        em = await image_embed(post_data)  # Get embed
        await ctx.respond(embed=em)

    @slash_command() # Not passing in guild_ids creates a global slash command (might take an hour to register).
    async def hi(self, ctx):
        await ctx.respond(f"Hi, this is a global slash command from a cog!")

def setup(bot):
    bot.add_cog(Example(bot))