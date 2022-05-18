import discord
from ....components.rec_net_link_button import RecNetLinkButton
from ..profile_embed import profile_embed
from random import randint
from utility import get_recent_account_id
from utility.emojis import get_emoji

class RandomAccount(discord.ui.View):
    def __init__(self, ctx, rec_net, year = 2016, specify = "Profile"):
        super().__init__(
            timeout=None
        )
        self.ctx = ctx  
        self.rec_net = rec_net
        self.specify = specify
        self.year = year  # year range for accounts
        
        self.last_account_ids = {
            2015: 0,
            2016: 69_723,
            2017: 386_114,
            2018: 1_290_001,
            2019: 3_314_552,
            2020: 11_159_630,
            2021: 40_734_808
        }
            
    async def start(self):
        embed = await self.find_account_and_return_embed()
        return self, embed 
    
    async def find_account_and_return_embed(self, interaction = None):
        while True:
            random_account_id = randint(self.last_account_ids.get(self.year-1)+1, self.last_account_ids.get(self.year))
            try:
                match self.specify:
                    case "Bio":
                        user = await self.rec_net.account(id=random_account_id, includes=["bio"])
                        if not user.bio: continue
                    case "Profile Picture":
                        user = await self.rec_net.account(id=random_account_id)
                        if user.profile_image == "DefaultProfileImage": continue   
                    case _:  # Profile
                        user = await self.rec_net.account(id=random_account_id, includes=["bio", "progress", "subs"])
                        if not user: continue
                break
            except BaseException as err:
                print(f"Unexpected {err=}, {type(err)=}")
                continue
            
        return profile_embed(user, specify=self.specify)
    
    async def handle_message(self, interaction):
        embed = await self.find_account_and_return_embed(interaction)
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(emoji=get_emoji('random'), style=discord.ButtonStyle.primary, row=0, custom_id="persistent:random_account_ui_another")
    async def another(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.handle_message(interaction)