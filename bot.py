import logging
from discord.ext import commands
from scripts import load_cfg
from rest import Client
from modules import CogManager
from database import DatabaseManager

class RecNetBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        #initialize
        self.cog_manager.buildCogs()
        #TODO: add config validation & address module dependencies

    def run(self):
        super().run(self.config['token'])

