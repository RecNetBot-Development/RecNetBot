import discord
from ..room_embed import room_embed
from utility.emojis import get_emoji
from random import randint
from utility.discord_helpers.helpers import respond as _respond
from utility.discord_helpers.helpers import edit_message
from ..room_rank_embed import room_rank_embed

def shorten(text, limit = 80):
    return text[:limit] + (text[limit:] and '..')

class RankRoomSelect(discord.ui.Select):
    def __init__(self, rank_view, rooms):
        options = []
        for room in rooms:
            # Limit is 100 characters
            if len(room['Name']) > 100:
                continue
            
            options.append(
                discord.SelectOption(
                    label=room['Name'], 
                    description=shorten(f"Inspect ^{room['Name']}"))
                )
        
        super().__init__(
            row=0, 
            placeholder="Room", 
            custom_id="persistent:room_rank_select", 
            options=options
        )
        self.rank_view = rank_view

    async def callback(self, interaction):
        room_chosen = self.values[0]
        await self.rank_view.display_room(room_chosen, interaction)
        
class RankRoomRankingSelect(discord.ui.Select):
    def __init__(self, rank_view):
        super().__init__(
            row=1, 
            placeholder="Ranking Method", 
            custom_id="persistent:room_rank_method", 
            options=
                [   
                    discord.SelectOption(label="Popularity", description="RecNet's Ranking Method"),
                    discord.SelectOption(label="Cheers", description="Rank by Cheers"),
                    discord.SelectOption(label="Favorites", description="Rank by Favorites"),
                    discord.SelectOption(label="Visits", description="Rank by Visits"),
                    discord.SelectOption(label="Visitors", description="Rank by Visitors")
                ]
        )
        self.rank_view = rank_view

    async def callback(self, interaction):
        method_chosen = self.values[0]
        await self.rank_view.update_ranking(method_chosen, interaction)
        
class RankBackButton(discord.ui.Button):
    def __init__(self, rank_view):
        super().__init__(
            row=2,
            label="Go Back"
        )
        self.rank_view = rank_view
                
    async def callback(self, interaction):
        await self.rank_view.go_back(interaction)

class Rank(discord.ui.View):
    def __init__(self, rec_net, rooms, tags, keywords):
        super().__init__(
            timeout=None
        )
        self.tags = tags
        self.keywords = keywords
        self.rec_net = rec_net
        self.rooms = rooms
        self.default_rooms_ranking = self.rooms
        self.main_embed = None
        self.embeds = {}
        self.saved_room_embeds = {}
        
        # Add dropdown menu for rooms
        self.update_items()
            
    async def update_ranking(self, method, interaction):
        if method in self.embeds:
            self.main_embed = self.embeds[method]
        else:
            match method:
                case "Popularity":
                    self.rooms = self.default_rooms_ranking
                case "Cheers":
                    self.rooms.sort(key=lambda room: room["Stats"]["CheerCount"], reverse=True)
                case "Favorites":
                    self.rooms.sort(key=lambda room: room["Stats"]["FavoriteCount"], reverse=True)
                case "Visits":
                    self.rooms.sort(key=lambda room: room["Stats"]["VisitCount"], reverse=True)
                case "Visitors":
                    self.rooms.sort(key=lambda room: room["Stats"]["VisitorCount"], reverse=True)
            
            self.main_embed = room_rank_embed(self.rooms, self.tags, self.keywords, method)
            self.embeds[method] = self.main_embed
        await self.go_back(interaction)
            
    async def display_room(self, room_name, interaction):
        self.update_items(displaying_room=True)
        if room_name not in self.saved_room_embeds:
            room = await self.rec_net.room(name=room_name, info=["tags", "subrooms", "roles", "scores"], includes=["roles", "creator"])
            self.saved_room_embeds[room_name] = room_embed(room)
        await edit_message(interaction, embed=self.saved_room_embeds[room_name], view=self)
        
    async def go_back(self, interaction):
        self.update_items()
        await edit_message(interaction, embed=self.main_embed, view=self)
            
    async def respond(self, ctx):
        self.update_items()
        if not self.main_embed: self.main_embed = room_rank_embed(self.rooms, self.tags, self.keywords)
        self.embeds["Popularity"] = self.main_embed
        await _respond(ctx, embed=self.main_embed, view=self)
        
    def update_items(self, displaying_room=False):
        self.clear_items()
        self.add_item(RankRoomSelect(self, self.rooms))
        if displaying_room: self.add_item(RankBackButton(self))
        if not displaying_room: self.add_item(RankRoomRankingSelect(self))
        
    