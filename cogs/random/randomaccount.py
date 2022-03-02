from discord import Embed
from utility import load_cfg, get_recent_account_id
from discord.commands import slash_command, Option # Importing the decorator that makes slash commands.
from embeds import RandomAccount
from random import randint

cfg = load_cfg()

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="randomaccount",
    description="Find a random account!"
)
async def randomaccount(
    self, 
    ctx,
    account_year: Option(str, "Choose accounts' creation year", choices=["2016", "Latest"], required=False, default="Latest"),
    specify: Option(str, "Choose specific information", choices=["Profile", "Bio", "Profile Picture"], required=False, default="Profile")
):
    await ctx.interaction.response.defer()
        
    max_id = int(account_year) if not account_year == "Latest" else 0
    view, embed = await RandomAccount(ctx, self.bot.rec_net, max_id, specify).start()
    await ctx.respond(embed=embed, view=view)   