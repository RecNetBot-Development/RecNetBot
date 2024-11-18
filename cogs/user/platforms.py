import discord
from utils import profile_url, img_url
from utils.formatters import format_platforms, TOTAL_PLATFORMS
from utils.converters import FetchAccount
from embeds import get_default_embed
from discord.commands import slash_command
from discord.ext.bridge import BridgeOption as Option
from exceptions import ConnectionNotFound
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
    name="platforms",
    description="See what platforms a player has played on."
)
async def platforms(
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

    if not account.platforms:
        em.description = "User hasn't played on any platforms yet!"
        return await ctx.respond(embed=em) 
     
    # Create the embed and send
    em.description = "All the platforms this user has played on:\n"
    em.description += ' '.join(format_platforms(account.platforms))

    # Include extra info on how many total platforms the user has played on
    extra_info = f"{len(account.platforms)} of {TOTAL_PLATFORMS} platforms."
    if len(account.platforms) == TOTAL_PLATFORMS:
        extra_info += " Nice collection!"
    em.set_footer(text=extra_info)
    
    await ctx.respond(embed=em, view=Menu(account.username))
    