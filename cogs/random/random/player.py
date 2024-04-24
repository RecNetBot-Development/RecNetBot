import discord
import recnetpy
import random
from typing import List
from recnetpy.dataclasses.account import Account
from discord.commands import slash_command
from discord.ext.bridge import BridgeOption as Option
from embeds import fetch_profile_embed, get_default_embed
from database import ConnectionManager

ACCS = {2015: [], 2016: [1852, 34641, 31469, 1126, 11675, 19517, 3560, 68758, 10665, 16270, 14940, 68792, 39099, 9916, 47520, 21409, 1], 2017: [88815, 347497, 277089, 79211, 78666, 366937, 159154, 319444, 170583, 272386, 213838, 203474, 316681, 372074, 156085, 276676, 310916, 195175, 329824, 311311, 314074, 358788, 352738, 228577, 345800, 156228, 224166, 132126, 144256, 287195, 206193, 121916, 128016, 179907, 85088, 254959, 334909, 198937], 2018: [439000, 620745, 515033, 638796, 546806, 481690, 715200, 418933, 805144, 733388, 1117791, 1110889, 447263, 659865, 493146, 534186, 613951, 487637, 1210785, 872257, 699089, 1023994, 835842, 1232317, 395439, 655687, 860253, 1236914, 791214, 582917, 678296, 622743, 410754, 1155163, 913154, 1195466, 929446, 570960, 1230392, 1052288, 527321, 882822, 1268602, 402301, 419974, 555477, 1242268, 672036, 586891, 686783, 551129, 885181, 730691, 538365, 1142357, 1259740, 489899, 389368, 386806, 1276474, 638716, 837406, 485186, 786607], 2019: [1312288, 2312859, 2527663, 2539447, 1424966, 1751132, 2172278, 2395704, 2881818, 1469774, 1479520, 1686696, 2290395, 1457431, 2049822, 1832582, 1671309, 2859795, 2135398, 3083253, 3254059, 2208153, 1736331, 2393578, 1773739, 2004491, 1697550, 2331343, 3179695, 1861473, 1304945, 1416963, 2057143, 1467035, 1311378, 1634926, 2641274, 1990632, 3294426, 2312978, 1854809, 1717035, 1563266, 1461494, 1888434, 3161996, 2129166, 3038967, 1714923, 1690275, 1732198], 2020: [5731079, 4080515, 4530885, 3912774, 7906190, 3976829, 3710329, 9409892, 6078720, 6445187, 6597567, 4412145, 4710826, 10874001, 6328685, 4213153, 9775057, 5326881, 4105018, 8494666, 4121601, 8628014, 3747531, 9526391, 4168358, 8493879, 8073816, 9310239, 4795658, 8406816, 5220289, 8618408, 3946295, 9942509, 6615476, 11065378, 5469781, 8359555, 6532522, 4468918, 8886115, 4944419], 2021: [20011278, 15184888, 12805529, 14138278, 14861915, 11440809, 26875312, 35341784, 22187222, 13100926, 30816030, 14465533, 17698129, 27886495, 31033344, 36810857, 32564489, 13990274, 19890837, 37408764, 22385053], 2022: [48366317, 45098274, 79245113, 56177294, 65151521, 42336157, 59750188, 70413484], 2023: [], 2024: []}

class RandomAccount(discord.ui.View):
    def __init__(self, rec_net: recnetpy.Client, year: int = 2016, amount: int = 1):
        super().__init__()
        self.RecNet = rec_net
        self.year = year
        # Interaction timeout
        self.timeout = 600
        self.disable_on_timeout = True
        # Timeout for fetching accounts
        self.time_out = 10
        self.users = []
        self.amount = amount
        
    async def fetch_account(self) -> List[Account]:
        attempts = 0
        while len(self.users) < self.amount:
            # If no user was able to be found
            if attempts >= self.time_out:
                break
                
            # Fetch the random user
            pool = ACCS[self.year] if self.year else ACCS[random.randint(2016, 2022)]
            random_ids = random.sample(pool, self.amount)
            self.users += await self.RecNet.accounts.fetch_many(random_ids)
            
            attempts += 1

        # Return first 3 and remove from cache
        return_users = self.users[:self.amount]
        self.users = self.users[self.amount:]

        return return_users
            
    async def fetch_with_embed(self) -> List[discord.Embed]:
        users = await self.fetch_account()
        
        # If it times out
        if not users:
            embed = get_default_embed()
            embed.description = "Something went wrong and I couldn't find a random account. Try again later!"
            return [embed]
        
        embeds = []
        for user in users:
            em = await fetch_profile_embed(user, include=[])
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
    amount: Option(int, "How many you'd like", min_value=1, max_value=5, required=False, default=1) 
):
    await ctx.interaction.response.defer()
    
    view = RandomAccount(self.bot.RecNet, year=join_date, amount=amount)
    await view.respond(ctx.interaction)