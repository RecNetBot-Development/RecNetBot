import discord
import platform
import os
import logging
import time
import sqlite3
from datetime import datetime
from cat_api import CatAPI
from utils import load_config
from discord.ext import commands, tasks
from recnetpy import Client
from typing import List
from modules import CogManager
from database import ConnectionManager, RoomCacheManager, InventionCacheManager, BookmarkManager, LoggingManager, FeedManager, FeedTypes, FeedData, AnnouncementManager, Announcement
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from google.auth.exceptions import DefaultCredentialsError
from embeds import get_default_embed, announcement_embed

class RecNetBot(commands.AutoShardedBot):
    def __init__(self, production: bool):
        super().__init__(help_command=None)

        # Load config
        self.config = load_config(is_production=production)
        self.debug_guilds = self.config.get("debug_guilds", [])
    
        # Setup logger
        self.logger = logging.getLogger('discord')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(handler)

        # Add Modules
        self.RecNet = None
        self.cog_manager = CogManager(self)
        self.CatAPI = CatAPI(api_key=self.config.get("the_cat_api_key"))

        # Optionally enable Perspective API for /toxicity
        try:
            self.perspective = discovery.build(
                "commentanalyzer",
                "v1alpha1",
                developerKey=self.config.get("perspective_api_key"),
                discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
                static_discovery=False,
            )
        except (HttpError, DefaultCredentialsError):
            self.perspective = None
            print("Perspective API disabled. Some functionality will be lost!")

        # Verify post for RR account links
        self.verify_post = None
        
        # Channel for bug reports
        self.bug_channel = None

        # Initialize database
        self.db = sqlite3.connect(self.config.get("sqlite_database", "rnb.db"), detect_types=sqlite3.PARSE_DECLTYPES)
        self.cm = ConnectionManager(self.db)
        self.rcm = RoomCacheManager(self.db)
        self.icm = InventionCacheManager(self.db)
        self.bcm = BookmarkManager(self.db)
        self.lcm = LoggingManager(self.db)
        #self.fcm = FeedManager(self.db)
        self.acm = AnnouncementManager(self.db)

        # Initialize
        self.cog_manager.buildCogs()


    async def on_ready(self):
        """
        Do asynchronous setup here
        """

        # Get Rec Room API key
        api_key = self.config["rr_api_key"]
        self.RecNet = Client(api_key=api_key)

        # Initialize cat API
        if self.CatAPI.api_key:
            await self.CatAPI.initialize()

        self.verify_post = await self.RecNet.images.fetch(self.config["verify_post"])
        self.log_channel = await self.fetch_channel(self.config["log_channel"])
        
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name=self.config.get("status_message", "Rec Room"))
        )
        
        print(
            f"RNB ONLINE",
            f"Logged in as {self.user.name}",
            f"PyCord version: {discord.__version__}",
            f"Python version: {platform.python_version()}",
            f"Running on: {platform.system()} {platform.release()} ({os.name})\n",
            sep="\n"
        )
    
    #async def on_error(self, event, *args, **kwargs):
    #    logging.basicConfig(level=logging.WARNING, filename="error.log", filemode="a+",
    #                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    #    logging.error(event + " -> " + str(args) + " " + str(kwargs))


    def run(self):
        super().run(self.config['discord_token'])


    async def on_application_command_completion(self, ctx: discord.ApplicationContext):
        if hasattr(ctx.command, "mention"):
            self.lcm.log_command_usage(ctx.author.id, ctx.command.mention)
        else:
            # User commands don't have the mention attribute
            self.lcm.log_command_usage(ctx.author.id, f"other:{ctx.command.name}")

        # Check announcements
        announcement: Announcement = self.acm.get_unread_announcement(ctx.author.id)
        if not announcement: return
        if announcement.expiration_timestamp and announcement.expiration_timestamp < time.time(): return
        
        em = announcement_embed(announcement)
        await ctx.followup.send(embed=em, ephemeral=True)

    
    #@tasks.loop(seconds=10)
    async def feed_update(self):
        # Get feeds
        feeds = self.fcm.get_all_feeds()

        # Sort feeds
        image_feeds = {} 
        room_feeds: List[FeedData] = []
        event_feeds: List[FeedData] = []
        for i in feeds:
            match i.type:
                case FeedTypes.IMAGE:
                    if i.rr_id in image_feeds:
                        image_feeds.append(i)
                    else:
                        image_feeds[i.rr_id] = [i]

                case FeedTypes.ROOM:
                    room_feeds.append(i)

                case FeedTypes.EVENT:
                    event_feeds.append(i)

                case _: ...

        # Update image feeds
        if image_feeds:
            # Sort image ids
            image_ids = list(image_feeds.keys())

            # Fetch images
            images = await self.RecNet.images.fetch_many(image_ids)

            # Send to feeds
            for i in images:
                feeds = image_feeds[i.id]
                print(f"Image {i.id} sent to {feeds}")


                        

