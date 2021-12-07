import discord
from embeds import image_embed

class ImageUI(discord.ui.View):
    def __init__(self, ctx, photos):
        super().__init__()  
        self.ctx = ctx
        self.photos = photos
        self.index = 0

    async def start(self):
        embed = self.create_embed()
        await self.ctx.respond(embed=embed, view=self)

    @discord.ui.button(label="Latest", style=discord.ButtonStyle.red, row=0)
    async def latest(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.update_image(interaction, 0)

    @discord.ui.button(label="Oldest", style=discord.ButtonStyle.red, row=0)
    async def oldest(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.update_image(interaction, len(self.photos))

    @discord.ui.button(label="< 10", style=discord.ButtonStyle.red, row=1)
    async def previous10(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.update_image(interaction, -10)

    @discord.ui.button(label="< 1", style=discord.ButtonStyle.red, row=1)
    async def previous(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.update_image(interaction, -1)

    @discord.ui.button(label="1 >", style=discord.ButtonStyle.red, row=1)
    async def next(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.update_image(interaction, 1)

    @discord.ui.button(label="10 >", style=discord.ButtonStyle.red, row=1)
    async def next10(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.update_image(interaction, 10)

    async def update_image(self, interaction, index_add):
        if not index_add:  # If it's 0, reset to first image
            self.index = 0
        else:
            self.index += index_add
            if self.index > len(self.photos)-1: self.index = len(self.photos)-1
            if self.index < 0: self.index = 0

        embed = self.create_embed()
        await interaction.response.edit_message(content=f"Index: `{self.index+1}/{len(self.photos)}`", embed=embed, view=self)

    def create_embed(self):
        embed = image_embed(self.ctx, self.photos[self.index])
        return embed