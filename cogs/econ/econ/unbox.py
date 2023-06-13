import discord
import random
import json
from embeds import get_default_embed
from resources import get_emoji
from discord.commands import slash_command, Option
from economy import get_rarity_color, load_items, get_item, Item, load_boxes, Box, get_box
from enum import Enum
from typing import List

ITEMS = load_items()
BOXES = load_boxes()

class BoxOption(discord.ui.Button):
    def __init__(self, option: int):
        self.option = option
        item = get_item(item_id=self.option)
        name = item.name
 
        super().__init__(style=discord.ButtonStyle.primary, label=name, custom_id=str(self.option))

    async def callback(self, interaction: discord.Interaction):
        await self.view.callback(interaction, int(self.custom_id))


class BoxAgain(discord.ui.Button):
    def __init__(self, box: Box):
        super().__init__(style=discord.ButtonStyle.primary)

        self.box = box
        self.label = f"Open {self.box.name}"

    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        await interaction.message.edit(view=self.view)

        view = BoxMenu(self.view.bot, self.box)
        ctx = await self.view.bot.get_application_context(interaction)
        await view.respond(ctx)


class InventoryButton(discord.ui.Button):
    def __init__(self, inv_cmd):
        super().__init__(style=discord.ButtonStyle.gray, label="Inventory")
        self.inv_cmd = inv_cmd

    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        await interaction.message.edit(view=self.view)

        # Run the inv command
        ctx = await self.view.bot.get_application_context(interaction)
        await self.inv_cmd(ctx)


class SellButton(discord.ui.Button):
    def __init__(self, item: Item, ecm):
        super().__init__(style=discord.ButtonStyle.green)
        self.ecm = ecm
        self.item = item

        # Button label
        self.label = f"Sell for {self.item.tokens}"

    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        await interaction.message.edit(view=self.view)

        # Remove item from inv
        self.ecm.add_item(interaction.user.id, self.item.id, -1)
        # Add tokens
        self.ecm.add_tokens(interaction.user.id, self.item.tokens)

        await interaction.response.send_message(f"Sold {self.item.emoji_icon}** {self.item.name}** for {get_emoji('token')}**{self.item.tokens}**!")


class BoxMenu(discord.ui.View):
    def __init__(self, bot, box: Box, inv_cmd = None):
        super().__init__(
            timeout=600,
            disable_on_timeout=True
        )

        # Inventory command
        self.inv_cmd = inv_cmd

        # Rewards
        self.box = box
        self.items = self.randomize_items(self.box)

        # Reward buttons
        for i in self.items:
            self.add_item(BoxOption(i.id))

        # Bot
        self.bot = bot

        # Context
        self.ctx = None
        
    async def callback(self, interaction: discord.Interaction, item_id: int):
        # Box option button callback

        # Reward the user
        self.claim_item(item_id)

        # Fetch how many user has
        amount = self.bot.ecm.get_item_amount(self.ctx.author.id, item_id)

        # Clear reward options
        self.clear_items()

        # Get the chosen reward
        item = get_item(item_id=item_id)

        # Again button
        self.add_item(BoxAgain(self.box))

        # Sell button
        self.add_item(SellButton(item, self.bot.ecm))

        # Inventory button
        if self.inv_cmd:
            self.add_item(InventoryButton(self.inv_cmd))

        # Reward embed
        em = get_default_embed()
        em.title = "Reward chosen!"
        em.description = f"**{item.name}** (x{amount})" \
                         f"\n{get_emoji('token')} {item.tokens:,}" \
                         f"\n{get_emoji('level') * item.rarity}"
        em.set_thumbnail(url=item.img_url)
        em.set_footer(text=f"{self.ctx.author.name}'s reward")
        
        # Reward rarity indicator
        em.color = get_rarity_color(item.rarity)

        await interaction.response.edit_message(embed=em, view=self)

    def claim_item(self, item_id: int):
        """ Add the item to the user's inventory """
        self.bot.ecm.add_item(self.ctx.author.id, item_id, 1)

    def randomize_items(self, box: Box) -> List[Item]:
        # Chooses items for the box
        all_items = ITEMS.copy()

        # Filter the wanted items
        if box.categories:
            item_pool: List[Item] = list(filter(lambda item: item.category in box.categories, all_items))

        if box.rarities:
            item_pool: List[Item] = list(filter(lambda item: item.rarity in box.rarities, all_items))

        if box.items:
            item_pool: List[Item] = list(filter(lambda item: item in box.items, all_items))

        # Randomly choose from the item pool
        chosen_items = []
        for i in range(3):
            item = random.choice(item_pool)
            item_pool.remove(item)
            chosen_items.append(item)

        return chosen_items

    def create_menu(self):
        # Present the options
        em = get_default_embed()
        em.title = "Choose your reward"
        em.set_footer(text=f"{self.ctx.author.name}'s box")

        for i in self.items:
            em.add_field(name=f"{i.emoji_icon} {i.name}", value=f"{get_emoji('token')} {i.tokens:,} {get_emoji('level') * i.rarity}")

        return em

    async def respond(self, ctx: discord.ApplicationContext):
        await self.handle_message(ctx, edit=False)

    async def edit(self, ctx: discord.ApplicationContext):
        await self.handle_message(ctx, edit=True)

    async def handle_message(self, ctx: discord.ApplicationContext, edit: bool = False):
        self.ctx = ctx

        # Create reward menu
        em = self.create_menu()

        if edit:
            await ctx.interaction.response.edit_message(embed=em, view=self)
        else:
            await ctx.interaction.response.send_message(embed=em, view=self)
        
async def get_boxes(ctx: discord.AutocompleteContext):
    """Returns a list of items that begin with the characters entered so far."""
    return [box.name for box in BOXES if box.name.lower().startswith(ctx.value.lower())]

@slash_command(
    name="unbox",
    description="Unbox a reward box."
)
async def unbox(
    self, 
    ctx: discord.ApplicationContext,
    box: Option(str, name="box", description="What type of box would you like to open?", autocomplete=get_boxes)
):
    # Get the box
    box = get_box(box_name=box)
    if not box:
        return await ctx.respond("Box doesn't exist!")

    # Get inventory command
    group = discord.utils.get(self.__cog_commands__, name='econ')
    inv_cmd = discord.utils.get(group.walk_commands(), name='inventory')

    view = BoxMenu(self.bot, box, inv_cmd)
    await view.respond(ctx)

    
    

        

        
