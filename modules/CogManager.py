import os
import json
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
            try:
                cog = Cog(self, dir)
                if cog.get_commands(): self.bot.add_cog(cog)  # Only add the cog if it has commands.
            except Exception as e:
                print(e)
                print(f"{dir} failed to load")
            
