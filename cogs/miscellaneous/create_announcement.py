import discord
import random
from embeds import announcement_embed
from discord.commands import slash_command, Option
from discord.ext.commands import is_owner
from utils import unix_timestamp, load_config
from database import Announcement


# Define a simple View that gives us a confirmation menu.
class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.timeout = 600
        self.disable_on_timeout = True

    # When the confirm button is pressed, set the inner value
    # to `True` and stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.send_message("Confirming", ephemeral=True)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`.
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
    async def cancel_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.send_message("Cancelling", ephemeral=True)
        self.value = False
        self.stop()


class AnnouncementModal(discord.ui.Modal):
    def __init__(self, manager, *args, **kwargs) -> None:
        super().__init__(
            discord.ui.InputText(
                label="Title",
                placeholder="Title for the announcement",
                style=discord.InputTextStyle.short
            ),
            discord.ui.InputText(
                label="Description",
                placeholder="Description for the announcement",
                style=discord.InputTextStyle.paragraph
            ),
            discord.ui.InputText(
                label="Image URL",
                placeholder="Optional image for the announcement",
                style=discord.InputTextStyle.short,
                required=False
            ),
            discord.ui.InputText(
                label="Expiration Timestamp",
                placeholder="Optional timestamp for when the announcement should expire",
                style=discord.InputTextStyle.short,
                required=False
            ),
            *args,
            **kwargs,
        )

        self.manager = manager

    async def callback(self, interaction: discord.Interaction):
        announcement = Announcement(
            id=0,
            title=self.children[0].value,
            unix_timestamp=0,
            description=self.children[1].value,
            image_url=self.children[2].value,
            expiration_timestamp=int(self.children[3].value)
        )

        # Add clarification for expirations
        if announcement.expiration_timestamp:
            expiration_confirmation = f" Announcement will expire {unix_timestamp(announcement.expiration_timestamp, 'F')}"
        else:
            expiration_confirmation = ""

        em = announcement_embed(announcement)

        # We create the View and assign it to a variable so that we can wait for it later.
        view = Confirm()
        await interaction.response.send_message("Publish this announcement? All previous announcements will be ignored." + expiration_confirmation, view=view, embed=em)
        # Wait for the View to stop listening for input...
        await view.wait()

        if view.value: 
            # Confirmed
            self.manager.create_announcement(
                title=self.children[0].value,
                description=self.children[1].value,
                image_url=self.children[2].value,
                expiration_timestamp=self.children[3].value
            )
            await interaction.followup.send("Announcement published! ✅")
        else:
            # Denied
            await interaction.followup.send("Announcement discarded. ❌")




config = load_config(is_production=True)

@slash_command(
    name="create_announcement",
    guild_ids=config.get("debug_guilds", [])
)
@is_owner()
async def announcement(
    self, 
    ctx: discord.ApplicationContext
):
    acm = self.bot.acm
    modal = AnnouncementModal(title="Send an announcement", manager=acm)
    await ctx.send_modal(modal)   


    
    

        

        
