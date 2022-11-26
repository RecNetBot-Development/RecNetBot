import discord
import re
from resources import get_emoji
from embeds import get_default_embed
from utils import unix_timestamp, date_to_unix, img_url
from utils.formatters import format_platforms
from utils.paginator import RNBPaginator, RNBPage
from discord.commands import slash_command
from recnetpy.misc.bitmask_decode import bitmask_decode
from recnetpy.dataclasses.account import PLATFORM_LIST

@slash_command(
    name="loadingscreens",
    description="Browse Rec Room's official loading screens."
)
async def loadingscreens(self,  ctx: discord.ApplicationContext):
    resp = await self.bot.RecNet.rec_net.cdn.config.LoadingScreenTipData.make_request("get")
    
    # Check if successfully fetched the loading screens
    if resp.success:
        loading_screens = resp.data
        loading_screens.reverse()  # Fresh ones first
    else:
        await ctx.respond(f"Couldn't fetch the loading screens! Error code: {resp.status}")
    
    # Create paginator
    pages = list(map(lambda ele: RNBPage(embeds=[create_embed(ele)]), loading_screens))
    paginator = RNBPaginator(pages=pages, trigger_on_display=True, show_indicator=False, author_check=True)
    await paginator.respond(ctx.interaction)


def create_embed(data: dict) -> discord.Embed:
    # Get essential information
    timestamp = date_to_unix(data["CreatedAt"])
    platforms = bitmask_decode(data["PlatformMask"], PLATFORM_LIST)
    
    # Create the embed
    em = get_default_embed()
    em.title = data["Title"]
    
    # Replace sprites with unknown emojis
    em.description = re.sub("<sprite .+?>", get_emoji("unknown"), data["Message"])
    
    # Add additional information
    em.description += f"\n\nMade {unix_timestamp(timestamp, 'R')}" \
                      f"\nAimed towards {' '.join(format_platforms(platforms))}"
                      
    # Include if the loading screen is for new players only
    if data["RestrictToNewUsers"]:
        em.description += "\nThis loading screen is only visible to new players!"
                      
    # Add loading screen image
    em.set_image(url=img_url(data["ImageName"]))
    
    return em
        

        
