from discord import Embed
from rec_net.managers.room.room import Room
from rec_net.managers.event.event import Event
from ..finalize_embed import finalize_embed
from utility import Emoji, unix_timestamp, img_url, room_url, event_url

"""Makes an embed for a single RecNet post"""
def image_embed(ctx, image):
    user = image.creator

    # Information of the post that'll be included in the embed
    info = f"""
{Emoji.cheer} `{image.cheer_count}` {Emoji.comment} `{image.comment_count}`
{Emoji.date} {unix_timestamp(image.created_at)}
    """
    
    # Optional data depending on if it's available
    if isinstance(image.room, Room):  # Include room name
        room = f"[`^{image.room.name}`]({room_url(image.room.name)})" if isinstance(image.room, Room) else 'Unknown!'
        info += f"\n{Emoji.room} {room}"
    if isinstance(image.event, Event):  # include event name
        event = f"[`{image.event.name}`]({event_url(image.event.id)})" if isinstance(image.event, Event) else 'None!'
        info += f"\n{Emoji.event} {event}"
    if image.tagged:  # Include tagged users
        info += f"\n{Emoji.visitors} {' '.join(f'[`@{user.username}`](https://rec.net/user/{user.username})' for user in image.tagged)} ({len(image.tagged)})"
        
    # Define embed  
    em = Embed(
        title = f"Taken by @{user.username}",
        description = info,
        url=f"https://rec.net/user/{user.username}"
    )

    # Set the image as the post
    em.set_image(url=img_url(image.image_name))  # Just in case it somehow doesn't exist.

    em = finalize_embed(ctx, em)
    return em  # Return the embed.