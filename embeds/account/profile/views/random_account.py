import discord
from ....components.rec_net_link_button import RecNetLinkButton
from ..profile_embed import profile_embed
from random import randint
from utility import get_recent_account_id

class RandomAccount(discord.ui.View):
    def __init__(self, ctx, rec_net, year = 1987, specify = "Profile"):
        super().__init__(
            timeout=None
        )
        self.ctx = ctx  
        self.rec_net = rec_net
        self.specify = specify
        self.year = year  # year range for accounts
        
        self.last_account_ids = {
            2016: 69723 
        }
            
    async def start(self):
        embed = await self.find_account_and_return_embed()
        return self, embed 
    
    async def find_account_and_return_embed(self, interaction = None):
        max_id = self.last_account_ids.get(self.year, await get_recent_account_id())
        while True:
            random_account_id = randint(1, max_id)
            try:
                match self.specify:
                    case "Bio":
                        user = await self.rec_net.account(id=random_account_id, includes=["bio"])
                        if not len(user.bio):
                            continue
                    case "Profile Picture":
                        user = await self.rec_net.account(id=random_account_id)
                        if not len(user.profile_image):
                            continue
                    case _:  # Profile
                        user = await self.rec_net.account(id=random_account_id, includes=["bio", "progress", "subs"])
                break
            except BaseException as err:
                print(f"Unexpected {err=}, {type(err)=}")
                continue
        return profile_embed(self.ctx, user, specify=self.specify.lower())
    
    async def handle_message(self, interaction):
        embed = await self.find_account_and_return_embed(interaction)
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Another!", style=discord.ButtonStyle.primary, row=0, custom_id="persistent:random_account_ui_another")
    async def another(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.handle_message(interaction)