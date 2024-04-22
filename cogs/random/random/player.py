import discord
import recnetpy
import random
from typing import List
from recnetpy.dataclasses.account import Account
from discord.commands import slash_command
from discord.ext.bridge import BridgeOption as Option
from embeds import fetch_profile_embed, get_default_embed

# These are the last ids of the accounts from their respective join year
LAST_ACCOUNT_IDS = {
    2015: 0,
    2016: 69_723,
    2017: 386_114,
    2018: 1_290_001,
    2019: 3_314_552,
    2020: 11_159_630,
    2021: 40_734_808,
    2022: 83_276_444
}

class RandomAccount(discord.ui.View):
    def __init__(self, rec_net: recnetpy.Client, year: int = None, bio_only: bool = False, amount: int = 1):
        super().__init__()
        self.RecNet = rec_net
        self.year = year
        self.bio_only = bio_only
        self.amount = amount
        # Interaction timeout
        self.timeout = 600
        self.disable_on_timeout = True
        # Timeout for fetching accounts
        self.time_out = 10
        
    async def fetch_account(self, amount: int = 1) -> List[Account]:
        attempts, users = 0, []
        while not users:
            # If no user was able to be found
            if attempts >= self.time_out:
                break
            
            # Fetch either by year or a random year if none input
            if self.year:
                year = self.year
            else:
                year = random.choice(list(LAST_ACCOUNT_IDS.keys()))
                if year == 2015: year = 2016
                
            # Fetch the random user
            random_ids = random.sample(range(LAST_ACCOUNT_IDS.get(year-1), LAST_ACCOUNT_IDS.get(year)), amount)
            users = await self.RecNet.accounts.fetch_many(random_ids)
            
            attempts += 1

        return users
            
    async def fetch_with_embed(self) -> List[discord.Embed]:
        users = await self.fetch_account(self.amount)
        
        # If it times out
        if not users:
            embed = get_default_embed()
            embed.description = "Something went wrong and I couldn't find a random account. Try again later!"
            return [embed]
        
        embeds = []
        if self.bio_only:
            embed = get_default_embed()
            for user in users:
                bio = await user.get_bio()
                embed.add_field(name=f"@{user.username}", value=bio, inline=False)
            embeds.append(embed)
        else:
            for user in users:
                em = await fetch_profile_embed(user)
                embeds.append(em)
            
        return embeds
            
    @discord.ui.button(label="Another!", style=discord.ButtonStyle.primary)
    async def again(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.defer()

        # Make sure it's the author using the component
        if interaction.user.id != interaction.message.interaction.user.id:
            return await interaction.followup.send("You're not authorized!", ephemeral=True)
        
        embeds = await self.fetch_with_embed()
        await interaction.edit_original_response(embeds=embeds, view=self)
        
        
    async def respond(self, interaction: discord.Interaction):
        embeds = await self.fetch_with_embed()
        await interaction.edit_original_response(embeds=embeds, view=self)
        

@slash_command(
    name="player",
    description="Lookup random players by join date."
)
async def player(
    self, 
    ctx: discord.ApplicationContext,
    join_date: Option(int, "Choose join date if any", choices=[2016, 2017, 2018, 2019, 2020, 2021, 2022], required=False),
    amount: Option(int, "How many you'd like", min_value=1, max_value=5, default=1)
):
    await ctx.interaction.response.defer()

    view = RandomAccount(self.bot.RecNet, year=join_date, amount=amount)
    await view.respond(ctx.interaction)

    
    

        

        
