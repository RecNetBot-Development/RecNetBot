import discord
from discord.commands import slash_command, Option
from utils.converters import FetchAccount
from embeds import profile_embed
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
    
    await account.get_subscriber_count()
    await account.get_level()
    await account.get_bio()
    await ctx.respond(
        embed=profile_embed(account)
    )

        
