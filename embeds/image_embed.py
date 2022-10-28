import discord
from recnetpy.dataclasses.room import Room
from recnetpy.dataclasses.event import Event
from recnetpy.dataclasses.image import Image
from resources import get_emoji
from utils import img_url, post_url, room_url, event_url, profile_url, unix_timestamp
from embeds import get_default_embed


def image_embed(image: Image) -> discord.Embed:
    """Makes an embed for a single RecNet post"""
    em = get_default_embed()
    em.title = "View RecNet Post"
    em.url = post_url(image.id)
    
    info = [
        f"{get_emoji('cheer')} `{image.cheer_count:,}` {get_emoji('comment')} `{image.comment_count:,}`",  # cheers & comments
        f"{get_emoji('date')} {unix_timestamp(image.created_at)}"  # post date
    ]
    
    # Optional data depending on if it's available
    if image.room:  # Include room name
        room = f"[`^{image.room.name}`]({room_url(image.room.name)})"
        info.insert(1, 
            f"{get_emoji('room')} {room}")
        
    if image.event:  # include event name
        event = f"[`{image.event.name}`]({event_url(image.event.id)})"
        info.insert(1, 
            f"{get_emoji('event')} {event}")
        
    if image.tagged_players:  # Include tagged users
        info.insert(1, 
            f"{get_emoji('tagged')} {' '.join(f'[`@{user.username}`](https://rec.net/user/{user.username})' for user in image.tagged_players)} ({len(image.tagged_players)})")
        
    em.description = "\n".join(info)
        
    em.set_author(name=f"Taken by @{image.player.username}", url=profile_url(image.player.username), icon_url=img_url(image.player.profile_image, True, 240))

    # Set the image as the post
    em.set_image(url=img_url(image.image_name))

    return em

async def fetch_image_embed(image: Image, *args, **kwargs) -> discord.Embed:
    """
    Fetches the necessary data required for the embed
    """
    
    await image.get_event()
    await image.get_room()
    await image.get_tagged_players()
    await image.get_player()
    
    return image_embed(image, *args, **kwargs)