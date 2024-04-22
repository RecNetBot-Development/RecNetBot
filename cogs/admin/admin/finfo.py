import discord
from bot import RecNetBot
from discord.commands import slash_command
from utils import load_config
from database import FeedTypes
from tasks.update_feeds import rr_api_calls_per_hour

config = load_config(is_production=True)

@slash_command(
    name="finfo"
)
async def finfo(
    self, 
    ctx: discord.ApplicationContext
):
    await ctx.interaction.response.defer()

    # dev check
    if not ctx.author.id in config.get("developers", []):
        return await ctx.respond("nuh uh!")

    bot: RecNetBot = self.bot
    feeds = await bot.fcm.get_feeds_based_on_type(FeedTypes.IMAGE)
    
    # Get total feeds
    feed_count = 0
    for i in feeds.values():
        feed_count += len(i)
        
    # Get rooms
    room_count = len(feeds.keys())

    await ctx.respond(f"Feeds: {feed_count}\nRoom count: {room_count}")