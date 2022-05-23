from discord import Embed
from utility import load_cfg, respond
from discord.commands import slash_command, Option # Importing the decorator that makes slash commands.
from embeds import RandomAccount
from random import randint

cfg = load_cfg()

@slash_command(
    debug_guilds=cfg['test_guild_ids'],
    name="account",
    description="Find a random account!"
)
async def randomaccount(
    self, 
    ctx,
    account_year: Option(int, "Choose accounts' creation year", choices=[2016, 2017, 2018, 2019, 2020, 2021], required=False, default=2021),
    specify: Option(str, "Choose specific information", choices=["profile", "bio", "profile picture"], required=False, default="profile")
):
    await ctx.interaction.response.defer()
        
    view, embed = await RandomAccount(ctx, self.bot.rec_net, account_year, specify.capitalize()).start()
    await respond(ctx, embed=embed, view=view)