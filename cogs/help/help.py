import discord
from discord.ext import commands
from discord.commands import slash_command
from embeds import get_default_embed
from resources import get_emoji
from typing import List


class HelpView(discord.ui.View):
    def __init__(self, bot: commands.Bot, context: discord.ApplicationContext):
        super().__init__()
        self.bot = bot
        self.ctx = context
        self.cogs = list(filter(lambda ele: ele.get_commands(), self.bot.cogs.values()))  # Only include cogs with commands
        self.commands = []
        self.embed = None
        
        self.add_item(Dropdown(self))
        
    def initialize(self) -> discord.Embed:
        """
        Generates the first embed
        """
        
        self.register_selections(self.cogs)
        return self.embed
        
        
    def register_selections(self, selections: List[commands.Cog]):
        """
        Takes in selected cogs and creates the command list
        """
        
        self.commands = []
        
        # List all commands from commands to a single list
        for cog in selections:
            for cmd in cog.walk_commands():
                if not isinstance(cmd, discord.SlashCommand): continue  # Only allow slash commands for now
                self.commands.append(cmd)
                
        # Sort in alphabetical order
        self.commands.sort(key=lambda cmd: cmd.name)
        
        self.embed = self.create_embed()
        
        
    def create_embed(self) -> discord.Embed:
        """
        Creates a help page embed
        """
        
        em = get_default_embed()
        pieces = []
        
        for cmd in self.commands:
            pieces.append(f"{cmd.mention}\n{get_emoji('arrow')} {cmd.description}")
            
        em.description = "\n".join(pieces)
        
        return em
        
        
    async def refresh(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=self.embed, view=self)
        
        
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
    name="help",
    description="Get help with navigating RecNetBot!"
    
)
async def help(self, ctx: discord.ApplicationContext):
    view = HelpView(self.bot, context=ctx)
    em = view.initialize()
    await ctx.respond(view=view, embed=em)