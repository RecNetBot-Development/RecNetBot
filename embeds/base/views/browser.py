import discord
from random import randint

class Browser(discord.ui.View):
    def __init__(self, data):
        super().__init__(
            timeout=None
        )
        self.index = 0
        self.data = data
        
    @discord.ui.button(label="< 1", style=discord.ButtonStyle.primary, row=1, custom_id="persistent:ls_ui_previous_1")
    async def previous1(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.update_index(-1)
        await self.handle_message(interaction)
        
    @discord.ui.button(label="1 >", style=discord.ButtonStyle.primary, row=1, custom_id="persistent:ls_ui_next_1")
    async def next1(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.update_index(1)
        await self.handle_message(interaction)
        
    @discord.ui.button(label="Random", style=discord.ButtonStyle.primary, row=1, custom_id="persistent:ls_ui_random")
    async def random(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.random_index()
        await self.handle_message(interaction)
        
    async def respond(self, interaction):
        embed = self.create_embed()
        await interaction.respond(embed=embed, view=self)
    
    def update_index(self, index_add):
        new_index = self.index + index_add
        if new_index < 0:
            self.index = 0
        elif new_index > len(self.loading_screens)-1:
            self.index = len(self.loading_screens)-1
        else:
            self.index = new_index
            
    def random_index(self):
        self.index = randint(0, len(self.loading_screens)-1)
     
    async def handle_message(self, interaction):
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)
        
    def create_embed(self):
        ...
