import discord
import recnetpy
from typing import Dict, TYPE_CHECKING, List
from discord.commands import slash_command
import recnetpy.dataclasses
from embeds import get_default_embed
from utils import room_url, img_url, BaseView
from resources import get_icon, get_emoji
from database import FeedManager

if TYPE_CHECKING:
    from bot import RecNetBot

class FeedButton(discord.ui.Button["FeedView"]):
    def __init__(self, bot: 'RecNetBot', feed: Dict, fcm: FeedManager, label: str):
        self.feed = feed
        self.fcm = fcm
        self.bot = bot
        super().__init__(style=discord.ButtonStyle.red, label=label, custom_id=str(feed['id']), emoji=get_emoji('x'))

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
        await interaction.followup.send(f"Successfully deleted ^{self.feed['room_name']} feed from {self.feed['server_name']}!", ephemeral=True)


class FeedView(BaseView):
    def __init__(self, feeds: List[Dict], bot: 'RecNetBot', rooms: Dict[int, recnetpy.dataclasses.Room], create_cmd):
        super().__init__()

        # Feeds
        self.feeds = feeds
        
        # Misc
        self.bot = bot
        self.fcm = bot.fcm
        self.rooms = rooms
        self.create_cmd = create_cmd

        # Index every feed for deletion
        self.feed_index = {}

        for i, feed in enumerate(self.feeds, start=1):
            self.feed_index[feed['id']] = i
            
            # Fetch channel
            channel = self.bot.get_channel(feed['channel_id'])
            feed["channel_name"] = channel.mention if channel else f"{get_emoji('warning')} Unknown Channel"
            
            # Fetch room
            room = self.rooms.get(feed['rr_id'], None)
            feed['room_name'] = room.name if room else f"{get_emoji('warning')} Unknown Room"
            
            self.add_item(FeedButton(self.bot, feed, self.fcm, label=f"{i}."))
            
        # Create embed once the channels have been fetched
        self.embed = self.create_embed()
            
    def create_embed(self):
        em = get_default_embed(
            title = "Delete a Photo Feed",
            thumbnail=discord.EmbedMedia(url=get_icon("photo_delete")),
            footer=discord.EmbedFooter(text="The feed cannot be retrieved after deletion. You can always recreate feeds.")
        )
        
        feed_fields = {}
        if self.feeds:
            for i in self.feeds:
                text = f"{self.feed_index[i['id']]}. ^{i['room_name']} in {i['channel_name']}"
                
                # Categorize based on if the server is in current server
                server_name = i.get("server_name")
                if server_name in feed_fields:
                    feed_fields[server_name].append(text)
                else:
                    feed_fields[server_name] = [text]
                    
            for i, j in feed_fields.items():
                em.add_field(name=i, value="\n".join(j), inline=False)
        else:
            em.add_field(name="No feeds to delete!", value=f"You can create feeds in your servers with {self.create_cmd.mention}.")

        return em
        
@slash_command(
    name="delete",
    description="Delete a photo feed webhook."
)
async def delete(
    self, 
    ctx: discord.ApplicationContext
):
    await ctx.interaction.response.defer(ephemeral=True)
    
    # Get feed database manager
    fcm: FeedManager = self.bot.fcm

    # Get users' feeds
    feeds = await fcm.get_feeds_by_user(ctx.author.id) or []

    # Get feeds in server if admin
    if ctx.author.guild_permissions.administrator:
        server_feeds = await fcm.get_feeds_in_server(ctx.guild_id) or []
        for i in server_feeds:
            if i not in feeds: feeds.append(i)
                
    if feeds:
        # Fetch rooms
        room_ids = []
        for i in feeds:
            server = self.bot.get_guild(i['server_id'])
            i["server_name"] = server.name if server else f"{get_emoji('warning')} Unknown Server"
            room_ids.append(i['rr_id'])
        
        rooms: List[recnetpy.dataclasses.Room] = await self.bot.RecNet.rooms.fetch_many(room_ids)
        rooms_ = {}
        for room in rooms:
            rooms_[room.id] = room
    else:
        rooms_ = {}

    # /feed create
    group = discord.utils.get(self.__cog_commands__, name='feed')
    cmd = discord.utils.get(group.walk_commands(), name='create')

    # Create the view containing our feeds
    view = FeedView(feeds, self.bot, rooms_, cmd)

    await ctx.respond(embed=view.embed, view=view, ephemeral=True)

        
