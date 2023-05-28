import discord
import recnetpy
import random
from utils import img_url
from typing import List
from recnetpy.dataclasses.image import Image
from discord.commands import slash_command, Option

class RandomImage(discord.ui.View):
    def __init__(self, rec_net: recnetpy.Client, amount: int = 1):
        super().__init__()
        self.RecNet = rec_net
        self.timeout = 600
        self.disable_on_timeout = True
        self.amount = amount
        self.image_pool = []
        
    async def fetch_image(self, amount: int = 1) -> List[Image]:
        if not self.image_pool:
            self.image_pool = await self.RecNet.images.front_page(500)
        
        images = random.choices(self.image_pool, k=self.amount)

        return images
            
    async def fetch_with_links(self) -> List[str]:
        images = await self.fetch_image(self.amount)
        
        # If it times out
        if not images:
            return ["Something went wrong and I couldn't find a random image. Try again later!"]
        
        links = list(map(lambda image: img_url(image.image_name), images))
            
        return links
            
    @discord.ui.button(label="Another!", style=discord.ButtonStyle.primary)
    async def again(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        # Make sure it's the author using the component
        if interaction.user.id != interaction.message.interaction.user.id:
            return await interaction.response.send_message("You're not authorized!", ephemeral=True)
        
        links = await self.fetch_with_links()
        await interaction.response.edit_message(content="\n".join(links), view=self)
        
        
    async def respond(self, interaction: discord.Interaction):
        links = await self.fetch_with_links()
        await interaction.response.send_message(content="\n".join(links), view=self)
        

@slash_command(
    name="image",
    description="Lookup random images taken in Rec Room without context."
)
async def image(
    self, 
    ctx: discord.ApplicationContext,
    amount: Option(int, "How many you'd like", min_value=1, max_value=5, default=1)
):
    view = RandomImage(self.bot.RecNet, amount=amount)
    await view.respond(ctx.interaction)

    
    

        

        
