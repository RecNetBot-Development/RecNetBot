import discord
from utils import img_url, profile_url
from embeds import get_default_embed
from utils.converters import FetchAccount
from discord.commands import slash_command
from discord.ext.bridge import BridgeOption as Option
from exceptions import ConnectionNotFound
from utils.autocompleters import account_searcher
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
        cm: ConnectionManager = self.bot.cm
        account = await cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
        
    # Embed skeleton
    em = get_default_embed()
    em.set_author(name=f"@{account.username}", icon_url=img_url(account.profile_image, crop_square=True, resolution=180))

    if not account.banner_image:  # Check if the user has a banner
        em.description = "User hasn't set a banner yet!"
        return await ctx.respond(embed=em) 
        
    em.set_image(url=img_url(account.banner_image, raw=True))
    await ctx.respond(embed=em, view=Menu(account.banner_image, account.username))
        
    
    
    