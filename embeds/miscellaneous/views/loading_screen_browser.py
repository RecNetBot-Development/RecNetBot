import discord
from random import randint
from utility.emojis import get_emoji
from ..loading_screen_embed import loading_screen_embed

class LoadingScreens(discord.ui.View):
    def __init__(self, ctx, rec_net):
        super().__init__(
            timeout=None
        )
        self.ctx = ctx
        self.index = 0
        self.rec_net = rec_net
        self.loading_screens = []
        
    async def start(self):
        ls_resp = await self.rec_net.rec_net.cdn.config.LoadingScreenTipData.get().fetch()
        self.loading_screens = ls_resp.data
        return self, self.create_embed()
        
    @discord.ui.button(emoji=get_emoji('prev'), style=discord.ButtonStyle.primary, row=0, custom_id="persistent:ls_ui_previous_1")
    async def previous1(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.update_index(-1)
        await self.handle_message(interaction)
        
    @discord.ui.button(emoji=get_emoji('next'), style=discord.ButtonStyle.primary, row=0, custom_id="persistent:ls_ui_next_1")
    async def next1(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.update_index(1)
        await self.handle_message(interaction)
        
    @discord.ui.button(emoji=get_emoji('random'), style=discord.ButtonStyle.primary, row=0, custom_id="persistent:ls_ui_random")
    async def random(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.random_index()
        await self.handle_message(interaction)
        
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
        return loading_screen_embed(self.loading_screens[self.index])
    
    async def interaction_check(self, interaction):
        return self.ctx.user == interaction.user
