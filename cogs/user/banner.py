import discord
from utils import img_url, profile_url
from embeds import get_default_embed
from utils.converters import FetchAccount
from discord.commands import slash_command, Option
from exceptions import ConnectionNotFound

@slash_command(
    name="banner",
    description="Fetch a Rec Room user's banner with many resolution options."
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
        
    em = get_default_embed()
        
    if not account.banner_image:  # Check if the user has a banner
        em.description = f"[{account.display_name}]({profile_url(account.username)}) hasn't set a banner yet!"
        return await ctx.respond(embed=em) 
        
    resolutions = (480, 360, 180)
    # Make a list of banners with different resolutions
    em.description = "\n".join(map(lambda res: f"[{res}]({img_url(account.banner_image, resolution=res)})", resolutions))
        
    await ctx.respond(img_url(account.banner_image, resolution=1080), embed=em) 
        
    
    
    