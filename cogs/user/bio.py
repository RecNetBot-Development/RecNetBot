import discord
from utils import sanitize_bio, get_linked_account, profile_url
from utils.converters import FetchAccount
from embeds import get_default_embed
from recnetpy.dataclasses.account import Account
from exceptions import AccountNotFound, ConnectionNotFound
from discord.commands import slash_command, Option

@slash_command(
    name="bio",
    description="Read someone's Rec Room bio."
)
async def bio(
    self, 
    ctx: discord.ApplicationContext, 
    account: Option(FetchAccount, name="username", description="Enter RR username", default="", required=False)
):
    await ctx.interaction.response.defer()
    
    if not account:
        account = await get_linked_account(self.bot.cm, self.bot.RecNet, ctx.author.id)
    
    bio = await account.get_bio()
    
    if not bio: # Check if the user has a bio
        em = get_default_embed()
        em.description = f"[{account.display_name}]({profile_url(account.username)}) hasn't written a bio!"
        return await ctx.respond(
            embed=em
        )

    await ctx.respond(
        content=sanitize_bio(bio)
    )
        

        
