import os
import json
import discord
import logging
from typing import TYPE_CHECKING, Optional
from resources import CategoryIcons
from discord.ext import commands
from discord import ApplicationCommandError, Forbidden
from .ModuleCollector import ModuleCollector
from discord.commands import ApplicationCommand, SlashCommand, SlashCommandGroup, UserCommand
from exceptions import ConnectionNotFound
from recnetpy.rest.exceptions import HTTPError, InternalServerError, BadRequest, NotFound
from resources import get_icon
from embeds import get_default_embed

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
                        if isinstance(mod, SlashCommand) and not mod.is_subcommand or isinstance(mod, SlashCommandGroup) and not mod.parent or isinstance(mod, UserCommand) and mod:
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
                            if isinstance(mod, SlashCommand) and not mod.is_subcommand or isinstance(mod, SlashCommandGroup) and not mod.parent or isinstance(mod, UserCommand) and mod:
                                command_group = self.appendCommandToGroup(mod, command_group)
                            else:
                                print(f"Failed to load /{script} from {self.__cog_name__}")
                                
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
        
        original = None
        if hasattr(original, "embed"):
            original = exception.original

        if original and hasattr(original, "embed"):
            if isinstance(original, ConnectionNotFound) and "{}" in original.embed.description:
                # Fetch the link command
                user_cog = self.bot.get_cog("User")
                cmd = discord.utils.get(user_cog.__cog_commands__, name='verify')
                #group = discord.utils.get(user_cog.__cog_commands__, name='profile')
                #cmd = discord.utils.get(group.walk_commands(), name='link')
                    
                # Plug in the link command
                original.embed.description = original.embed.description.format(cmd.mention)
            
            await ctx.respond(embed=original.embed)
        else:
            # Fetch the bug report command
            misc_cog = self.bot.get_cog("Miscellaneous")
            bug_cmd = discord.utils.get(misc_cog.__cog_commands__, name='bugreport')

            # Embed template
            em = get_default_embed()
            em.set_thumbnail(url=get_icon("rectnet"))

            # Check for miscallenous errors
            if isinstance(original, Forbidden):  # Lacking permissions
                # Create embed
                em.title = "Missing Permissions!"
                em.description = "This command does not work as expected because I do not have sufficient permissions.\n" \
                                  "### Solutions:\n" \
                                  f"- [Re-invite the bot]({self.bot.config['invite_link']}) to reset permissions\n" \
                                  "- Make sure the bot does not have interfering roles\n" \
                                  "- Make sure the channel permissions do not overlap with the bot's required permissions\n" \
                                  f"- If all hope is lost, get help from [the support server]({self.bot.config['server_link']})"
            
                await ctx.respond(embed=em)
                return  # Don't report to log channel
            
            elif isinstance(original, InternalServerError | HTTPError | BadRequest | NotFound):  # Error sending request to RecNet
                # Fetch the API status command
                api_cog = self.bot.get_cog("API")
                api_cmd = discord.utils.get(api_cog.__cog_commands__, name='apistatus')

                # Create embed
                em.title = "Server error!"
                em.description = "RecNet failed to handle my request for data.\n" \
                                  "### Possible reasons:\n" \
                                  "- A freak error. Try again.\n" \
                                  "- RecNet had a breaking change and I need to be updated.\n" \
                                  f"- RecNet's servers are down. Check with {api_cmd.mention}.\n" \
                                  f"- If this error lasts for days, shoot us a {bug_cmd.mention}!"
                em.add_field(name="Exception", value=str(original))

                await ctx.respond(embed=em)

            else:  # Unknown error
                # Create embed
                em.title = "Something unexpected happened!"
                em.description = f"```{str(original)}```\nConsider telling us about what happened so this bug can be resolved quicker! {bug_cmd.mention}"
                em.set_footer(text="This error was logged and will be investigated!")

                await ctx.respond(embed=em)

            # Unknown error
            logging.basicConfig(level=logging.WARNING, filename="error.log", filemode="a+",
                            format="%(asctime)-15s %(levelname)-8s %(message)s")
            logging.error(str(exception))
            
            # Create log embed
            em.description = f"```{str(original)}```"

            # Error
            em.description += f"\n```{str(exception)}```"

            # Which command
            em.description += "\n**Command**" \
                              f"\n{ctx.command.mention}"

            # List params
            em.description += "\n\n**Parameters**"
            if ctx.selected_options:
                for param in ctx.selected_options:
                    em.description += f"\n- `{param['name']}` = `{param['value']}`"
            else:
                em.description += "\nEmpty"

            # Who ran the command
            em.set_author(name=ctx.author, icon_url=ctx.author.avatar)

            # Clear the footer
            em.set_footer(text="")

            # Send error to RNB log channel
            await self.bot.log_channel.send(embed=em)
            
            # Raise it anyways for better debugging
            raise original
        