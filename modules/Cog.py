import os
from discord.ext import commands
from scripts.ModuleCollector import ModuleCollector
from discord.commands import ApplicationCommand
from rec_net.exceptions import AccountNotFound
from embeds import error_embed

class Cog(commands.Cog):
    def __init__(self, manager, name):
        self.bot = manager.bot
        self._modules = ModuleCollector()
        self.__cog_name__ = name
        self.__cog_commands__ = []
        self.buildCog()

    def buildCog(self):
        for file in os.listdir(f"./cogs/{self.__cog_name__}"):
            if file.endswith(".py"):
                extension = file[:-3]
                self._modules.add(f"cogs.{self.__cog_name__}.{extension}")
                lib = self._modules.get(f"cogs.{self.__cog_name__}.{extension}")
                for attr in dir(lib):
                    if isinstance(getattr(lib, attr), ApplicationCommand):
                        mod = getattr(lib, attr)
                        if not command.is_subcommand:
                            self.addCommand(mod)
                            print(f"Command {attr} in Cog {self.__cog_name__} has been loaded")

    def addCommand(self, command):
        command.cog = self
        self.__cog_commands__.append(command._update_copy(self.__cog_settings__))

    # Global error handling
    async def cog_command_error(self, ctx, error):
        raise_error = True
        if isinstance(error.original, AccountNotFound):
            raise_error = True

        em = error_embed(ctx, error.original)

        await ctx.respond(embed=em, ephemeral=True)
        if raise_error: raise error
        