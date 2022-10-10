import discord
from discord.commands import slash_command, Option
from utils.converters import FetchAccount
from embeds import fetch_profile_embed
from exceptions import ConnectionNotFound

@slash_command(
    name="profile",
    description="View a Rec Room profile with additional information.",
    
)
async def profile(
    self,   
    ctx: discord.ApplicationContext,
    account: Option(FetchAccount, name="username", description="Enter RR username", default=None, required=False)
):
    await ctx.interaction.response.defer()
    
    if not account:  # Check for a linked RR account
        account = await self.bot.cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
    
    em = await fetch_profile_embed(account)
    await ctx.respond(
        embed=em
    )

        
