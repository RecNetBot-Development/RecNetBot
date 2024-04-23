import discord
from typing import List
from resources import get_emoji
from utils import unix_timestamp, img_url, sanitize_bio, sanitize_name
from utils.formatters import format_platforms, format_identities, format_pronouns
from embeds import get_default_embed
from recnetpy.dataclasses.account import Account

from utils.rec_net_urls import profile_url

def profile_embed(account: Account) -> discord.Embed:
    """
    Generates a neat embed that overhauls a RR profile
    
    Additional requirements:
        - sub count
        - level
        - bio
    """
    
    em = get_default_embed()
    info = [
        f"{get_emoji('username')} @{sanitize_name(account.username)}",
        f"{get_emoji('level')} Level `{account.level.level}`" if account.level is not None else None,
        f"{get_emoji('subscribers')} Subscribers: `{account.subscriber_count:,}`" if account.subscriber_count is not None else None, # Optional
        f"{get_emoji('pronouns')} {format_pronouns(account.personal_pronouns)}" if account.personal_pronouns else None,
        f"{get_emoji('identities')} {' '.join(format_identities(account.identity_flags))}" if account.identity_flags else None,
        f"```{sanitize_bio(account.bio)}```" if account.bio else None,  # Optional
        f' '.join(format_platforms(account.platforms)) if account.platforms else None,
        f"{get_emoji('date')} Joined {unix_timestamp(account.created_at)}",
        f"{get_emoji('information')} ID: `{account.id}`"
    ]
    em.description = "\n".join(filter(lambda ele: ele, info))
    
    em.title = account.display_name
    if account.display_emoji:
        em.title = f"{em.title} {account.display_emoji}"
    if account.is_influencer:
        em.title = f"{get_emoji('verified')} {em.title}"

    em.url = profile_url(account.username)
    em.set_thumbnail(
        url=img_url(account.profile_image, crop_square=True)
    )
    
    if account.banner_image:
        em.set_image(url=img_url(account.banner_image))
    
    return em


async def fetch_profile_embed(account: Account, include: List = ["subscriber", "level", "bio", "influencer"]) -> discord.Embed:
    """
    Fetches the necessary data and returns the embed
    
    optional include: ["subscriber", "level", "bio", "influencer"]
    """
    
    if "subscriber" in include:
        await account.get_subscriber_count()
    if "level" in include:
        await account.get_level()
    if "bio" in include:
        await account.get_bio()
    if "influencer" in include:
        await account.get_is_influencer()
    
    return profile_embed(account)