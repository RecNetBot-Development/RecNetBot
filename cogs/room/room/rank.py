import discord
from discord.ext import commands
from embeds import get_default_embed
from resources import get_emoji
from typing import List, Optional
from recnetpy.dataclasses.room import Room
from discord.commands import slash_command, Option
from utils.paginator import RNBPaginator, RNBPage


class RankView(discord.ui.View):
    def __init__(self, bot: commands.Bot, context: discord.ApplicationContext, room_pool = List[Room], filters: str = None):
        super().__init__()
        self.bot = bot
        self.ctx = context
        self.room_pool = room_pool
        self.embeds = {
            "popularity": None,
            "cheers": None,
            "comments": None,
            "favorites": None,
            "visits": None,
            "visitors": None
        }
        self.filters = filters
        self.paginator = None
        self.scope = 16
        
        self.add_item(Dropdown(self))
        
    def initialize(self) -> discord.Embed:
        """
        Generates the first embed
        """
        
        self.register_selections("Popularity")
        return self.embeds["popularity"]
        
        
    def register_selections(self, selection: str):
        if not self.embeds[selection.lower()]:
            match selection:
                case "Popularity":
                    rooms = self.room_pool
                    
                case "Cheers":
                    rooms = sorted(self.room_pool, key=lambda room: room.cheer_count, reverse=True)
                    
                case "Favorites":
                    rooms = sorted(self.room_pool, key=lambda room: room.favorite_count, reverse=True)
                    
                case "Visits":
                    rooms = sorted(self.room_pool, key=lambda room: room.visit_count, reverse=True)
                    
                case "Visitors":
                    rooms = sorted(self.room_pool, key=lambda room: room.visitor_count, reverse=True)
            
            self.embeds[selection.lower()] = self.create_embed(rooms[:self.scope-1], selection)
            
        
    def create_embed(self, rooms: Optional[List[Room]], selection: str) -> discord.Embed:
        """
        Creates role page embeds
        """
        em = get_default_embed()
        em.title = f"Rooms ranked based on keywords and tags"
        
        if not rooms:
            em.description = "No rooms found!"
            return [RNBPage(embeds=[em])]
            
        ranked = ""
        for placement, room in enumerate(rooms, start=1):
            match selection:
                case "Popularity":
                    em.description = f"Ranked by **RecNet's ranking system**\n`^Room` • {get_emoji('cheer')} Cheers"
                    details = f"{room.cheer_count:,}"
                    
                case "Cheers":
                    em.description = f"Ranked by **cheers**\n`^Room` • {get_emoji('cheer')} Cheers"
                    details = f"{room.cheer_count:,}"
                    
                case "Favorites":
                    em.description = f"Ranked by **favorites**\n`^Room` • {get_emoji('favorite')} Favorites"
                    details = f"{room.favorite_count:,}"
                    
                case "Visits":
                    em.description = f"Ranked by **total visits**\n`^Room` • {get_emoji('visitor')} Visits"
                    details = f" {room.visit_count:,}"
                    
                case "Visitors":
                    em.description = f"Ranked by **unique visitors**\n`^Room` • {get_emoji('visitor')} Visitors"
                    details = f"{room.visitor_count:,}"
                    
            ranked += f"**{placement}.** `^{room.name}` • {details}\n"
            #ranked += f"**{placement}.** `^{room.name}`\n{details}\n\n"
            
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
                label="Popularity",
                description="RecNet's way of ranking",
                emoji=get_emoji('level')
            ),
            discord.SelectOption(
                label="Cheers",
                description="By how many cheers",
                emoji=get_emoji('cheer')
            ),
            discord.SelectOption(
                label="Favorites",
                description="By how many favorites",
                emoji=get_emoji('favorite')
            ),
            discord.SelectOption(
                label="Visits",
                description="By how many total visits",
                emoji=get_emoji('visitor')
            ),
            discord.SelectOption(
                label="Visitors",
                description="By how many unique visitors",
                emoji=get_emoji('visitors')
            ),
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
    description="Ranks rooms in a leaderboard by filters."
)
async def rank(
    self, 
    ctx: discord.ApplicationContext,
    filter: Option(str, name="filter", description="Enter keywords or #tags. Example: pvp #contest", required=False)
):
    await ctx.interaction.response.defer()
    
    if filter:
        results = await self.bot.RecNet.rooms.search(filter, take=200)
    else:
        results = await self.bot.RecNet.rooms.hot(take=200)
    
    view = RankView(self.bot, context=ctx, room_pool=results, filters=filter)
    embeds = view.initialize()
    paginator = RNBPaginator(pages=embeds, custom_view=view, show_indicator=False, show_disabled=False)
    view.paginator = paginator
    await paginator.respond(ctx.interaction)