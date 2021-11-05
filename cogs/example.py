from scripts import load_cfg, image_embed
from discord.ext import commands
from discord.commands import slash_command # Importing the decorator that makes slash commands.

cfg = load_cfg()

class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 
    @slash_command(guild_ids=[cfg['test_guild_id']]) # Create a slash command for the supplied guilds.
    async def image_test(self, ctx):
        # Test post
        post = {"Id":45084641,"Type":1,"Accessibility":1,"AccessibilityLocked":False,"ImageName":"fe721c0f7f1c4deaaa2d79057cc62af1.jpg","Description":None,"PlayerId":1827567,"TaggedPlayerIds":[1827567],"RoomId":170134,"PlayerEventId":189069,"CreatedAt":"2020-12-15T04:56:54.4519046Z","CheerCount":1,"CommentCount":2}
        em = await image_embed(post)  # Get embed
        await ctx.respond(embed=em)

    @slash_command() # Not passing in guild_ids creates a global slash command (might take an hour to register).
    async def hi(self, ctx):
        await ctx.respond(f"Hi, this is a global slash command from a cog!")

def setup(bot):
    bot.add_cog(Example(bot))