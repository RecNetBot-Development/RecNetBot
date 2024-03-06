import discord
import random
from discord.commands import slash_command
from embeds import get_default_embed, cat_embed
from cat_api import Cat, CatAPI
from resources import get_icon
from typing import List, Optional

CAT_EMOJIS = ["🐈", "😿", "😾", "🐱", "🙀", "😺", "😽", "😼", "😸", "😹", "😻", "🐅"]

class CatView(discord.ui.View):
    def __init__(self, cat_client: CatAPI):
        super().__init__()
        self.timeout = 600
        self.disable_on_timeout = True
        self.CatAPI: CatAPI = cat_client
        self.current_cat: Optional[Cat] = None
        self.current_embed = Optional[discord.Embed]

    @discord.ui.button(label="More!", custom_id="more_btn", style=discord.ButtonStyle.green)
    async def more(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.defer()

        # Make sure it's the author using the component
        if interaction.user.id != interaction.message.interaction.user.id:
            return await interaction.followup.send("You're not authorized!", ephemeral=True)
        
        # Respond using og response function
        await self.respond(interaction)

    @discord.ui.button(label="❤️", custom_id="fav_btn", style=discord.ButtonStyle.gray)
    async def favorite(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.defer()

        # Make sure it's the author using the component
        if interaction.user.id != interaction.message.interaction.user.id:
            return await interaction.followup.send("You're not authorized!", ephemeral=True)
        
        # Make sure to not let user spam favs
        if button.style == discord.ButtonStyle.red:
            return await interaction.followup.send("You have already favorited this cat! 😻", ephemeral=True)

        await self.CatAPI.favorite_cat(self.current_cat.id, interaction.user.id)

        # Respond using og response function
        self.refresh_components(fav_activate=True)
        await interaction.edit_original_response(embed=self.current_embed, view=self)
        await interaction.followup.send("Cat favorited! 😻", ephemeral=True)

    async def respond(self, interaction: discord.Interaction):
        em = get_default_embed()

        cats: List[Cat] = await self.CatAPI.get_cats()

        # Check if any cats were found
        if not cats:
            em.title = "Uh oh!"
            em.description = "Looks like the cats have escaped the shelter. Try again later!"
            em.set_thumbnail(url=get_icon('rectnet'))

            return await interaction.edit_original_response(embed=em)
        
        # Only one cat!
        cat = cats[0]
        self.current_cat = cat

        # Distribute found cat
        em = cat_embed(cat)

        self.current_embed = em
        self.refresh_components()

        await interaction.edit_original_response(embed=em, view=self)

    def refresh_components(self, fav_activate: bool = False) -> None:
        """Refreshes the view components
        """
        # More button
        more_btn = self.get_item(custom_id="more_btn")
        more_btn.label = f"More! {random.choice(CAT_EMOJIS)}"

        # Fav button
        fav_btn = self.get_item(custom_id="fav_btn")

        if fav_activate:
            fav_btn.label = "💗"
            fav_btn.style = discord.ButtonStyle.red 
        else:
            fav_btn.label = "❤️"
            fav_btn.style = discord.ButtonStyle.grey

        # Link button
        link_btn = discord.ui.Button(
            label="Image",
            url=self.current_cat.img_url,
            style=discord.ButtonStyle.link
        )

        # Get rid of current components
        self.clear_items()

        # Update!!
        components = [more_btn, fav_btn, link_btn]
        for i in components:
            self.add_item(i)

@slash_command(
    name="pls",
    description="Find cute pictures of our feline buddies!"
)
async def pls(
    self, 
    ctx: discord.ApplicationContext
):
    await ctx.interaction.response.defer()

    view = CatView(cat_client=self.bot.CatAPI)
    await view.respond(ctx.interaction)

    