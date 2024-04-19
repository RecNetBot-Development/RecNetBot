import discord
import recnetpy
from typing import Dict, TYPE_CHECKING, List
from discord.commands import slash_command
import recnetpy.dataclasses
from embeds import get_default_embed
from utils import room_url, img_url
from resources import get_icon
from database import FeedManager

if TYPE_CHECKING:
    from bot import RecNetBot

class FeedButton(discord.ui.Button["FeedView"]):
    def __init__(self, bot: 'RecNetBot', feed: Dict, fcm: FeedManager):
        self.feed = feed
        self.fcm = fcm
        self.bot = bot
        super().__init__(style=discord.ButtonStyle.red, label=f"Delete {feed['room'].name}", custom_id=str(feed['id']))

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: FeedView = self.view
        
        feed_id = self.feed['id']
        
        # Delete feed from database
        await self.fcm.delete_feed_with_id(feed_id)
        try:  # Attempt to delete the webhook if not already deleted
            webhook = await self.bot.fetch_webhook(self.feed['webhook_id'])
            await webhook.delete()
        except:
            ...

        # Remove from feeds
        view.feeds.remove(self.feed)
        self.disabled = True

        await interaction.response.edit_message(embed=view.create_embed(), view=view)
        await interaction.followup.send("Successfully deleted feed!", ephemeral=True)


class FeedView(discord.ui.View):
    def __init__(self, feeds: List[Dict], bot: 'RecNetBot', rooms: Dict[int, recnetpy.dataclasses.Room]):
        super().__init__()

        self.feeds = feeds
        self.bot = bot
        self.fcm = bot.fcm
        self.rooms = rooms

        for i in feeds:
            i["channel"] = self.bot.get_channel(self.feed['channel_id'])
            i['room'] = self.rooms[i['room_id']]
            self.add_item(FeedButton(self.bot, i, self.fcm))
            
        # Create embed once the channels have been fetched
        self.embed = self.create_embed()
            
    def create_embed(self):
        em = get_default_embed(
            title = "Delete a Photo Feed",
            thumbnail=discord.EmbedMedia(url=get_icon("photo"))
        )
        
        if self.feeds:
            # Fetch rooms
            for i in self.feeds:
                em.add_field(name=i['id'], value=f"^{i['room'].name} in {i['channel'].mention}")
        else:
            em.add_field(name="No feeds to delete!", value="You can create feeds with /feed create.")
            
        return em
        
@slash_command(
    name="delete",
    description="Delete a photo feed webhook."
)
async def delete(
    self, 
    ctx: discord.ApplicationContext
):
    await ctx.interaction.response.defer()
    
    # Get feed database manager
    fcm: FeedManager = self.bot.fcm

    # Get users' feeds
    feeds = await fcm.get_feeds_by_user(ctx.author.id)

    # Fetch rooms
    room_ids = []
    for i in feeds:
        room_ids.append(i['rr_id'])
    rooms: List[recnetpy.dataclasses.Room] = await self.bot.RecNet.rooms.fetch_many(room_ids)
    rooms_ = {}
    for room in rooms:
        rooms_[room.id] = room

    # Create the view containing our feeds
    view = FeedView(feeds, self.bot, rooms_)

    await ctx.respond(embed=view.embed, view=view)

        
