import discord
import random
import json
from embeds import get_default_embed
from resources import get_emoji
from discord.commands import slash_command
from economy import get_rarity_color


with open("economy/items.json") as items:
    ITEMS: list = json.load(items)


class BoxOption(discord.ui.Button):
    def __init__(self, option: int):
        self.option = option
        item = ITEMS[self.option]
        name = item["name"]
 
        super().__init__(style=discord.ButtonStyle.primary, label=name, custom_id=str(self.option))

    async def callback(self, interaction: discord.Interaction):
        await self.view.callback(interaction, int(self.custom_id))


class BoxAgain(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.primary, label="Another!")

    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        await interaction.message.edit(view=self.view)

        view = BoxMenu(self.view.bot)
        ctx = await self.view.bot.get_application_context(interaction)
        await view.respond(ctx)


class BoxMenu(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        # Component timeout
        self.timeout = 600
        self.disable_on_timeout = True

        # Rewards
        self.items = self.randomize_items()

        # Reward buttons
        for i in self.items:
            self.add_item(BoxOption(i["id"]))

        # Bot
        self.bot = bot

        # Context
        self.ctx = None
        
    async def callback(self, interaction: discord.Interaction, option: int):
        # Box option button callback

        # Clear reward options
        self.clear_items()

        # Again button
        self.add_item(BoxAgain())

        # Get the chosen reward
        reward = ITEMS[option]

        em = get_default_embed()
        em.title = "Reward chosen!"
        em.description = f"**{reward['name']}**" \
                         f"\n{get_emoji('token')} {reward['tokens']:,}" \
                         f"\n{get_emoji('level') * reward['rarity']}"
        em.set_thumbnail(url=reward['img_url'])
        em.set_footer(text=f"{self.ctx.author.name}'s reward")
        
        # Reward rarity indicator
        em.color = get_rarity_color(reward["rarity"])

        await interaction.response.edit_message(embed=em, view=self)

    def randomize_items(self):
        # Chooses items for the box
        item_pool = ITEMS.copy()
        chosen_items = []

        for i in range(3):
            item = random.choice(item_pool)
            item_pool.remove(item)
            item["id"] = ITEMS.index(item)
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
    ctx: discord.ApplicationContext
):
    view = BoxMenu(self.bot)
    await view.respond(ctx)

    
    

        

        
