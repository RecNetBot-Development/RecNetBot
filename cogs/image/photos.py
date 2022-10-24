import discord
from discord.commands import slash_command, Option
from utils.converters import FetchAccount
from exceptions import ConnectionNotFound, ImagesNotFound
from utils.paginator import RNBPaginator, RNBPage

@slash_command(
    name="photos",
    description="Browse through a user's RecNet posts."
)
async def photos(
    self, 
    ctx: discord.ApplicationContext,
    account: Option(FetchAccount, name="username", description="Enter RR username", default=None, required=False)
):
    await ctx.interaction.response.defer()

    if not account:  # Check for a linked RR account
        account = await self.bot.cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
    
    posts = await account.get_images(take=1_000_000)
    if not posts: raise ImagesNotFound
        
    pages = list(map(lambda ele: RNBPage(ele), posts))
    paginator = RNBPaginator(pages=pages, trigger_on_display=True, show_indicator=False, author_check=True)

    await paginator.respond(ctx.interaction)

    
    

        

        
