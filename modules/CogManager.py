import os
from modules.Cog import Cog

class CogManager:
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        self._cogs = []

    @property
    def cogDirs(self):
        dirName = './cogs'
        dirFiles = os.listdir(dirName)

        return filter(lambda file: os.path.isdir(f"{dirName}/{file}"), dirFiles)

    def buildCogs(self):
        cogDirs = self.cogDirs
        for dir in cogDirs:
            self.bot.add_cog(Cog(self, dir))
