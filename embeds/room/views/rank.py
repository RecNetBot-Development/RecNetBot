import discord
from ..room_embed import room_embed
from utility.emojis import get_emoji
from random import randint
from utility.discord_helpers.helpers import respond as _respond
from utility.discord_helpers.helpers import edit_message
from ..room_rank_embed import room_rank_embed

class RankRoomSelect(discord.ui.Select):
    def __init__(self, rank_view, rooms):
        super().__init__(
            row=0, 
            placeholder="Room", 
            custom_id="persistent:room_rank_select", 
            options=
                [   
                    discord.SelectOption(label=room['Name'], description=f"Inspect ^{room['Name']}") for room in rooms
                ]
        )
        self.rank_view = rank_view

    async def callback(self, interaction):
        room_chosen = self.values[0]
        await self.rank_view.display_room(room_chosen, interaction)

class RankBackButton(discord.ui.Button):
    def __init__(self, rank_view):
        super().__init__(
            row=1,
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
        self.main_embed = None
        
        # Add dropdown menu for rooms
        self.add_item(RankRoomSelect(self, self.rooms))
        self.add_item(RankBackButton(self))
            
    async def display_room(self, room_name, interaction):
        room = await self.rec_net.room(name=room_name, info=["tags", "subrooms", "roles", "scores"], includes=["roles", "creator"])
        embed = room_embed(room)
        await edit_message(interaction, embed=embed, view=self)
        
    async def go_back(self, interaction):
        if not self.main_embed: self.main_embed = room_rank_embed(self.rooms, self.tags, self.keywords)
        await edit_message(interaction, embed=self.main_embed, view=self)
            
    async def respond(self, ctx):
        if not self.main_embed: self.main_embed = room_rank_embed(self.rooms, self.tags, self.keywords)
        await _respond(ctx, embed=self.main_embed, view=self)
    