import discord
import recnetpy
import random
import bisect
from embeds import get_default_embed
from utils import img_url, unix_timestamp, post_url
from utils.paginator import RNBPaginator, RNBPage
from typing import List
from recnetpy.dataclasses.image import Image
from discord.commands import slash_command, Option
from datetime import datetime
from resources import get_emoji, get_icon
from enum import Enum
from utils import load_config

config = load_config(is_production=True)

#MAX_IMAGE_ID = 570000000
MAX_OLD_IMAGE_ID = 4_000_000
#MAX_NEW_IMAGE_ID = 570_000_000
MAX_NEW_IMAGE_ID = 300_000_000

class YearButton(discord.ui.Button):
    def __init__(self, year: int, answer_showcase: bool = None):
        if answer_showcase is not None:
            super().__init__(style=discord.ButtonStyle.green if answer_showcase is True else discord.ButtonStyle.red, label=str(year), disabled=True)
        else:
            super().__init__(style=discord.ButtonStyle.grey, label=str(year))
        self.year = year

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(invisible=True)

        assert self.view is not None
        view: ImageQuiz = self.view
        
        await view.answer(interaction, self.year)

class HintButton(discord.ui.Button):
    def __init__(self, enabled: bool = True):
        super().__init__(style=discord.ButtonStyle.green, label="Hint", disabled=not enabled)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(invisible=True)

        assert self.view is not None
        view: ImageQuiz = self.view

        # Disable self
        self.disabled = True
        
        await view.hint(interaction)

