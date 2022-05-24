import discord
from utility.discord_helpers.helpers import edit_message
from embeds.base.embed import DefaultEmbed as Embed
from utility import load_cfg, respond
from discord.commands import slash_command
from utility.emojis import get_emoji  # Importing the decorator that makes slash commands.

cfg = load_cfg()
        
"""BUTTONS"""
class MainMenuButton(discord.ui.Button):
    def __init__(self, bot, ctx):
        self._ctx = ctx
        self._bot = bot
        super().__init__(
            label="Back to Main Menu",
            row=0,
            style=discord.ButtonStyle.primary
        )
        
    async def callback(self, interaction: discord.Interaction):
        embed = main_menu(self._bot)
        view = HelpMainView(self._ctx, self._bot)
                                            
        await edit_message(
            self._ctx, 
            interaction, 
            embed=embed,
            view=view
        )
        
class CategoryButton(discord.ui.Button):
    def __init__(self, cog, bot, ctx):
        self._ctx = ctx
        self._bot = bot
        self._cog = cog
        super().__init__(
            label="Back to Category",
            row=0,
            style=discord.ButtonStyle.secondary
        )
        
    async def callback(self, interaction: discord.Interaction):
        embed = create_category_help_page(self._cog, self._ctx)
        view = HelpCategoryView(self._cog, self._ctx, self._bot)
        
        await edit_message(
            self._ctx, 
            interaction, 
            embed=embed,
            view=view
        )
    
        
"""COMMANDS"""
def create_command_help_page(command, ctx):
    name = f"/{command.parent.name + ' ' if command.parent else ''}{command.name}"

    embed = Embed(
        title=f"{name} (from {command.cog.icon} {command.cog.qualified_name})",
        description=command.description if command.description else "No description provided!"  
    )
    
    def parse_choices(choice):
        return f"`{choice.name}`"
    
    if command.options:
        params = '\r\r'.join([  # Each parameter
                '\r'.join([  # Parameter information
                    f"`{param.name}` {'*Required*' if param.required else '*Optional*'}",
                    f"{param.description}",
                    f"*Options* ({', '.join(map(parse_choices, param.choices))})" if param.choices else '',
                ])
            for param in command.options
            ])
        
        embed.add_field(
            name="Parameters", 
            value=params, 
            inline=False
        )
    
    return embed

class HelpCommandView(discord.ui.View):
    def __init__(self, cog, ctx, bot):
        super().__init__()
        self.ctx = ctx

        # Adds the dropdown to the view object.
        self.add_item(HelpCategoryNavigation(cog, ctx, bot))
        self.add_item(MainMenuButton(bot, ctx))
        self.add_item(CategoryButton(cog, bot, ctx))
        
    async def interaction_check(self, interaction):
        return self.ctx.user == interaction.user

"""CATEGORIES"""       
class HelpCategoryNavigation(discord.ui.Select):
    def __init__(self, cog, ctx, bot):
        self._cog = cog
        self._commands = self._cog.walk_commands()
        self._options = self.get_command_options(self._commands)
        self._ctx = ctx
        self._bot = bot
        
        super().__init__(
            placeholder="Command Details",
            options=[self._options[option]['select_option'] for option in self._options],
            row=1
        )

    def get_command_options(self, commands):
        options = {}
        for command in commands:
            if isinstance(command, discord.SlashCommandGroup): 
                for subcommand in command.subcommands:   
                    options[subcommand.name.lower()] = {
                        "select_option": discord.SelectOption(label=f"/{command.name} {subcommand.name}", description=subcommand.description),
                        "command": subcommand
                    }
                    
                continue

            options[command.name.lower()] = {
                "select_option": discord.SelectOption(label=f"/{command.name}", description=command.description),
                "command": command
            }

        return options
    
    def list_and_combine_commands(self):
        commands_combined = {}
        for command in self._commands:
            if isinstance(command, discord.SlashCommandGroup): 
                for subcommand in command.subcommands:  
                    commands_combined[subcommand.name.lower()] = subcommand
                    
                continue

            commands_combined[command.name.lower()] = command
        return commands_combined

    async def callback(self, interaction: discord.Interaction):
        option = self._options.get(self.values[0].lower().split(" ")[-1].replace("/", ""))
        if option and "command" in option:
            embed = create_command_help_page(option['command'], self._ctx)
            view = HelpCommandView(self._cog, self._ctx, self._bot)
            
            await edit_message(
                self._ctx, 
                interaction, 
                embed=embed,
                view=view
            )
        
            
