import discord
from exceptions import ConnectionNotFound
from utils import sanitize_bio, profile_url
from utils.converters import FetchAccount
from embeds import get_default_embed
from discord.commands import slash_command, Option

@slash_command(
    name="bio",
    description="Read a player's bio."
)
async def bio(
    self, 
    ctx: discord.ApplicationContext, 
    account: Option(FetchAccount, name="username", description="Enter RR username", default="", required=False)
):
    await ctx.interaction.response.defer()
    
    if not account:
        account = await self.bot.cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
    
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
        

        
