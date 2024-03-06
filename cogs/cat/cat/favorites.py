import discord
import random
from discord.commands import slash_command
from embeds import get_default_embed, cat_embed
from cat_api import Cat, CatAPI
from resources import get_icon
from typing import List, Optional
from utils.paginator import RNBPage, RNBPaginator

@slash_command(
    name="favorites",
    description="Browse through your favorite cats!"
)
async def favorites(
    self, 
    ctx: discord.ApplicationContext
):
    await ctx.interaction.response.defer()

    cats: List[Cat] = await self.bot.CatAPI.get_favorite_cats(ctx.author.id)
    if not cats:
        return await ctx.respond("You don't have any favorites! 😿")

    pages = list(map(lambda ele: RNBPage(ele), cats))
    paginator = RNBPaginator(pages=pages, trigger_on_display=True, show_indicator=False, author_check=True)
    await paginator.respond(ctx.interaction)

    