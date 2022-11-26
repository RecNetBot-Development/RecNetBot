import discord
from utils import img_url, profile_url
from embeds import get_default_embed
from utils.converters import FetchAccount
from discord.commands import slash_command, Option
from exceptions import ConnectionNotFound

@slash_command(
    name="banner",
    description="Get a player's RecNet banner."
)
async def banner(
    self,   
    ctx: discord.ApplicationContext,
    account: Option(FetchAccount, name="username", description="Enter RR username", default=None, required=False)
):
    await ctx.interaction.response.defer()
    
    if not account:  # Check for a linked RR account
        account = await self.bot.cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
        
    if not account.banner_image:  # Check if the user has a banner
        return await ctx.respond(
            f"[{account.display_name}](<{profile_url(account.username)}>) hasn't set a banner yet!"
        ) 
        
    await ctx.respond(img_url(account.banner_image, raw=True)) 
        
    
    
    