class NextButton(discord.ui.Button):
    def __init__(self, correct: bool = True):
        super().__init__(
            style=discord.ButtonStyle.green if correct else discord.ButtonStyle.red, 
            label="Next!"
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(invisible=True)

        assert self.view is not None
        view: ImageQuiz = self.view
        
        await view.respond(interaction)

class LinkButton(discord.ui.Button):
    def __init__(self, link: str):
        super().__init__(
            style=discord.ButtonStyle.link,
            label="RecNet",
            url=link
        )

class ImageQuiz(discord.ui.View):
    def __init__(self, rec_net: recnetpy.Client):
        super().__init__()
        self.RecNet = rec_net
        self.timeout = 300
        self.current_image: Image = None
        self.amount = 1

        # Modifier
        self.modifier = None
        self.modifier_info = ""

        # Log the answers
        self.answers = {
            "correct": 0,
            "incorrect": 0
        }
        self.best_streak = 0
        self.streak = 0
        self.streak_type = ""
        self.correct_answer = 0

        # If set to true, id range is 1 -> MAX_OLD_IMAGE_ID
        # If set to false, id range is MAX_OLD_IMAGE_ID -> MAX_NEW_IMAGE_ID
        self.older = True

        # Different caches
        self.image_cache = {
            "new": [],
            "old": []
        }
        
    async def get_image(self) -> Image:
        min_id = 1 if self.older else MAX_OLD_IMAGE_ID
        max_id = MAX_OLD_IMAGE_ID if self.older else MAX_NEW_IMAGE_ID
        image_pool = "old" if self.older else "new"

        # Fetch images randomly until amount is met
        while len(self.image_cache[image_pool]) < self.amount:
            self.image_cache[image_pool] += await self.RecNet.images.fetch_many(random.sample(range(min_id, max_id), 100))
        
        # Check if random images need to be drawn due to low amount
        if len(self.image_cache[image_pool]) <= self.amount:
            image = self.image_cache[image_pool]
            self.image_cache[image_pool] = []
        else:
            # Choose random image from image pool
            image = random.choice(self.image_cache[image_pool])
            self.image_cache[image_pool].remove(image)

        return image
        
    async def answer(self, interaction: discord.Interaction, year: int):
        # Check if the answer was correct
        correct = year == self.correct_answer
        correct_key = "correct" if correct else "incorrect"
        self.answers[correct_key] += 1

        # Update streak accordingly
        if self.streak_type == correct_key:
            self.streak += 1
            if self.streak_type == "correct" and self.streak > self.best_streak:
                self.best_streak = self.streak
        else:
            self.streak = 1
            self.streak_type = correct_key

        # Update components
        self.clear_items()
        self.add_item(NextButton(correct))
        self.add_item(YearButton(year, answer_showcase=correct))
        self.add_item(LinkButton(post_url(self.current_image.id)))

        # Response
        self.current_embed.set_author(
            name='✅ Correct!' if correct else '❌ Incorrect.'
        )
        self.current_embed.description = f"The picture was taken {unix_timestamp(self.current_image.created_at, 'D')}."
        self.current_embed.set_footer(text=f"✅ {self.answers['correct']} / {self.answers['incorrect']} ❌")
        self.current_embed.color = discord.Color.green() if correct else discord.Color.red()
        self.update_embed_score_footer()
        await interaction.edit_original_response(embed=self.current_embed, view=self)


    async def hint(self, interaction: discord.Interaction):
        # Come up with random hints
        hints = []

        # Room hint
        if self.current_image.room_id:
            room = await self.current_image.get_room()
            if room:
                hints.append(f"The room was created on {unix_timestamp(room.created_at, 'D')}.")

        # User join date hint
        account = await self.current_image.get_player()
        if account:
            hints.append(f"The player made their account on {unix_timestamp(account.created_at, 'D')}.")

        # None were found?
        if not hints:
            await interaction.respond("No hints available this time!", ephemeral=True)
            return

        # Share the hint
        self.current_embed.add_field(name=f"{get_emoji('light')} Hint", value=random.choice(hints))
        await interaction.edit_original_response(embed=self.current_embed, view=self)
    

    def delete_rand_items(self, items: list, amount: int):
        to_delete = set(random.sample(range(len(items)), amount))
        return [x for i, x in enumerate(items) if not i in to_delete]

    def update_embed_score_footer(self):
        footer = f"✅ {self.answers['correct']} / {self.answers['incorrect']} ❌"

        if self.streak > 1:
            emoji = "🔥" if self.streak_type == "correct" else "💩"
            footer += f" — {emoji} {self.streak}"

        self.current_embed.set_footer(text=footer)

    async def respond(self, interaction: discord.Interaction):
        # Chance
        self.older = random.choice([True, False])

        # Find a random image
        image = await self.get_image()
        self.current_image = image
        self.correct_answer = datetime.fromtimestamp(self.current_image.created_at).year

        # Year buttons
        self.clear_items()
        buttons = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

        # Random modifier
        self.modifier = random.choice([None, "delete_half", "50/50"])
        match self.modifier:
            case "delete_half":
                # Half the buttons gone!
                self.modifier_info = "Half the answers are gone."
                buttons = self.delete_rand_items(buttons, int(len(buttons)/2))

                # Make sure the correct answer is included
                if self.correct_answer not in buttons:
                    buttons = self.delete_rand_items(buttons, 1)
                    bisect.insort(buttons, self.correct_answer) 
            case "50/50":
                # Answer is 50/50
                self.modifier_info = "50/50"
                buttons = [self.correct_answer]
                bisect.insort(buttons, self.correct_answer + 1 if self.correct_answer != 2024 else self.correct_answer - 1) 
            case _:
                # No modifier
                self.modifier = None

        # Add all the year buttons
        for i in buttons:
            self.add_item(YearButton(i))

        # Add a hint button if there's no modifiers
        if not self.modifier: self.add_item(HintButton())
        
        #if self.streak >= 2 and self.streak_type == "incorrect":
        #    self.add_item(HintButton())

        # Form an embed
        em = get_default_embed()
        em.set_author(name="Guess which year this picture was taken!")
        em.set_image(url=img_url(image.image_name))
        if self.modifier: em.description = f"**Modifier:** {self.modifier_info}"
        self.current_embed = em

        self.update_embed_score_footer()
        await interaction.edit_original_response(embed=self.current_embed, view=self)

    async def on_timeout(self):
        self.disable_all_items()

        if not self._message or self._message.flags.ephemeral:
            message = self.parent
        else:
            message = self.message

        if message:
            correct = self.answers["correct"]
            incorrect = self.answers["incorrect"]
            stats = [
                f"Total Guesses: `{correct + incorrect}`",
                f"Best Streak: `{self.best_streak}`",
                f"✅ `{correct}` / `{incorrect}` ❌"
            ]
            em = get_default_embed()
            em.title = "Image Quiz Results"
            em.description = "\n".join(stats)
            em.set_author(name="Timed out!")
            em.set_thumbnail(url=get_icon("photo"))
            em.set_footer(text="You gave it your Rec Room best! [|=)]")
            await message.edit(embeds=[em, self.current_embed], view=self)
        

@slash_command(
    name="image",
    description="Guess the year in which the images were taken!",
    guild_ids=config.get("debug_guilds", [])
)
async def image(
    self, 
    ctx: discord.ApplicationContext
):
    await ctx.interaction.response.defer()

    view = ImageQuiz(self.bot.RecNet)
    await view.respond(ctx.interaction)

    
    

        

        
