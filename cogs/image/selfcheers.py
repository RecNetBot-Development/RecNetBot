import discord
import time
import asyncio
from discord.commands import slash_command, Option
from embeds import get_default_embed
from utils import img_url, profile_posts_url
from utils.converters import FetchAccount
from exceptions import ConnectionNotFound
from utils.paginator import RNBPaginator, RNBPage

@slash_command(
    name="selfcheers",
    description="See how many times a player has cheered their own RecNet posts."
)
async def selfcheers(
    self, 
    ctx: discord.ApplicationContext,
    account: Option(FetchAccount, name="username", description="Enter RR username", default=None, required=False)
):
    await ctx.interaction.response.defer()

    if not account:  # Check for a linked RR account
        account = await self.bot.cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
    
    start_time = time.perf_counter()
    
    posts = await account.get_images(take=1000)
    new_posts = posts
    while len(new_posts) % 1000 == 0 and new_posts:
        new_posts = await account.get_images(skip=1000 * len(posts) // 1000, take=1000, force=True)  # Skips the previous posts to fetch another 1000
        posts += new_posts
    
    if posts:
        # Filter out images that have no cheers since they can't possibly be self-cheered
        cheered_images = list(filter(lambda image: image.cheer_count, posts))
        
        # Create co-routines for fetching the cheers of the images
        coroutines = map(lambda image: image.get_cheers(), cheered_images)
        
        # Fetch the cheers
        await asyncio.gather(*coroutines)
        
        # Exclude images that are self-cheered
        self_cheered_images = list(filter(lambda image: account.id in image.cheer_player_ids, cheered_images))
    else:
        self_cheered_images = []
    
    end_time = time.perf_counter()
        
    # Create result embed
    em = get_default_embed()
    em.title = f"{account.display_name}'s self-cheers"
    em.url = profile_posts_url(account.username)
    em.set_thumbnail(url=img_url(account.profile_image, crop_square=True))
    em.add_field(
        name="Benchmark",
        value=f"Time elapsed: {round(end_time - start_time, 1)} secs."
    )
    
    if self_cheered_images:  # If there are self-cheers
        percentage = round(len(self_cheered_images) * 100 / len(posts), 1)
        if percentage < 1:
            percentage = "less than 1"
        em.description = f"**{len(self_cheered_images):,}**, that's **{percentage}%** of their posts! How unpure."
        
        pages = list(map(lambda ele: RNBPage(ele), self_cheered_images))
        paginator = RNBPaginator(pages=pages, trigger_on_display=True, show_indicator=False, constant_embed=em, author_check=False)

        await paginator.respond(ctx.interaction)
        
    else:  # If no self-cheers
        em.description = f"No self-cheers in sight! This user is pure."
        
        await ctx.respond(embed=em)
    