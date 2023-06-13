import discord
from utils import img_url
from embeds import get_default_embed
from utils.converters import FetchAccount
from discord.commands import slash_command, Option
from exceptions import ConnectionNotFound
from utils.autocompleters import account_searcher
from utils import profile_url

@slash_command(
    name="pfp",
    description="Get a player's uncropped profile picture."
)
async def pfp(
    self,   
    ctx: discord.ApplicationContext,
    account: Option(FetchAccount, name="username", description="Enter RR username", default=None, required=False, autocomplete=account_searcher)
):
    await ctx.interaction.response.defer()
    
    if not account:  # Check for a linked RR account
        account = await self.bot.cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
        
    #resolutions = (480, 360, 180)
        
    #em = get_default_embed()
    # Make a list of pfp's with different resolutions
    #em.description = "\n".join(map(lambda res: f"[{res}]({img_url(account.profile_image, resolution=res)})", resolutions))
        
    #await ctx.respond(img_url(account.profile_image, raw=True), embed=em)
    
    response = f"[{account.display_name} @{account.username}](<{profile_url(account.username)}>)'s full profile picture:\n"
    await ctx.respond(response + img_url(account.profile_image, raw=True)) 
        
    
    
    