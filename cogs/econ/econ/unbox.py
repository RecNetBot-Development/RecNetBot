import discord
import random
import json
from embeds import get_default_embed
from resources import get_emoji
from discord.commands import slash_command, Option
from economy import get_rarity_color, load_items, get_item
from enum import Enum

ITEMS = load_items()

class BoxTypes(Enum):
    LOW_TIER = 0
    HIGH_TIER = 1

class BoxOption(discord.ui.Button):
    def __init__(self, option: int):
        self.option = option
        item = ITEMS[self.option]
        name = item["name"]
 
        super().__init__(style=discord.ButtonStyle.primary, label=name, custom_id=str(self.option))

    async def callback(self, interaction: discord.Interaction):
        await self.view.callback(interaction, int(self.custom_id))


class BoxAgain(discord.ui.Button):
    def __init__(self, box_type: BoxTypes):
        self.box_type = box_type
        if self.box_type == BoxTypes.HIGH_TIER:
            label = "Open 3-4 Star Box"
        else:
            label = "Open 1-2 Star Box"
        super().__init__(style=discord.ButtonStyle.primary, label=label)

    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        await interaction.message.edit(view=self.view)

        view = BoxMenu(self.view.bot, self.box_type)
        ctx = await self.view.bot.get_application_context(interaction)
        await view.respond(ctx)


class BoxMenu(discord.ui.View):
    def __init__(self, bot, box_type: BoxTypes):
        super().__init__(
            timeout=600,
            disable_on_timeout=True
        )

        # Rewards
        self.box_type = box_type
        self.items = self.randomize_items(self.box_type)

        # Reward buttons
        for i in self.items:
            self.add_item(BoxOption(i["id"]))

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

        # Again button
        self.add_item(BoxAgain(self.box_type))

        # Get the chosen reward
        reward = get_item(item_id=item_id)

        em = get_default_embed()
        em.title = "Reward chosen!"
        em.description = f"**{reward['name']}** (x{amount})" \
                         f"\n{get_emoji('token')} {reward['tokens']:,}" \
                         f"\n{get_emoji('level') * reward['rarity']}"
        em.set_thumbnail(url=reward['img_url'])
        em.set_footer(text=f"{self.ctx.author.name}'s reward")
        
        # Reward rarity indicator
        em.color = get_rarity_color(reward["rarity"])

        await interaction.response.edit_message(embed=em, view=self)

    def claim_item(self, item_id: int):
        """ Add the item to the user's inventory """
        self.bot.ecm.add_item(self.ctx.author.id, item_id, 1)

    def randomize_items(self, box_type: BoxTypes):
        # Chooses items for the box
        item_pool = ITEMS.copy()

        # Filter the wanted items
        if box_type == BoxTypes.LOW_TIER:
            item_pool = list(filter(lambda item: item["rarity"] in (1, 2), item_pool))
        else:
            item_pool = list(filter(lambda item: item["rarity"] in (3, 4), item_pool))

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
            em.add_field(name=f"{i['emoji_icon']} {i['name']}", value=f"{get_emoji('token')} {i['tokens']:,}")

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
        

@slash_command(
    name="unbox",
    description="Unbox a reward box."
)
async def unbox(
    self, 
    ctx: discord.ApplicationContext,
    box: Option(str, name="box", description="What type of box would you like to open?", required=False, choices=[
        "1-2 Stars (Free)", 
        "3-4 Stars ()"
    ], default="1-2 Stars (Free)"),
):
    box_type = BoxTypes.LOW_TIER if box == "1-2 Stars (Free)" else BoxTypes.HIGH_TIER

    view = BoxMenu(self.bot, box_type)
    await view.respond(ctx)

    
    

        

        
