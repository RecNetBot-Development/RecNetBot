import discord
from ..image.ui.image_browser import ImageUI

class RecNetFeedButton(discord.ui.Button):
    def __init__(self, ctx, user):
        super().__init__(
            style=discord.ButtonStyle.primary, 
            label="View feed",
            row=1
        )
        self.ctx = ctx
        self.user = user

    async def callback(self, interaction):
        view, embeds = await ImageUI(ctx=self.ctx, user=self.user, posts=self.user.feed, interaction=interaction, is_component_interaction=True).start()
        await interaction.edit_original_message(embeds=embeds, view=view)