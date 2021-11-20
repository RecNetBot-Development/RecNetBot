import importlib
import os
import sys
from rest import Client
from modules.Cog import Cog
from discord.commands import ApplicationCommand

class CogManager:
    def __init__(self, bot, rnb_db, rn_client=Client(), *args, **kwargs):
        self.bot = bot
        self.rn_client = rn_client
        self.rnb_db = rnb_db
        self._cogs = []

    @property
    def cogDirs(self):
        dirName = './cogs'
        dirFiles = os.listdir(dirName)

        return filter(lambda file: os.path.isdir(f"{dirName}/{file}"), dirFiles)

    def buildCogs(self):
        cogDirs = self.cogDirs
        for dir in cogDirs:
            self.bot.add_cog(Cog(self, dir, self.rn_client))
