import discord
from utils import img_url
from embeds import get_default_embed
from utils.converters import FetchAccount
from discord.commands import slash_command
from discord.ext.bridge import BridgeOption as Option
from exceptions import ConnectionNotFound
from utils.autocompleters import account_searcher
from utils import profile_url
from database import ConnectionManager

class Menu(discord.ui.View):
    def __init__(self, image_name: str, username: str):
        super().__init__()

        btn = discord.ui.Button(
            label="Image URL",
            url=img_url(image_name, resolution=0),
            style=discord.ButtonStyle.url
        )
        self.add_item(btn)

        btn2 = discord.ui.Button(
            label="Profile URL",
            url=profile_url(username),
            style=discord.ButtonStyle.url
        )
        self.add_item(btn2)

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
        cm: ConnectionManager = self.bot.cm
        account = await cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
        
    #resolutions = (480, 360, 180)
        
    #em = get_default_embed()
    # Make a list of pfp's with different resolutions
    #em.description = "\n".join(map(lambda res: f"[{res}]({img_url(account.profile_image, resolution=res)})", resolutions))
        
    #await ctx.respond(img_url(account.profile_image, raw=True), embed=em)
    
    em = get_default_embed()
    em.set_author(name=f"@{account.username}")
    em.set_image(url=img_url(account.profile_image, raw=True))
    await ctx.respond(embed=em, view=Menu(account.profile_image, account.username)) 
        
    
    
    