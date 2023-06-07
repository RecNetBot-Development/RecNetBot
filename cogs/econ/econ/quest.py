import discord
import random
import json
from embeds import get_default_embed
from resources import get_emoji
from discord.commands import slash_command
from utils import unix_timestamp
from economy import get_rarity_color, load_quests

QUESTS = load_quests()

class QuestSelection(discord.ui.Select):
    def __init__(self, selected_quest):
        # Add quests to the list
        options = []
        for quest in QUESTS:
            option = discord.SelectOption(
                label=quest.get("name"),
                description=quest["description"],
                default = True if quest == selected_quest else False
            )
            options.append(option)

        super().__init__(
            placeholder="Choose your Quest",
            min_values=1,
            max_values=1,
            options=options,
            row=0
        )

    async def callback(self, interaction: discord.Interaction):
        # Make sure it's the author using the component
        if interaction.user.id != interaction.message.interaction.user.id:
            return await interaction.response.send_message("You're not authorized!", ephemeral=True)
        
        # Find the quest
        for i in QUESTS:
            if self.values[0] == i["name"]:
                quest = i
                break

        # Make embed
        self.view.set_quest(quest)

        ctx = await self.view.bot.get_application_context(interaction)
        await self.view.edit(ctx)


class QuestStart(discord.ui.Button):
    def __init__(self, disabled: bool = False):
        super().__init__(
            label="Start" if not disabled else "Under Construction",
            style=discord.ButtonStyle.green if not disabled else discord.ButtonStyle.danger,
            disabled=disabled
        )

    async def callback(self, interaction: discord.Interaction):
        # Make sure it's the author using the component
        if interaction.user.id != interaction.message.interaction.user.id:
            return await interaction.response.send_message("You're not authorized!", ephemeral=True)
        
        ctx = await self.view.bot.get_application_context(interaction)
        await self.view.start(ctx)
        


class QuestMenu(discord.ui.View):
    def __init__(self, bot):
        # Selected
        self.quest = None
        self.embed = None
        self.set_quest(QUESTS[0])

        super().__init__(
            timeout=600,
            disable_on_timeout=True,
        )

        # Bot
        self.bot = bot

        # Context
        self.ctx = None
        
    def set_quest(self, quest):
        """
        Creates a showcase embed for the quest
        """
        em = get_default_embed()
        em.title = quest["name"]
        em.description = quest["description"]
        em.set_image(url=quest["image_url"])

        self.embed = em
        self.quest = quest

    async def start(self, ctx: discord.ApplicationContext):
        ...

    async def respond(self, ctx: discord.ApplicationContext):
        await self.handle_message(ctx, edit=False)

    async def edit(self, ctx: discord.ApplicationContext):
        await self.handle_message(ctx, edit=True)

    async def handle_message(self, ctx: discord.ApplicationContext, edit: bool = False):
        # Reset the default
        self.clear_items()
        self.add_item(QuestSelection(self.quest))
        self.add_item(QuestStart(disabled=True))

        self.ctx = ctx
        if edit:
            await ctx.interaction.response.edit_message(embed=self.embed, view=self)
        else:
            await ctx.interaction.response.send_message(embed=self.embed, view=self)


@slash_command(
    name="quest",
    description="Embark on a RecNetBot Original quest!"
)
async def quest(
    self, 
    ctx: discord.ApplicationContext
):
    view = QuestMenu(self.bot)
    await view.respond(ctx)
        


