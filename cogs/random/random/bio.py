import discord
import recnetpy
import random
from utils.paginator import RNBPaginator, RNBPage
from typing import List
from recnetpy.dataclasses.image import Image
from discord.commands import slash_command

MAX_PLAYER_ID = 83_276_444

class RandomBio(discord.ui.View):
    def __init__(self, rec_net: recnetpy.Client, amount: int = 1):
        super().__init__()
        self.RecNet = rec_net
        self.timeout = 600
        self.disable_on_timeout = True
        self.amount = amount
        self.account_pool = []
        self.current_accounts = []
        
    async def find_accounts(self) -> List[Image]:
        api_calls = 0

        # Fetch accounts randomly until enough bios are found
        while len(self.account_pool) < self.amount:
            random_accounts = await self.RecNet.accounts.fetch_many(random.sample(range(1, MAX_PLAYER_ID), 100))
            api_calls += 1
            print("Account IDS", random_accounts)
            for i in random_accounts:
                bio = await i.get_bio()
                api_calls += 1
                print("Bio =", bio)
                if bio: self.account_pool.append(i)
                print("Accounts: ", len(self.account_pool))
                if len(self.account_pool) >= self.amount: break
        
        print(api_calls)
        
        # Check if random accounts need to be drawn due to low amount
        if len(self.account_pool) <= self.amount:
            accounts = self.account_pool
            self.account_pool = []
        else:
            # Choose random accounts from image pool
            accounts = []
            for i in range(self.amount):
                accounts.append(random.choice(self.account_pool))
                self.account_pool.remove(accounts[-1])

        return accounts
            

    @discord.ui.button(label="More!", style=discord.ButtonStyle.green)
    async def more(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.defer()

        # Make sure it's the author using the component
        if interaction.user.id != interaction.message.interaction.user.id:
            return await interaction.followup.send("You're not authorized!", ephemeral=True)
        
        # Respond using og response function
        await self.respond(interaction)


    @discord.ui.button(label="Browse", style=discord.ButtonStyle.primary)
    async def browse(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.defer()
        
        pages = list(map(lambda ele: RNBPage(ele), self.current_accounts))
        paginator = RNBPaginator(pages=pages, trigger_on_display=True, show_indicator=False, author_check=False)
        await paginator.respond(interaction, ephemeral=True)
        

    async def respond(self, interaction: discord.Interaction):
        # Respond to interaction with random bios
        accounts = await self.find_accounts()
        self.current_accounts = accounts

        # Get img.rec.net links of image objects
        bios = list(map(lambda account: account.bio, accounts))

        await interaction.edit_original_response(content="\n".join(bios), view=self)
        

@slash_command(
    name="bio",
    description="Find random bios from the depths of RecNet."
)
async def bio(
    self, 
    ctx: discord.ApplicationContext
):
    await ctx.interaction.response.defer()

    view = RandomBio(self.bot.RecNet, amount=3)
    await view.respond(ctx.interaction)

    
    

        

        
