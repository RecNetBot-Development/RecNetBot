import discord
import random
import json
from embeds import get_default_embed
from resources import get_emoji
from discord.commands import slash_command
from economy import get_rarity_color, load_items

ITEMS = load_items()

@slash_command(
    name="inventory",
    description="Inspect your inventory"
)
async def inventory(
    self, 
    ctx: discord.ApplicationContext
):
    em = get_default_embed()
    em.title = f"{ctx.author.name}'s inventory"

    inv = self.bot.ecm.get_inventory(ctx.author.id)
    net_worth = 0  # How much are all items worth

    # Let's sort items based on rarity
    rarity_inv = {
        5: [],
        4: [],
        3: [],
        2: [],
        1: [],
        0: []
    }  
    for i in inv:
        rarity_inv[i['item']['rarity']].append(i)
        net_worth += i['item']['tokens']

    # Let's sort each item by amount and make embed
    for rarity, inv in rarity_inv.items():
        # Ignore if no items in rarity
        if not inv: continue

        # Sort by amount
        inv.sort(key=lambda item: item["amount"], reverse=True)

        # Item list
        items = []
        for item in inv:
            # Don't list items the user doesn't own
            if item['amount'] <= 0: continue

            items.append(
                f"{item['item']['emoji_icon']} {item['item']['name']} (x{item['amount']})"
            )

        # Don't make a category for items you don't own
        if not items: continue

        # Add to embed
        em.add_field(
            name=f"{rarity} Star{'s' if rarity != 1 else ''}",
            value="\n".join(items),
            inline=False
        )

    # Additional information
    em.add_field(
        name="Information",
        value=f"{get_emoji('token')}{net_worth:,} • Net Worth",
        inline=False
    )

    await ctx.respond(embed=em)
        


