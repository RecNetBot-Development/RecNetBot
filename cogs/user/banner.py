import discord
from utils import img_url, profile_url
from embeds import get_default_embed
from utils.converters import FetchAccount
from discord.commands import slash_command, Option
from exceptions import ConnectionNotFound
from utils.autocompleters import account_searcher

@slash_command(
    name="banner",
    description="Get a player's RecNet banner."
)
async def banner(
    self,   
    ctx: discord.ApplicationContext,
    account: Option(FetchAccount, name="username", description="Enter RR username", default=None, required=False, autocomplete=account_searcher)
):
    await ctx.interaction.response.defer()
    
    if not account:  # Check for a linked RR account
        account = await self.bot.cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
        
    if not account.banner_image:  # Check if the user has a banner
        em = get_default_embed()
        em.description = f"[{account.display_name} @{account.username}](<{profile_url(account.username)}>) hasn't set a banner yet!"
        return await ctx.respond(embed=em) 
        
    response = f"[{account.display_name} @{account.username}](<{profile_url(account.username)}>)'s banner:\n"
    await ctx.respond(response + img_url(account.banner_image, raw=True)) 
        
    
    
    