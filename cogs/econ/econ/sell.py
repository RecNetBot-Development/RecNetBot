import discord
import random
import json
from embeds import get_default_embed
from resources import get_emoji
from discord.commands import slash_command, Option
from economy import get_rarity_color, load_items, get_item

ITEMS = load_items()

# For prompting the user whether or not to sell the item
class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Sell", style=discord.ButtonStyle.green)
    async def confirm_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.defer(invisible=True)
        self.value = True
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.gray)
    async def cancel_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.defer(invisible=True)
        self.value = False
        self.stop()

async def get_items(ctx: discord.AutocompleteContext):
    """Returns a list of items that begin with the characters entered so far."""
    return [item['name'] for item in ITEMS if item["name"].lower().startswith(ctx.value.lower())]

@slash_command(
    name="sell",
    description="Sell consumables"
)
async def sell(
    self, 
    ctx: discord.ApplicationContext,
    _item: Option(str, name="item", description="Which item would you like to sell?", autocomplete=get_items),
    amount: Option(int, name="amount", description="How many would you like to sell?", min_value=1)
):
    item = get_item(item_name=_item)
    if not item:
        return await ctx.respond("Item doesn't exist!")

    # How many does the user have
    owned = self.bot.ecm.get_item_amount(ctx.author.id, item["id"])
    if owned < amount:
        return await ctx.respond(f"You can't sell (x{amount}) {item['emoji_icon']} **{item['name']}** because you only have {owned}!")

    # How much money
    tokens = item['tokens'] * amount

    # Confirm selling
    view = Confirm()
    
    # Edit to sell phase
    sell_prompt = f"You are about to sell (x{amount}) {item['emoji_icon']} **{item['name']}** for {get_emoji('token')}**{tokens}**."
    await ctx.respond(
        content=sell_prompt,
        view=view
    )
    
    await view.wait()
    if not view.value:
        return await ctx.interaction.edit_original_response(content=f"~~{sell_prompt}~~", embeds=[], view=None)
    
    self.bot.ecm.add_item(ctx.author.id, item["id"], -amount)
    self.bot.ecm.add_tokens(ctx.author.id, tokens)

    await ctx.interaction.edit_original_response(content=
        f"Sold (x{amount}) {item['emoji_icon']} **{item['name']}** for {get_emoji('token')}**{tokens}**!",
        view=None    
    )
        


