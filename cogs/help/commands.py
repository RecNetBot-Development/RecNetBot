from dataclasses import dataclass
import discord
from discord.ext import commands
from discord.commands import slash_command
from embeds import get_default_embed
from resources import get_emoji
from typing import List
from utils import chunks
from utils.paginator import RNBPaginator, RNBPage

@dataclass
class Group:
    name: str
    description: str
    mention: str

class HelpView(discord.ui.View):
    def __init__(self, bot: commands.Bot, context: discord.ApplicationContext, invite_link: str = None, server_link: str = None):
        super().__init__()
        self.bot = bot
        self.ctx = context
        self.cogs = list(filter(lambda ele: ele.get_commands(), self.bot.cogs.values()))  # Only include cogs with commands
        self.commands = []
        self.embeds = []
        self.selected_cogs = []
        self.paginator = None
        
        self.add_item(Dropdown(self))
        
        """
        buttons = []
        # Invite bot button
        if invite_link:
            invite_btn = discord.ui.Button(
                label="Invite Bot",
                url=invite_link,
                style=discord.ButtonStyle.link,
                row=3
            )
            buttons.append(invite_btn)
        
        # Join discord button
        if server_link:
            server_btn = discord.ui.Button(
                label="Join Discord",
                url=server_link,
                style=discord.ButtonStyle.link,
                row=3
            )
            buttons.append(server_btn)
        
        # add buttons
        for item in buttons:
            self.add_item(item)
        """
        
        
    def initialize(self) -> discord.Embed:
        """
        Generates the first embed
        """
        
        self.register_selections(self.cogs)
        return self.embeds
        
        
    def register_selections(self, selections: List[List[commands.Cog]]):
        """
        Takes in selected cogs and creates the command list
        """
        
        self.commands = []
        self.selected_cogs = selections
        
        # List all commands from commands to a single list
        groups = []
        commands = []
        for cog in selections:
            for cmd in cog.walk_commands():
                if not isinstance(cmd, discord.SlashCommand): continue  # Only allow slash commands for now
                
                if cmd.is_subcommand:  # Add the group
                    # Make sure there's no duplicate groups
                    group = cmd.parent
                    if group in groups: continue
                    groups.append(cmd.parent)
                    
                    # Make a mockup class for the help command
                    commands.append(
                        Group(
                            group.name, group.description.format(len(group.subcommands)), f"</{group.name}:0>"
                        )
                    )
                    continue
                
                commands.append(cmd)
                
        # Sort in alphabetical order
        commands.sort(key=lambda cmd: cmd.name)
        
        # Make pages of n commands
        self.commands = chunks(commands, 8)
        self.embeds = self.create_embeds()
        
        
    def create_embeds(self) -> discord.Embed:
        """
        Creates help page embeds
        """
        
        # Generate title with all selected cogs
        #if self.selected_cogs or self.selected_cogs != self.cogs:
        #    cog_names = list(map(lambda cog: cog.qualified_name.lower(), self.selected_cogs))
        #    title = ", ".join(cog_names).capitalize() + " commands"
        #else:
        #    title = "All commands"
            
        # Generate each embed page
        embeds = []  
        for page in self.commands:
            pieces = []
            em = get_default_embed()
            for cmd in page:
                pieces.append(f"{cmd.mention}\n{get_emoji('arrow')} {cmd.description}")
            
            #em.title = title
            em.description = "\n".join(pieces)
            embeds.append(RNBPage(embeds=[em]))
        
        return embeds
        
        
    async def refresh(self, interaction: discord.Interaction):
        #await interaction.response.edit_message(embed=self.embed, view=self)
        await interaction.response.defer(invisible=True)
        await self.paginator.update(pages=self.embeds, custom_view=self)
        
        
class Dropdown(discord.ui.Select):
    def __init__(self, view: HelpView):
        self.help_view = view
        self.bot = self.help_view.bot
        self.cogs = self.help_view.cogs
        
        # Create selection options with cogs
        options = [
            discord.SelectOption(
                label="All"
            )
        ]
        for cog in self.cogs:
            select = discord.SelectOption(
                label=cog.qualified_name,
                emoji=cog.icon
                #description=cog.description
            )
            
            options.append(select)

        super().__init__(
            placeholder="Select Categories",
            min_values=1,
            max_values=len(options),
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        """
        Returns chosen categories back to the view
        """
        if "All" in self.values:
            cogs = self.cogs
        else:
            cogs = list(filter(lambda ele: ele.qualified_name in self.values, self.cogs))
             
        self.help_view.register_selections(cogs)
        await self.help_view.refresh(interaction)


@slash_command(
    name="commands",
    description="View all of RecNetBot's commands!"
    
)
async def commands(self, ctx: discord.ApplicationContext):
    server_link, invite_link = self.bot.config.get("server_link", None), self.bot.config.get("invite_link", None)
    
    view = HelpView(self.bot, context=ctx, server_link=server_link, invite_link=invite_link)
    embeds = view.initialize()
    paginator = RNBPaginator(pages=embeds, custom_view=view, show_indicator=False, trigger_on_display=True, hidden_items=["first", "last", "random", "next10", "prev10"], default_button_row=3)
    view.paginator = paginator
    await paginator.respond(ctx.interaction)