import discord
import random
import json
from embeds import get_default_embed
from resources import get_emoji
from discord.commands import slash_command
from utils import unix_timestamp
from economy import get_rarity_color, load_items

ITEMS = load_items()

@slash_command(
    name="profile",
    description="View your economy profile"
)
async def profile(
    self, 
    ctx: discord.ApplicationContext
):
    profile = self.bot.ecm.get_profile(ctx.author.id)
    if not profile:
        self.bot.ecm.create_profile(ctx.author.id)
        profile = self.bot.ecm.get_profile(ctx.author.id)

    inv = self.bot.ecm.get_inventory(ctx.author.id)
    item_count = sum([i['amount'] for i in inv])

    em = get_default_embed()
    em.title = f"{ctx.author.name}'s profile"
    em.description = f"{get_emoji('token')} {profile.tokens}" \
                     f"\n{item_count} items" \
                     f"\nJoin Date: {unix_timestamp(profile.join_date, 'D')}"
    em.set_thumbnail(url=ctx.author.avatar.url)

    await ctx.respond(embed=em)
        


