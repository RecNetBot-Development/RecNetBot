import discord
from utils import profile_url
from utils.formatters import format_platforms
from utils.converters import FetchAccount
from embeds import get_default_embed
from discord.commands import slash_command, Option
from exceptions import ConnectionNotFound

@slash_command(
    name="platforms",
    description="See what platforms a Rec Room user has played on."
)
async def platforms(
    self,   
    ctx: discord.ApplicationContext,
    account: Option(FetchAccount, name="username", description="Enter RR username", default=None, required=False)
):
    await ctx.interaction.response.defer()
    
    if not account:  # Check for a linked RR account
        account = await self.bot.cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
    
    if not account.platforms:
        em = get_default_embed()
        em.description = f"[{account.display_name}]({profile_url(account.username)}) hasn't played on any platforms yet!"
        return await ctx.respond(embed=em) 
     
    await ctx.respond(' '.join(format_platforms(account.platforms)))
    