def create_category_help_page(cog, ctx):
    embed = Embed(
        title=f"{cog.icon} {cog.qualified_name}",
        description=cog.description + " View more details of a command by selecting it on the dropdown component."
    )

    uncategorized_commands = []
    for command in cog.get_commands():
        if isinstance(command, discord.SlashCommandGroup):
            embed.add_field(
                name=f"/{command.name}",
                value=", ".join([f"`{subcommand.name}`" for subcommand in command.subcommands]),
                inline=False
            )
            continue

        uncategorized_commands.append(command)
            
    if uncategorized_commands:
        commands = ", ".join([f"`/{command.name}`" for command in uncategorized_commands])
        embed.add_field(
            name="Uncategorized Commands", 
            value=commands, 
            inline=False
        )

    return embed
        
class HelpCategoryView(discord.ui.View):
    def __init__(self, cog, ctx, bot):
        super().__init__()
        self.ctx = ctx

        # Adds the dropdown to the view object.
        self.add_item(HelpCategoryNavigation(cog, ctx, bot))
        self.add_item(MainMenuButton(bot, ctx))
        
    async def interaction_check(self, interaction):
        return self.ctx.user == interaction.user
 
 
"""MAIN MENU"""
def main_menu(bot):
    cogs = bot.cogs
    
    embed = Embed(
        title='RecNetBot',
        description="Navigate the categories and view command details with the dropdown component!"
    )

    for key, cog in cogs.items():
        embed.add_field(
            name=f"{cog.icon} {cog.qualified_name}", 
            value=cog.description
        )
        
    info_parts = [
        f"{get_emoji('stats')} I am in `{len(bot.guilds)}` servers so far!"
    ]  # Default info parts
    if 'bot_invite_link' in cfg:
        info_parts.append(
            f"{get_emoji('discord')} Want me in your server? Invite me with [this link]({cfg['bot_invite_link']})!"
        )
    if 'server_link' in cfg:
        info_parts.append(
            f"{get_emoji('questions')} If you have any questions, run into a bug or have feedback, let us know in my [home server]({cfg['server_link']})!"
        )
    if 'github_link' in cfg:
        info_parts.append(
            f"{get_emoji('github')} I am open source! Check out my [GitHub repository]({cfg['github_link']})."
        )
        
    if info_parts:
        embed.add_field(
            name="Information",
            value='\n'.join(info_parts),
            inline=False
        )
        
    embed.add_field(
        name="Where is V2?",
        value=
        "As you might have noticed, RecNetBot is not what it used to be.\r"
        "Unfortunately, RecNetBot's second iteration, V2, broke recently. This means we're forced to rework the bot.\r"
        "As you might have noticed, some commands may be missing. Don't worry, we're doing our best to port all previous commands over.\r"
        "Thank you for understanding!\r"
    )
        
    return embed

class HelpMainNavigation(discord.ui.Select):
    def __init__(self, ctx, bot):
        self._ctx = ctx
        self._bot = bot
        self._options = self.get_category_options(self._bot.cogs)
        
        super().__init__(
            placeholder="Category Details",
            options=[self._options[option]['select_option'] for option in self._options],
            row=1
        )

    def get_category_options(self, cogs):
        options = {}  # Help category navigation options
        for key, cog in cogs.items():
            options[cog.qualified_name.lower()] = {
                "select_option": discord.SelectOption(label=cog.qualified_name, description=cog.description, emoji=cog.icon),
                "cog": cog
            }

        return options
    
    async def callback(self, interaction: discord.Interaction):
        option = self._options.get(self.values[0].lower())
        if option and "cog" in option:
            embed = create_category_help_page(option['cog'], self._ctx)
            view = HelpCategoryView(option['cog'], self._ctx, self._bot)
            
            await edit_message(
                self._ctx, 
                interaction, 
                embed=embed,
                view=view
            )
        
        else:
            embed = main_menu(self._bot)
                                              
            await edit_message(
                self._ctx, 
                interaction, 
                embed=embed,
                view=view
            )
    
class HelpMainView(discord.ui.View):
    def __init__(self, ctx, bot):
        super().__init__()
        self.ctx = ctx
        
        # Adds the dropdown to the view object.
        self.add_item(HelpMainNavigation(ctx, bot))
        
    async def interaction_check(self, interaction):
        return self.ctx.user == interaction.user
        
@slash_command(
    debug_guilds=cfg['test_guild_ids'],
    name="help",
    description="The help command to help you use RecNetBot!"
)
async def help(
    self, 
    ctx
):
    await ctx.interaction.response.defer()
    embed = main_menu(self.bot)
    view = HelpMainView(ctx, self.bot)
    await respond(ctx, embed=embed, view=view)
