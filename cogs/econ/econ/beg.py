import discord
import random
import json
import math
from datetime import datetime
from embeds import get_default_embed
from resources import get_emoji
from discord.commands import slash_command
from discord.ext import commands
from economy import load_begs, load_items

BEGS = load_begs()
ITEMS = load_items()

class BegMenu(discord.ui.View):
    def __init__(self, bot):
        super().__init__(
            timeout=600,
            disable_on_timeout=True
        )
        self.bot = bot

        # Context
        self.ctx = None

    @discord.ui.button(label="Hop instances")
    async def repeat_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        ctx = await self.bot.get_application_context(interaction)

        await self.edit(ctx)

    async def respond(self, ctx: discord.ApplicationContext):
        await self.handle_message(ctx, edit=False)

    async def edit(self, ctx: discord.ApplicationContext):
        await self.handle_message(ctx, edit=True)

    async def handle_message(self, ctx: discord.ApplicationContext, edit: bool = False):
        self.ctx = ctx

        # Gamble
        chance = random.randint(0, 100)

        if chance <= 5:
            pool = BEGS["penalty"]
        elif chance <= 30:
            pool = BEGS["uncommon"]
        else:
            pool = BEGS["common"]

        reward = random.choice(pool)

        response = reward["response"]
        # Reward
        if reward["item_id"]:
            # Add to inventory
            self.bot.ecm.add_item(ctx.author.id, reward["item_id"], 1)

            item = ITEMS[reward["item_id"]]
            response += F"\n\n*You got* {item['emoji_icon']} **{item['name']}**"
        elif reward["tokens"]:
            # Add to balance
            self.bot.ecm.add_tokens(ctx.author.id, reward["tokens"])

            response += F"\n\n*You received* {get_emoji('token')}**{reward['tokens']}**"

        elif reward["penalty"]:
            # Set penalty
            self.bot.ecm.set_penalty(ctx.author.id, reward['penalty'])

            response += f"\n\n*You can't beg for the next {reward['penalty']} minutes!*"
            self.disable_all_items()

        else:
            response += f"\n\n*You didn't receive any gifts.*"
            
        if edit:
            await ctx.interaction.response.edit_message(content=response, view=self)
        else:
            await ctx.interaction.response.send_message(content=response, view=self)

@slash_command(
    name="beg",
    description="Beg in a Rec Center for goods. Be careful to not be votekicked!"
)
async def beg(
    self, 
    ctx: discord.ApplicationContext
):
    # Check for begging penalties
    penalty = self.bot.ecm.get_penalty(ctx.author.id)
    now_timestamp = int(datetime.now().timestamp())
    if penalty > now_timestamp:
        seconds = penalty - now_timestamp
        await ctx.respond(content=
            f"You were punished for begging. You're able to beg again in {math.ceil(seconds / 60)} minute{'s.' if seconds // 60 != 1 else '.'}"
        )
        return

    view = BegMenu(self.bot)
    await view.respond(ctx)
        


