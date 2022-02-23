import os
from discord.ext import commands
from utility.ModuleCollector import ModuleCollector
from discord.commands import ApplicationCommand, SlashCommand, SlashCommandGroup
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
                        """
                        add_application_command() only accepts SlashCommand or SlashCommandGroup
                        it doesn't accept subcommands (not mod.is_subcommand)
                        nor does it accept subcommand groups (not mod.parent (checks if the group has a parent group))
                        """
                        if isinstance(mod, SlashCommand) and not mod.is_subcommand or isinstance(mod, SlashCommandGroup) and not mod.parent:
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

        em = error_embed(ctx, error)

        await ctx.respond(embed=em, ephemeral=True)
        if raise_error: raise error