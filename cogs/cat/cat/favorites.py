import discord
import random
from discord.commands import slash_command
from embeds import get_default_embed, cat_embed
from cat_api import Cat, CatAPI
from resources import get_icon
from typing import List, Optional
from discord.ext.pages import PaginatorButton
from utils.paginator import RNBPage, RNBPaginator
from utils import load_config

config = load_config(is_production=True)

class FavButton(PaginatorButton):
    def __init__(self, cat_api: CatAPI):
        super().__init__(
            label="💔", 
            row=1,
            button_type="unfav",
            style=discord.ButtonStyle.grey
        )
        self.unfavorited_ids = []
        self.cat_api = cat_api

    async def callback(self, interaction: discord.Interaction):
        page = self.paginator.pages[
            self.paginator.current_page
        ]
        page_content = self.paginator.get_page_content(page)
        if not page_content.data:
            await interaction.response.send_message(content="Failed to unfavorite the cat... 😿", ephemeral=True)
            return

        cat: Cat = page_content.data
        if cat.favorite_id in self.unfavorited_ids:
            await interaction.response.send_message(content="You have already unfavorited the cat... 😿", ephemeral=True)
            return

        self.unfavorited_ids.append(cat.favorite_id)  # Disable unfavoriting it

        success = await self.cat_api.unfavorite_cat(cat.favorite_id)
        await interaction.response.send_message(
            content="Unfavorited the cat! 💔😿" if success else "Failed to unfavorite the cat... 😿", 
            ephemeral=True
        )

@slash_command(
    name="favorites",
    description="Browse through your favorite cats!",
    guild_ids=config.get("debug_guilds", [])
)
async def favorites(
    self, 
    ctx: discord.ApplicationContext
):
    await ctx.interaction.response.defer()

    cat_api = self.bot.CatAPI
    cats: List[Cat] = await cat_api.get_favorite_cats(ctx.author.id)
    if not cats:
        return await ctx.respond("You don't have any favorites! 😿")

    pages = list(map(lambda ele: RNBPage(ele, text=f"[🔗 Image URL 🐈]({ele.img_url})", data=ele), cats))
    paginator = RNBPaginator(pages=pages, trigger_on_display=True, show_indicator=False, author_check=True)
    paginator.add_button(FavButton(cat_api))
    await paginator.respond(ctx.interaction)

    