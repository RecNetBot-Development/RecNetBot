import os
import json
import discord
import logging
from typing import TYPE_CHECKING, Optional
from resources import CategoryIcons
from discord.ext import commands
from discord import ApplicationCommandError
from .ModuleCollector import ModuleCollector
from discord.commands import ApplicationCommand, SlashCommand, SlashCommandGroup, UserCommand

if TYPE_CHECKING:
    from .CogManager import CogManager
    
class Cog(commands.Cog):
    def __init__(self, manager: 'CogManager', name: str):
        self.bot = manager.bot
        self.__modules = ModuleCollector()
        self.__cog_name__ = name
        self.__cog_commands__ = []
        self.__cog_groups__ = []
        #self.__command_group = SlashCommandGroup(name=self.__cog_name__, description="No description provided!", debug_guilds=cfg['test_guild_ids'])
        self.__manifest = self.__getManifest
        self.buildCog()

    @property
    def __getManifest(self):
        cog_dir = os.listdir(f"./cogs/{self.__cog_name__}")
        if "manifest.json" in cog_dir:
            with open(f"./cogs/{self.__cog_name__}/manifest.json") as manifest_json:
                return json.load(manifest_json)
        else:
            return 
        
    @property
    def icon(self) -> Optional[discord.Emoji]:
        if icon_name := self.__manifest.get("icon", None):
            if hasattr(CategoryIcons, icon_name):
                return self.bot.get_emoji(getattr(CategoryIcons, icon_name))
        
        return None    
        

    def buildCog(self):
        # Add standalone commands
        scripts = self.__manifest.get('scripts', None)
        if scripts:
            for script in scripts:
                path = f"cogs.{self.__cog_name__}.{script}"
                self.__modules.add(path)
                lib = self.__modules.get(path)
                for attr in dir(lib):
                    mod = getattr(lib, attr)
                    if isinstance(mod, ApplicationCommand):
                        """
                        add_application_command() only accepts SlashCommand or SlashCommandGroup
                        it doesn't accept subcommands (not mod.is_subcommand)
                        nor does it accept subcommand groups (not mod.parent (checks if the group has a parent group))
                        """
                        if isinstance(mod, SlashCommand) and not mod.is_subcommand or isinstance(mod, SlashCommandGroup) and not mod.parent or isinstance(mod, UserCommand):
                            self.addCommand(mod)
        
        # Add command groups
        groups = self.__manifest.get('groups', None)
        if groups:
            for name, metadata in groups.items():
                print(f"Loading command group '{name}'...")
                scripts = metadata.get("scripts", [])
                if not scripts: continue
                
                command_group = SlashCommandGroup(name=name, debug_guilds=self.bot.config.get("debug_guilds"))
                for script in scripts:
                    path = f"cogs.{self.__cog_name__}.{name}.{script}"
                    self.__modules.add(path)
                    lib = self.__modules.get(path)
                    for attr in dir(lib):
                        mod = getattr(lib, attr)
                        if isinstance(mod, ApplicationCommand):
                            """
                            add_application_command() only accepts SlashCommand or SlashCommandGroup
                            it doesn't accept subcommands (not mod.is_subcommand)
                            nor does it accept subcommand groups (not mod.parent (checks if the group has a parent group))
                            """
                            if isinstance(mod, SlashCommand) and not mod.is_subcommand or isinstance(mod, SlashCommandGroup) and not mod.parent or isinstance(mod, UserCommand):
                                command_group = self.appendCommandToGroup(mod, command_group)
                                
                command_group.description = metadata.get("description", "No description provided!")
                self.__cog_commands__.append(command_group)
                        
        self.initializeCog()
        
    def debugPrint(self, text: str) -> None:
        print(f"{self.__cog_name__}: {text}")
        
    def initializeCog(self):
        self.__cog_name__ = self.__manifest['name']
        self.__cog_description__ = self.__manifest.get('description', "No description provided!")
        self.__cog_icon__ = self.__manifest.get('icon', None)

    def appendCommandToGroup(self, command, group):
        self.debugPrint(f"Adding command '{command.name}' to group '{group.name}'...")
        
        command.cog = self
        patched_command = command._update_copy(self.__cog_settings__)
        patched_command.parent = group
        group.subcommands.append(patched_command)
        
        return group

    def addCommand(self, command):
        self.debugPrint(f"Adding command '{command.name}'...")
        
        command.cog = self
        self.__cog_commands__.append(command)
            
            
        
    async def cog_command_error(self, ctx: discord.ApplicationContext, exception: ApplicationCommandError):
        """
        Global error handling for all cogs
        """
        
        # Handle cooldowns separately
        if isinstance(exception, commands.CommandOnCooldown):
            return await ctx.interaction.response.send_message("Please try again later.", ephemeral=True)
        
        original = exception.original
        if hasattr(original, "embed"):
            await ctx.respond(embed=original.embed)
        else:
            logging.basicConfig(level=logging.WARNING, filename="error.log", filemode="a+",
                            format="%(asctime)-15s %(levelname)-8s %(message)s")
            logging.error(str(exception))
            
            # Fetch the bug report command
            misc_cog = self.bot.get_cog("Miscellaneous")
            cmd = discord.utils.get(misc_cog.__cog_commands__, name='bugreport')
            
            # Make an error embed for the user
            user_em = discord.Embed(
                title = "Something unexpected happened!",
                description = f"```{str(original)}```\nConsider telling us about what happened so this bug can be resolved quicker! {cmd.mention}",
                color = discord.Color.red()
            )
            user_em.set_footer(text="This error was logged and will be fixed soon!")
            await ctx.respond(embed=user_em)
            
            # Send error to RNB log channel
            log_em = discord.Embed(
                title=str(exception),
                description=str(original),
                color = discord.Color.red()
            )
            log_em.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            log_em.set_footer(text=ctx.command.name)
            await self.bot.log_channel.send(embed=log_em)
            
            # Raise it anyways for better debugging
            raise original
        