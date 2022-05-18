from discord import Embed
from rec_net.managers.room.room import Room
from rec_net.managers.event.event import Event
from utility.emojis import get_emoji
from utility.funcs import unix_timestamp
from utility.rec_net_helpers import img_url, post_url, room_url, event_url, profile_url
from rec_net.managers.account.user import User

"""Makes an embed for a single RecNet post"""
def image_embed(image):
    user = image.creator

    # Information of the post that'll be included in the embed
    info = f"{get_emoji('cheer')} `{image.cheer_count}` {get_emoji('comment')} `{image.comment_count}`\n{get_emoji('date')} {unix_timestamp(image.created_at)}"
    
    # Optional data depending on if it's available
    if isinstance(image.room, Room):  # Include room name
        room = f"[`^{image.room.name}`]({room_url(image.room.name)})" if isinstance(image.room, Room) else 'Unknown!'
        info += f"\n{get_emoji('room')} {room}"
    if isinstance(image.event, Event):  # include event name
        event = f"[`{image.event.name}`]({event_url(image.event.id)})" if isinstance(image.event, Event) else 'None!'
        info += f"\n{get_emoji('event')} {event}"
    if image.tagged and isinstance(user, User):  # Include tagged users
        info += f"\n{get_emoji('tagged')} {' '.join(f'[`@{user.username}`](https://rec.net/user/{user.username})' for user in image.tagged)} ({len(image.tagged)})"
        
    username = user.username if hasattr(user, 'username') else 'UNKNOWN'
    # Define embed  
    em = Embed(
        title = "View RecNet Post",
        description = info,
        url=post_url(image.id)
    )
    
    em.set_author(name=f"Taken by @{username}", url=profile_url(username), icon_url=img_url(user.profile_image, True, 240))

    # Set the image as the post
    em.set_image(url=img_url(image.image_name))  # Just in case it somehow doesn't exist.

    return em  # Return the embed.