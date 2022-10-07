import discord
from utils import format_platforms, get_linked_account, profile_url
from utils.converters import FetchAccount
from embeds import get_default_embed
from discord.commands import slash_command, Option

@slash_command(
    name="platfroms",
    description="See what platforms a Rec Room user has played on."
)
async def platfroms(
    self,   
    ctx: discord.ApplicationContext,
    account: Option(FetchAccount, name="username", description="Enter RR username", default=None, required=False)
):
    await ctx.interaction.response.defer()
    
    if not account:  # Check for a linked RR account
        account = await get_linked_account(self.bot.cm, self.bot.RecNet, ctx.author.id)
    
    if not account.platforms:
        em = get_default_embed()
        em.description = f"[{account.display_name}]({profile_url(account.username)}) hasn't played on any platforms yet!"
        return await ctx.respond(embed=em) 
     
    await ctx.respond(' '.join(format_platforms(account.platforms)))
    