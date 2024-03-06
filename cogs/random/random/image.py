import discord
import recnetpy
import random
from utils import img_url
from utils.paginator import RNBPaginator, RNBPage
from typing import List
from recnetpy.dataclasses.image import Image
from discord.commands import slash_command, Option

#MAX_IMAGE_ID = 570000000
MAX_OLD_IMAGE_ID = 4_000_000
MAX_NEW_IMAGE_ID = 570_000_000

class RandomImage(discord.ui.View):
    def __init__(self, rec_net: recnetpy.Client, amount: int = 1):
        super().__init__()
        self.RecNet = rec_net
        self.timeout = 600
        self.disable_on_timeout = True
        self.amount = amount
        self.current_images = []

        # If set to true, id range is 1 -> MAX_OLD_IMAGE_ID
        # If set to false, id range is MAX_OLD_IMAGE_ID -> MAX_NEW_IMAGE_ID
        self.older = False

        # Different caches
        self.image_cache = {
            "new": [],
            "old": []
        }
        
    async def get_images(self) -> List[Image]:
        min_id = 1 if self.older else MAX_OLD_IMAGE_ID
        max_id = MAX_OLD_IMAGE_ID if self.older else MAX_NEW_IMAGE_ID
        image_pool = "old" if self.older else "new"

        # Fetch images randomly until amount is met
        while len(self.image_cache[image_pool]) < self.amount:
            self.image_cache[image_pool] += await self.RecNet.images.fetch_many(random.sample(range(min_id, max_id), 100))
        
        # Check if random images need to be drawn due to low amount
        if len(self.image_cache[image_pool]) <= self.amount:
            images = self.image_cache[image_pool]
            self.image_cache[image_pool] = []
        else:
            # Choose random images from image pool
            images = []
            for i in range(self.amount):
                images.append(random.choice(self.image_cache[image_pool]))
                self.image_cache[image_pool].remove(images[-1])

        return images
            

    @discord.ui.button(label="Older!", style=discord.ButtonStyle.green)
    async def more_old(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.defer()

        # Make sure it's the author using the component
        if interaction.user.id != interaction.message.interaction.user.id:
            return await interaction.followup.send("You're not authorized!", ephemeral=True)
        
        # Set to fetch older pics
        self.older = True

        # Respond using og response function
        await self.respond(interaction)


    @discord.ui.button(label="Newer!", style=discord.ButtonStyle.green)
    async def more_new(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.defer()

        # Make sure it's the author using the component
        if interaction.user.id != interaction.message.interaction.user.id:
            return await interaction.followup.send("You're not authorized!", ephemeral=True)
        
        # Set to fetch newer pics
        self.older = False

        # Respond using og response function
        await self.respond(interaction)


    @discord.ui.button(label="Browse", style=discord.ButtonStyle.primary)
    async def browse(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.defer()
        
        pages = list(map(lambda ele: RNBPage(ele), self.current_images))
        paginator = RNBPaginator(pages=pages, trigger_on_display=True, show_indicator=False, author_check=False)
        await paginator.respond(interaction, ephemeral=True)
        

    async def respond(self, interaction: discord.Interaction):
        # Respond to interaction with random images
        images = await self.get_images()
        self.current_images = images

        # Get img.rec.net links of image objects
        links = list(map(lambda image: img_url(image.image_name), images))

        await interaction.edit_original_response(content="\n".join(links), view=self)
        

@slash_command(
    name="image",
    description="Find random images from the depths of RecNet."
)
async def image(
    self, 
    ctx: discord.ApplicationContext
):
    await ctx.interaction.response.defer()

    view = RandomImage(self.bot.RecNet, amount=3)
    await view.respond(ctx.interaction)

    
    

        

        
