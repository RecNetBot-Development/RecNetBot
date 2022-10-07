import discord
import platform
import os
import logging
import json
import sqlite3
from discord.ext import commands
from recnetpy import Client
from modules import CogManager
from database import ConnectionManager

class RecNetBot(commands.Bot):
    def __init__(self, production: bool):
        super().__init__()

        # Load config
        path = "./config/{}.json"
        with open(path.format("production" if production else "development"), 'r') as cfg_json:
            self.config = json.load(cfg_json)
            
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

        # Verify post for RR account links
        self.verify_post = None
        
        # Channel for bug reports
        self.bug_channel = None

        # Initialize database
        self.db = sqlite3.connect(self.config.get("sqlite_database", "rnb.db"))
        self.cm = ConnectionManager(self.db)

        # Initialize
        self.cog_manager.buildCogs()


    async def on_ready(self):
        """
        Do asynchronous setup here
        """
        self.RecNet = Client()
        self.verify_post = await self.RecNet.images.fetch(self.config["verify_post"])
        self.bug_channel = await self.fetch_channel(self.config["bug_report_channel"])
        
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name=self.config.get("status_message", "/help"))
        )
        
        print(
            f"RNB ONLINE",
            f"Logged in as {self.user.name}",
            f"PyCord version: {discord.__version__}",
            f"Python version: {platform.python_version()}",
            f"Running on: {platform.system()} {platform.release()} ({os.name})",
            sep="\n"
        )


    #async def on_error(self, event, *args, **kwargs):
    #    logging.basicConfig(level=logging.WARNING, filename="error.log", filemode="a+",
    #                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    #    logging.error(event + " -> " + str(args) + " " + str(kwargs))


    def run(self):
        super().run(self.config['discord_token'])

