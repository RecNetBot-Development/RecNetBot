import discord
from utils import get_linked_account, img_url
from embeds import get_default_embed
from utils.converters import FetchAccount
from discord.commands import slash_command, Option

@slash_command(
    name="pfp",
    description="Fetch a Rec Room user's uncropped profile picture with many resolution options."
)
async def pfp(
    self,   
    ctx: discord.ApplicationContext,
    account: Option(FetchAccount, name="username", description="Enter RR username", default=None, required=False)
):
    await ctx.interaction.response.defer()
    
    if not account:  # Check for a linked RR account
        account = await get_linked_account(self.bot.cm, self.bot.RecNet, ctx.author.id)
        
    resolutions = (480, 360, 180)
        
    em = get_default_embed()
    # Make a list of pfp's with different resolutions
    em.description = "\n".join(map(lambda res: f"[{res}]({img_url(account.profile_image, resolution=res)})", resolutions))
        
    await ctx.respond(img_url(account.profile_image, resolution=1080), embed=em) 
        
    
    
    