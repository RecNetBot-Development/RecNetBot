import discord
from discord.ext import commands
from embeds import get_default_embed
from resources import get_emoji
from typing import List, Optional
from recnetpy.dataclasses.invention import Invention
from discord.commands import slash_command
from discord.ext.bridge import BridgeOption as Option
from utils.paginator import RNBPaginator, RNBPage
from exceptions import Disabled

class RankView(discord.ui.View):
    def __init__(self, bot: commands.Bot, context: discord.ApplicationContext, invention_pool = List[Invention], filters: str = None):
        super().__init__()
        self.bot = bot
        self.ctx = context
        self.invention_pool = invention_pool
        self.embeds = {
            "cheers": None,
            "downloads": None,
            "rooms": None
        }
        self.filters = filters
        self.paginator = None
        self.scope = 16
        
        self.add_item(Dropdown(self))
        
    def initialize(self) -> discord.Embed:
        """
        Generates the first embed
        """
        
        self.register_selections("Cheers")
        return self.embeds["cheers"]
        
        
    def register_selections(self, selection: str):
        if not self.embeds[selection.lower()]:
            match selection:
                case "Cheers":
                    invs = sorted(self.invention_pool, key=lambda inv: inv.cheer_count, reverse=True)
                    
                case "Downloads":
                    invs = sorted(self.invention_pool, key=lambda inv: inv.num_downloads, reverse=True)
                    
                case "Rooms":
                    invs = sorted(self.invention_pool, key=lambda inv: inv.num_players_have_used_in_room, reverse=True)
            
            self.embeds[selection.lower()] = self.create_embed(invs[:self.scope-1], selection)
            
        
    def create_embed(self, inventions: Optional[List[Invention]], selection: str) -> discord.Embed:
        """
        Creates invention page embeds
        """
        em = get_default_embed()
        em.title = f"Inventions ranked based on keywords and tags"
        
        if not inventions:
            em.description = "No inventions found!"
            return [RNBPage(embeds=[em])]
            
        ranked = ""
        for placement, inv in enumerate(inventions, start=1):
            match selection:
                case "Cheers":
                    em.description = f"Ranked by **cheers**\n`Invention` • {get_emoji('cheer')} Cheers"
                    details = f"{inv.cheer_count:,}"
                    
                case "Downloads":
                    em.description = f"Ranked by **downloads**\n`Invention` • {get_emoji('download')} Downloads"
                    details = f"{inv.num_downloads:,}"
                    
                case "Rooms":
                    em.description = f"Ranked by **usage in separate rooms**\n`Invention` • {get_emoji('room')} Rooms"
                    details = f" {inv.num_players_have_used_in_room:,}"
                    
            ranked += f"**{placement}.** `{inv.name}` • {details}\n"
            
        if self.filters:
            em.description = f"Filters: `{self.filters}`\n" + em.description
            
        em.add_field(name="Ranking", value=ranked)
        
        return [RNBPage(embeds=[em])]
        
        
    async def refresh(self, interaction: discord.Interaction, selection: str):
        await interaction.response.defer(invisible=True)
        
        self.register_selections(selection)
        await self.paginator.update(pages=self.embeds[selection.lower()], custom_view=self)
        
        
class Dropdown(discord.ui.Select):
    def __init__(self, view):
        self.rank_view = view

        options = [
            discord.SelectOption(
                label="Cheers",
                description="By how many cheers",
                emoji=get_emoji('cheer')
            ),
            discord.SelectOption(
                label="Downloads",
                description="By how many downloads",
                emoji=get_emoji('download')
            ),
            discord.SelectOption(
                label="Rooms",
                description="By how many times used in separate rooms",
                emoji=get_emoji('room')
            )
        ]

        super().__init__(
            placeholder="Ranking Method",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        """
        Returns chosen category back to the view
        """
        await self.rank_view.refresh(interaction, self.values[0])

@slash_command(
    name="rank",
    description="Ranks inventions in a leaderboard by filters."
)
async def rank(
    self, 
    ctx: discord.ApplicationContext,
    filter: Option(str, name="filter", description="Enter keywords or #tags. Example: door #gadget", required=False)
):
    await ctx.interaction.response.defer()
    
    # Broken command
    raise Disabled

    if filter:
        results = await self.bot.RecNet.inventions.search(filter, take=200)
    else:
        results = await self.bot.RecNet.inventions.featured(take=100)
    
    view = RankView(self.bot, context=ctx, invention_pool=results, filters=filter)
    embeds = view.initialize()
    paginator = RNBPaginator(pages=embeds, custom_view=view, show_indicator=False, show_disabled=False)
    view.paginator = paginator
    await paginator.respond(ctx.interaction)