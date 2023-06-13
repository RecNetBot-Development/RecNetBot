import discord
from utils import profile_url
from utils.formatters import format_platforms
from utils.converters import FetchAccount
from embeds import get_default_embed
from discord.commands import slash_command, Option
from exceptions import ConnectionNotFound
from utils.autocompleters import account_searcher

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
        account = await self.bot.cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
    
    # Embed skeleton
    em = get_default_embed()

    if not account.platforms:
        em.description = f"[{account.display_name} @{account.username}](<{profile_url(account.username)}>) hasn't played on any platforms yet!"
        return await ctx.respond(embed=em) 
     
    # Create the embed and send
    em.title = f"Platforms {account.display_name} @{account.username} has played on"
    #em.url = profile_url(account.username)
    em.description = ' '.join(format_platforms(account.platforms))
    await ctx.respond(embed=em)
    