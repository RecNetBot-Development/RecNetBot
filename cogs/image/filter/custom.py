import discord
from discord.commands import slash_command, Option
from utils.converters import FetchAccount
from exceptions import ConnectionNotFound, ImagesNotFound
from utils.paginator import RNBPaginator, RNBPage
from embeds import get_default_embed

@slash_command(
    name="custom",
    description="Combine all filters together to find specific RecNet posts."
)
async def custom(
    self, 
    ctx: discord.ApplicationContext,
    _sort: Option(str, name="sort", description="Choose what to sort by", required=False, choices=[
        "Oldest to Newest", 
        "Cheers: Highest to Lowest",
        "Comments: Highest to Lowest",
        "Tags: Highest to Lowest",
    ], default=None) = None,
    together: Option(str, name="together", description="Filter by which RR users are featured in a post (separate by spaces)", required=False, default=None) = None,
    taken_by: Option(FetchAccount, name="taken_by", description="Enter the RR username who took the photos", default=None, required=False) = None
):
    await ctx.interaction.response.defer()
    posts = []

    if taken_by:  # Check for a linked RR account
        posts: list = await taken_by.get_images(take=1_000_000)
    elif together:
        # Fetch the first user from together
        # Since the user is required to be in the post, this will work
        first_user = together.split(" ")[0]
        first_user = await self.bot.RecNet.accounts.get(first_user)
        if first_user:
            posts: list = await first_user.get_feed(take=1_000_000)
        
    # Sort photos
    match _sort:
        case "Oldest to Newest":
            posts.reverse()
        case "Cheers: Highest to Lowest":
            posts.sort(reverse=True, key=lambda image: image.cheer_count)
        case "Comments: Highest to Lowest":
            posts.sort(reverse=True, key=lambda image: image.comment_count)
        case "Tags: Highest to Lowest":
            posts.sort(reverse=True, key=lambda image: len(image.tagged_player_ids))
        case _:  # Don't sort
            ...
        
    # Filter by together
    if together:
        t_users = await self.bot.RecNet.accounts.get_many(together.split(" "))
        
        if t_users:
            posts = list(filter(lambda image: all(user.id in image.tagged_player_ids for user in t_users), posts))
    
    if posts:
        pages = list(map(lambda ele: RNBPage(ele), posts))
        paginator = RNBPaginator(pages=pages, trigger_on_display=True, show_indicator=False, author_check=True)
        await paginator.respond(ctx.interaction)
    else:
        em = get_default_embed()
        em.description = "No posts found, check your filters."
        await ctx.respond(embed=em)

    
    

        

        
