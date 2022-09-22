import os
import json
import time
from discord.ext import commands
from base_commands.base_posts import MissingArguments
from embeds.image.views.image_browser import MissingPosts
from rec_net.exceptions import *
from utility.ModuleCollector import ModuleCollector
from discord.commands import ApplicationCommand, SlashCommand, SlashCommandGroup
from embeds import error_embed
from utility.discord_helpers.helpers import respond
from utility.funcs import unix_timestamp, load_cfg
from utility.emojis import get_emoji
from datetime import datetime

cfg = load_cfg()
print(cfg)

class Cog(commands.Cog):
    def __init__(self, manager, name):
        self.bot = manager.bot
        self.__modules = ModuleCollector()
        self.__cog_name__ = name
        self.__cog_commands__ = []
        self.__cog_icon__ = ""
        self.__command_group = SlashCommandGroup(name=self.__cog_name__, description="No description provided!", debug_guilds=cfg['test_guild_ids'])
        self.__manifest = self.__getManifest
        self.__categorize_commands = self.__manifest.get('cog_group', True)
        self.buildCog()

    @property
    def icon(self):
        emoji = get_emoji(self.__cog_icon__, self.bot)
        return emoji

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
                    if isinstance(mod, SlashCommand) and not mod.is_subcommand or isinstance(mod, SlashCommandGroup) and not mod.parent:
                        self.addCommand(mod)
                        
        self.initializeCog()
        
    def debugPrint(self, text):
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

    # Global error handling
    async def cog_command_error(self, ctx, error):
        ignored_errors = [
            AccountNotFound,
            RoomNotFound,
            EventNotFound,
            ImageNotFound,
            MissingArguments,
            MissingPosts,
            NoTaggedPosts,
            NoSharedPosts,
            NameServerUnavailable,
            InvalidBioForPerspective
        ]
        
        if error.original.__class__ in ignored_errors:
            # Ignore any already handled error
            em = error_embed(error.original)
            await respond(ctx, embed=em, ephemeral=True)
        else:
            # Error for developers
            error_message = f"""
**Unexpected error occurred!**
{unix_timestamp(int(time.mktime(datetime.now().timetuple())))}
Author `{ctx.author}`
Guild `{ctx.guild.name}`
Command `/{ctx.command.name}`
```
{error}
```
            """
            em = error_embed(custom_text=error_message)
            await self.bot.get_channel(cfg['error_log_channel']).send(embed=em)  # Send it to the developer error log channel
            
            # Error for users
            friendly_error_message = f"**Something unexpected occurred!**\n" \
                                     f"Unable to process the request. I may be malfunctioning or Rec Room's servers are down."
                            
            em = error_embed(custom_text=friendly_error_message)
            await respond(ctx, embed=em, ephemeral=True)  # Send it to chat
            raise error