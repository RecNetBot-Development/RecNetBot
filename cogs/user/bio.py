import discord
from exceptions import ConnectionNotFound
from utils import sanitize_bio, profile_url
from utils.converters import FetchAccount
from embeds import get_default_embed
from discord.commands import slash_command, Option
from utils.autocompleters import account_searcher

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
        account = await self.bot.cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
    
    bio = await account.get_bio()
    
    # Embed skeleton
    em = get_default_embed()

    if not bio: # Check if the user has a bio
        em.description = f"[{account.display_name} @{account.username}](<{profile_url(account.username)}>) hasn't set a bio yet!"
        return await ctx.respond(embed=em) 

    em.title = f"{account.display_name} @{account.username}'s bio"
    em.description = sanitize_bio(bio)

    await ctx.respond(embed=em)
        

        
