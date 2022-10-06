import os
import json
import time
import discord
import logging
from typing import TYPE_CHECKING
from discord.ext import commands
from discord import ApplicationCommandError
from .ModuleCollector import ModuleCollector
from discord.commands import ApplicationCommand, SlashCommand, SlashCommandGroup, UserCommand
from exceptions import RNBException

if TYPE_CHECKING:
    from .CogManager import CogManager
    
class Cog(commands.Cog):
    def __init__(self, manager: 'CogManager', name: str):
        self.bot = manager.bot
        self.__modules = ModuleCollector()
        self.__cog_name__ = name
        self.__cog_commands__ = []
        #self.__command_group = SlashCommandGroup(name=self.__cog_name__, description="No description provided!", debug_guilds=cfg['test_guild_ids'])
        self.__manifest = self.__getManifest
        self.__categorize_commands = False
        self.buildCog()

    @property
    def __getManifest(self):
        cog_dir = os.listdir(f"./cogs/{self.__cog_name__}")
        if "manifest.json" in cog_dir:
            with open(f"./cogs/{self.__cog_name__}/manifest.json") as manifest_json:
                return json.load(manifest_json)
        else:
            return 

    def buildCog(self):
        scripts = self.__manifest.get('scripts', None)
        if not scripts: return self.debugPrint("No scripts, skipping...")
            
        for script in scripts:
            self.__modules.add(f"cogs.{self.__cog_name__}.{script}")
            lib = self.__modules.get(f"cogs.{self.__cog_name__}.{script}")
            for attr in dir(lib):
                if isinstance(getattr(lib, attr), ApplicationCommand):
                    mod = getattr(lib, attr)
                    """
                    add_application_command() only accepts SlashCommand or SlashCommandGroup
                    it doesn't accept subcommands (not mod.is_subcommand)
                    nor does it accept subcommand groups (not mod.parent (checks if the group has a parent group))
                    """
                    if isinstance(mod, SlashCommand) and not mod.is_subcommand or isinstance(mod, SlashCommandGroup) and not mod.parent or isinstance(mod, UserCommand):
                        self.addCommand(mod)
                        
        self.initializeCog()
        
    def debugPrint(self, text: str) -> None:
        print(f"{self.__cog_name__}: {text}")
        
    def initializeCog(self):
        self.__cog_name__ = self.__manifest['name']
        self.__cog_description__ = self.__manifest.get('description', "No description provided!")
        self.__cog_icon__ = self.__manifest.get('icon', None)
        if self.__categorize_commands: self.__cog_commands__.append(self.__command_group)

    def addCommand(self, command):
        self.debugPrint(f"Adding command '{command.name}'...")
        
        command.cog = self
        patched_command = command._update_copy(self.__cog_settings__)
        if self.__categorize_commands:
            patched_command.parent = self.__command_group
            self.__command_group.subcommands.append(patched_command)
        else:
            self.__cog_commands__.append(command)
            
        
    async def cog_command_error(self, ctx: discord.ApplicationContext, exception: ApplicationCommandError):
        """
        Global error handling for all cogs
        """
        
        original = exception.original
        if hasattr(original, "embed"):
            await ctx.respond(embed=original.embed)
        else:
            logging.basicConfig(level=logging.WARNING, filename="error.log", filemode="a+",
                            format="%(asctime)-15s %(levelname)-8s %(message)s")
            logging.error(str(exception))
            return await ctx.respond(f"An unknown error occurred! {str(original)}")
            
        