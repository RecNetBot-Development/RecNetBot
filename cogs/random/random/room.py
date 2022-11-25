import discord
import recnetpy
import random
from embeds import fetch_room_embed
from typing import List
from recnetpy.dataclasses.image import Image
from discord.commands import slash_command

class RandomRoom(discord.ui.View):
    def __init__(self, rec_net: recnetpy.Client, amount: int = 1):
        super().__init__()
        self.RecNet = rec_net
        self.time_out = 10
        self.amount = amount
        self.room_pool = []
        
        
    async def fetch_room(self, amount: int = 1) -> List[Image]:
        if not self.room_pool:
            self.room_pool = await self.RecNet.rooms.hot(take=100)
        
        rooms = random.choices(self.room_pool)

        return rooms
            
    async def fetch_with_embeds(self) -> List[discord.Embed]:
        rooms = await self.fetch_room(self.amount)
        
        # If it times out
        if not rooms:
            return ["Something went wrong and I couldn't find a random room. Try again later!"]
        
        embeds = []
        for room in rooms:
            embeds.append(await fetch_room_embed(room))
            
        return embeds
            
    @discord.ui.button(label="Another!", style=discord.ButtonStyle.primary)
    async def again(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        embeds = await self.fetch_with_embeds()
        await interaction.response.edit_message(embeds=embeds, view=self)
        
        
    async def respond(self, interaction: discord.Interaction):
        embeds = await self.fetch_with_embeds()
        await interaction.response.send_message(embeds=embeds, view=self)
        

@slash_command(
    name="room",
    description="Lookup random rooms taken in Rec Room."
)
async def room(
    self, 
    ctx: discord.ApplicationContext
):
    view = RandomRoom(self.bot.RecNet)
    await view.respond(ctx.interaction)

    
    

        

        