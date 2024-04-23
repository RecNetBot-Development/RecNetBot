import discord
import recnetpy
import random
import bisect
from embeds import get_default_embed
from utils import img_url, room_url, BaseView
from recnetpy.dataclasses.room import Room
from discord.commands import slash_command
from resources import get_icon
from utils import load_config

config = load_config(is_production=True)

class RoomButton(discord.ui.Button):
    def __init__(self, name: str, answer_showcase: bool = None):
        self.original_label = name
        if answer_showcase is not None:
            super().__init__(style=discord.ButtonStyle.green if answer_showcase is True else discord.ButtonStyle.red, label=self.original_label, disabled=True)
        else:
            super().__init__(style=discord.ButtonStyle.grey, label=self.original_label)
        self.name = name
        
        self.suggestions = 0

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(invisible=True)

        assert self.view is not None
        view: RoomQuiz = self.view
        
        # Suggest an answer if you're not the author
        if not view.authority_check(interaction):
            # Check if the user has already suggested an answer
            if interaction.user.id in view.suggestions:
                await interaction.followup.send(content="You have already suggested an answer!", ephemeral=True)
                return
                
            # Add +1 to suggestions
            self.suggestions += 1
            
            # Credit user as suggestion maker and prevent from suggesting
            # more than once to a question
            view.suggestions[interaction.user.id] = self.name
            
            # Add to button
            self.label = f"{self.original_label} +{self.suggestions}"
            self.style = discord.ButtonStyle.primary
            await interaction.edit_original_response(view=view)
            return
        
        await view.answer(interaction, self.name)

class NextButton(discord.ui.Button):
    def __init__(self, correct: bool = True):
        super().__init__(
            style=discord.ButtonStyle.green if correct else discord.ButtonStyle.red, 
            label="Next!"
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(invisible=True)

        assert self.view is not None
        view: RoomQuiz = self.view
        
        # Don't let non-authors press any other button
        if not view.authority_check(interaction):
            await interaction.followup.send(content="Not so fast! You can only suggest answers.", ephemeral=True)
            return
        
        await view.respond(interaction)

class LinkButton(discord.ui.Button):
    def __init__(self, link: str):
        super().__init__(
            style=discord.ButtonStyle.link,
            label="RecNet",
            url=link
        )

class ResultButton(discord.ui.Button):
    def __init__(self, correct: bool = True):
        super().__init__(
            style=discord.ButtonStyle.green, 
            label="Results"
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(invisible=True)

        assert self.view is not None
        view: RoomQuiz = self.view
        
        # Don't let non-authors press any other button
        if not view.authority_check(interaction):
            await interaction.followup.send(content="Not so fast! You can only suggest answers.", ephemeral=True)
            return
        
        await view.results(interaction)

class RoomQuiz(BaseView):
    def __init__(self, rec_net: recnetpy.Client):
        super().__init__()
        self.RecNet = rec_net
        self.timeout = 180
        self.current_room: Room = None
        self.amount = 5

        # Modifier
        self.modifier = None
        self.modifier_info = ""

        # Log the answers
        self.answers = {
            "correct": 0,
            "incorrect": 0
        }
        self.streak = 0
        self.best_streak = 0
        self.streak_type = ""
        self.correct_answer = 0

        # Suggesters. Resets every question
        self.suggestions = {}

        # Different caches
        self.room_pool = []
        
    async def get_room(self) -> Room:
        # Fetch rooms until amount is met
        while len(self.room_pool) < self.amount:
            self.room_pool += await self.RecNet.rooms.hot(1000)
        
         # Choose random room from room pool
        #room = random.choice(self.room_pool)
        room = random.choice(self.room_pool)
        self.room_pool.remove(room)

        return room
        
    async def results(self, interaction: discord.Interaction):
        await self.on_timeout()

    async def answer(self, interaction: discord.Interaction, room_name: str):
        # Check if the answer was correct
        correct = room_name == self.correct_answer
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

        # Credit suggestions
        if self.suggestions:
            field = discord.EmbedField(name="Helpers", value="")
            for user_id, room_name_ in self.suggestions.items():
                emoji = "✅" if room_name_ == self.correct_answer else "❌"
                field.value += f"{emoji} <@{user_id}> — ^{room_name_}\n"
            field.value = field.value.rstrip() # Strip lingering newline
            self.current_embed.append_field(field)

        # Clear suggestions
        self.suggestions = {}

        # Update components
        self.clear_items()
        self.add_item(NextButton(correct))
        self.add_item(RoomButton(room_name, answer_showcase=correct))
        self.add_item(LinkButton(room_url(self.current_room.name)))
        self.add_item(ResultButton())

        # Response
        self.current_embed.set_author(
            name='✅ Correct!' if correct else '❌ Incorrect.'
        )
        self.current_embed.description = f"It's called ^{self.current_room.name}."
        self.current_embed.set_footer(text=f"✅ {self.answers['correct']} / {self.answers['incorrect']} ❌")
        self.current_embed.color = discord.Color.green() if correct else discord.Color.red()
        self.update_embed_score_footer()
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
        # Find a random room
        room = await self.get_room()
        self.current_room = room
        self.correct_answer = self.current_room.name

        # Get top images of room
        images = await self.current_room.get_images(sort=1, take=50)

        # Room name buttons
        self.clear_items()
        buttons = [self.correct_answer]
        for i in range(4):
            #random_room = random.choice(self.room_pool)
            random_room = random.choice(self.room_pool)
            buttons.append(random_room.name)

        # Shuffle answers
        random.shuffle(buttons)

        # Random modifier
        self.modifier = None
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
                bisect.insort(buttons) 
            case _:
                # No modifier
                self.modifier = None

        # Add all the year buttons
        for i in buttons:
            self.add_item(RoomButton(i))

        # Add a hint button if there's no modifiers
        #if not self.modifier: self.add_item(HintButton())
        
        #if self.streak >= 2 and self.streak_type == "incorrect":
        #    self.add_item(HintButton())

        # Form an embed
        em = get_default_embed()
        em.set_author(name="Guess which hot room this is!")
        em.set_image(url=img_url(random.choice(images).image_name))
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
            em.title = "Room Quiz Results"
            em.description = "\n".join(stats)
            em.set_footer(text="You gave it your Rec Room best! [|=)]")
            em.set_thumbnail(url=get_icon("room"))
            await message.edit(embeds=[em, self.current_embed], view=self)
        

@slash_command(
    name="room",
    description="Guess the hot room based on its thumbnail!",
    guild_ids=config.get("debug_guilds", [])
)
async def room(
    self, 
    ctx: discord.ApplicationContext
):
    await ctx.interaction.response.defer()

    view = RoomQuiz(self.bot.RecNet)
    await view.respond(ctx.interaction)

    
    

        

        
