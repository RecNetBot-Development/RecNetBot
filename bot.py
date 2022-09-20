import discord
import platform
import os
import logging
from datetime import datetime
from discord.ext import commands
from utility import load_cfg
from rec_net import Client
from modules import CogManager
from database import DatabaseManager
from googleapiclient import discovery

class RecNetBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setup Persistent Views
        self.persistent_views_added = False

        # Setup logger
        self.logger = logging.getLogger('discord')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(handler)

        # Add Modules
        self.config = load_cfg()
        self.rec_net = Client()
        self.cog_manager = CogManager(self)
        self.database = DatabaseManager()
        self.discovery = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=self.config.get("perspective_api_key"),
            discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
            static_discovery=False,
        )

        # Initialize
        self.cog_manager.buildCogs()
        
        self.http.bulk_upsert_command_permissions = self.dummy

        #TODO: add config validation & address module dependencies

    async def dummy(self, *args, **kwargs):
        pass 

    async def on_ready(self):
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name=self.config.get("status_message", "/help"))
        )
        
        print(f"""
RNB ONLINE
Logged in as {self.user.name}
PyCord version: {discord.__version__}
Python version: {platform.python_version()}
Running on: {platform.system()} {platform.release()} ({os.name})

        """)

        # Add persistent views
        #if not self.persistent_views_added:
        #    self.add_view(ImageUI(None, None))
        #    self.persistent_views_added = True

    #async def on_interaction(self, interaction):
    #    date = datetime.utcnow()
    #    print(f"{date.hour}:{date.minute} UTC | {interaction.user} ran /{interaction.data['name']}")

    def run(self):
        super().run(self.config['discord_token'])

