import discord
from utils import sanitize_bio, get_linked_account
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
    print(account)
    
    bio = await account.get_bio()
    if bio: 
        await ctx.respond(
            content=sanitize_bio(bio)
        )
    else:
        em = get_default_embed()
        em.description = f"{account.display_name} hasn't written a bio!"
        await ctx.respond(
            embed=em
        )

        
