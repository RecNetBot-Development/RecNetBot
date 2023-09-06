import discord
from embeds import get_default_embed
from utils import img_url, profile_url, room_url, unix_timestamp
from resources import get_emoji
from recnetpy.dataclasses.event import Event
from utils.rec_net_urls import event_url


def event_embed(event: Event) -> discord.Embed:
    """
    Creates an embed for a RR event
    """
    
    em = get_default_embed()
    em.title = event.name
    em.url = event_url(event.id)
    if event.description:
        em.description = f"```{event.description}```"
    
    info_field = [
        f"{get_emoji('visitors')} Attendees `{event.attendee_count}`",
        f"{get_emoji('date')} Starts {unix_timestamp(event.start_time, 'R')} - Ends {unix_timestamp(event.end_time, 'R')}"
    ]
    is_room_private = not bool(event.room)
    if not is_room_private:  # if room isn't private
        room_link = f"[`^{event.room.name}`]({room_url(event.room.name)})"
        info_field.insert(0, 
            f"{get_emoji('room')} In Room {room_link}")
        
    em.add_field(name="Info", value="\n".join(info_field), inline=False)
    
    """
    broadcast_field = []
    if event.is_multi_instance:
        broadcast_field.append(f"{get_emoji('correct')} Multi Instance")
    if event.support_multi_instance_room_chat:
        broadcast_field.append(f"{get_emoji('correct')} Live Chat")
    if broadcast_field:
        em.add_field(name="Broadcasting", value="\n".join(broadcast_field), inline=False)
    """

    em.set_author(
        name=event.creator_player.display_name, 
        url=profile_url(event.creator_player.username),
        icon_url=img_url(event.creator_player.profile_image, crop_square=True)
    )

    # Add the banner
    if event.image_name:  # If the event has an image, set that as the image
        em.set_image(url=img_url(event.image_name))
        if not is_room_private: em.set_thumbnail(url=img_url(event.room.image_name, crop_square=True))
    elif not is_room_private and event.room.image_name:   # Otherwise set the room's thumbnail as the image if public
        em.set_image(url=img_url(event.room.image_name))

    return em


async def fetch_event_embed(event: Event, *args, **kwargs) -> discord.Embed:
    """
    Fetches the necessary data required for the embed
    """
    
    await event.get_creator_player()
    await event.get_room(include=0)
    return event_embed(event, *args, **kwargs)