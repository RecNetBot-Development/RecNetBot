import discord
from exceptions import ConnectionNotFound
from utils import sanitize_bio, profile_url, img_url
from utils.converters import FetchAccount
from embeds import get_default_embed
from discord.commands import slash_command
from discord.ext.bridge import BridgeOption as Option
from utils.autocompleters import account_searcher
from database import ConnectionManager

class Menu(discord.ui.View):
    def __init__(self, username: str):
        super().__init__()

        btn = discord.ui.Button(
            label="Profile URL",
            url=profile_url(username),
            style=discord.ButtonStyle.url
        )

        self.add_item(btn)

@slash_command(
    name="bio",
    description="Read a player's bio."
)
async def bio(
    self, 
    ctx: discord.ApplicationContext, 
    account: Option(FetchAccount, name="username", description="Enter RR username", default="", required=False, autocomplete=account_searcher)
):
    await ctx.interaction.response.defer()
    
    if not account:
        cm: ConnectionManager = self.bot.cm
        account = await cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
    
    bio = await account.get_bio()
    
    # Embed skeleton
    em = get_default_embed()
    em.set_author(name=f"@{account.username}", icon_url=img_url(account.profile_image, crop_square=True, resolution=180))

    if not bio: # Check if the user has a bio
        em.description = f"User hasn't set a bio yet!"
        return await ctx.respond(embed=em) 

    em.description = sanitize_bio(bio)
    await ctx.respond(embed=em, view=Menu(account.username))
        

        
