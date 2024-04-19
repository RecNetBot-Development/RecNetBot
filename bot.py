import discord
import platform
import os
import logging
import time
import aiosqlite
import sqlite3
# import server
from logging.handlers import RotatingFileHandler
from cat_api import CatAPI
from utils import load_config
from discord.ext import commands, tasks
from recnetpy import Client
from typing import List
from modules import CogManager
from database import *
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from google.auth.exceptions import DefaultCredentialsError
from utils.paginator import RNBPage, RNBPaginator
<<<<<<< HEAD
=======
#from tasks import backup_database
>>>>>>> b07f4ea8987e826d44cf2fd2d7adae682ffd320e
#from utils.persistent_views import *

class RecNetBot(commands.AutoShardedBot):
    def __init__(self, production: bool):
        self.production = production
        if self.production:
            super().__init__(help_command=None)
        else:
            # Developer only for now
            intents = discord.Intents.default()
            intents.members = True
            super().__init__(help_command=None, intents=intents)

        # Load config
        self.config = load_config(is_production=production)
        self.debug_guilds = self.config.get("debug_guilds", [])
    
        # Setup logger
        self.logger = logging.getLogger('discord')
        handler = RotatingFileHandler(filename='discord.log', encoding='utf-8', mode='w', maxBytes=1000000)  # 1 mb
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(handler)

        # Add Modules
        self.RecNet: Client = None
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
        self.db: aiosqlite.Connection = None
        self.backup: aiosqlite.Connection = None
        self.cm = ConnectionManager()
        self.rcm = RoomCacheManager()
        #self.icm = InventionCacheManager(self.db)
        #self.bcm = BookmarkManager(self.db)
        self.lcm = LoggingManager()
        self.acm = AnnouncementManager()
        #self.gm = GuildManager()
        #self.fcm = FeedManager()

        # Banned users' Discord IDs
        # Updates everytime someone gets banned
        self.banned_users = []

        # Persistent views
        self.persistent_views_added = False

        # Initialize
        self.cog_manager.buildCogs()


    async def on_ready(self):
        """
        Do asynchronous setup here
        """

        # Initialize databases
        self.db = await aiosqlite.connect(self.config["sqlite_database"], detect_types=sqlite3.PARSE_DECLTYPES)
        await self.cm.init(self.db)
        await self.rcm.init(self.db)
        await self.lcm.init(self.db)
        await self.acm.init(self.db)
        #await self.gm.init(self.db)
        #await self.fcm.init(self.db)

        # Backup
        self.backup = await aiosqlite.connect("backup.db", detect_types=sqlite3.PARSE_DECLTYPES)
<<<<<<< HEAD
=======
        # backup_database.start(self)
>>>>>>> b07f4ea8987e826d44cf2fd2d7adae682ffd320e

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
        
        # Register the persistent view for listening
        #if not self.persistent_views_added:
        #    self.add_view(VerificationView(self))
        #    self.persistent_views_added = True

        print(
            f"RNB ONLINE",
            f"Logged in as {self.user.name}",
            f"PyCord version: {discord.__version__}",
            f"Python version: {platform.python_version()}",
            f"Running on: {platform.system()} {platform.release()} ({os.name})\n",
            sep="\n"
        )
    

    async def __on_member_join(self, member: discord.Member):
        """Verify user on join if server is enrolled in member verification"""
        guild = member.guild

        # Check if guild is enrolled
        if not await self.gm.is_guild_setup(guild.id): return

        # Check if the user is verified
        cm: ConnectionManager = self.cm
        rr_id = await cm.get_discord_connection(member.id)
        if not rr_id: return
            
        # Get binding role
        gm: GuildManager = self.gm
        role_id = await gm.get_binding_role_id(guild.id)
        role: discord.Role = guild.get_role(role_id)

        # Get linked account
        account = await self.RecNet.accounts.fetch(rr_id)

        # Add verification role
        await member.add_roles(role, reason=f"Verified user: @{account.username} - ID: {account.id}")

        # Get naming convention
        name_rule = await gm.get_naming_convention(guild.id)

        # List any errors
        errors = []

        # Change member's name if naming convention set
        try:
            match name_rule:
                case NameRule.USERNAME:
                    await member.edit(nick=f"@{account.username}")
                case NameRule.DISPLAYNAME:
                    await member.edit(nick=f"{account.display_name}")
                case _:
                    ...
        except discord.errors.Forbidden:
            ...

        try:
            await member.add_roles(role, reason=f"Verified user: @{account.username} - ID: {account.id}")
        except discord.errors.Forbidden:
           ...


    #async def on_error(self, event, *args, **kwargs):
    #    logging.basicConfig(level=logging.WARNING, filename="error.log", filemode="a+",
    #                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    #    logging.error(event + " -> " + str(args) + " " + str(kwargs))


    def run(self):
        super().run(self.config['discord_token'])

    async def on_application_command_completion(self, ctx: discord.ApplicationContext):
        """Log command usage and push announcements"""
        if hasattr(ctx.command, "mention"):
            await self.lcm.log_command_usage(ctx.author.id, ctx.command.mention)
        else:
            # User commands don't have the mention attribute
            await self.lcm.log_command_usage(ctx.author.id, f"other:{ctx.command.name}")

        # Check announcements
        announcements: List[Announcement] = await self.acm.get_unread_announcements(ctx.author.id)
        if not announcements: return

        non_expired_announcements = []
        for i in announcements:
            if i.expiration_timestamp and i.expiration_timestamp < time.time():
                non_expired_announcements.append(i)
        
        pages = list(map(lambda ele: RNBPage(ele, data=ele), announcements))
        paginator = RNBPaginator(pages=pages, trigger_on_display=True, show_indicator=False, author_check=True)
        #await paginator.respond(ctx.interaction)

        await paginator.respond(ctx.interaction, ephemeral=True)

        #await ctx.followup.send(content="unread messages.....", view=paginator, ephemeral=True)
