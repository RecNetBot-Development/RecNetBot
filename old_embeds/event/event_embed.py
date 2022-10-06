from embeds.base.embed import DefaultEmbed as Embed
from utility.rec_net_helpers import img_url, profile_url, room_url
from utility.funcs import unix_timestamp
from utility import Emoji

"""Makes an embed for a single profile"""
def event_embed(event, specify = ""):
    em = Embed()
    
    match specify.lower():  # If only something specific is wanted
        case _:
            ...

    # Define embed
    em = Embed(
        title = event.name,
        description = f"```{event.description if event.description else 'This event does not have a description!'}```"
    )
    
    is_room_private = not bool(event.room)
    
    if is_room_private:
        room_link = "`[PRIVATE ROOM]`"
    else:
        room_link = f"[`^{event.room.name}`]({room_url(event.room.name)})"
    
    info_field = f"""
{Emoji.room} In Room {room_link}
{Emoji.visitors} Attendees `{event.attendee_count}`
{Emoji.date} {unix_timestamp(event.start_time, "R")} (Starts) - {unix_timestamp(event.end_time, "R")} (Ends)
    """
    em.add_field(name="Info", value=info_field, inline=False)
    
    broadcast_field = f"""
{Emoji.correct if event.is_multi_instance else Emoji.incorrect} Multi Instance
{Emoji.correct if event.supports_live_chat else Emoji.incorrect} Live Chat
    """
    em.add_field(name="Broadcasting", value=broadcast_field, inline=False)

    em.set_author(
        name=event.creator.display_name, 
        url=profile_url(event.creator.username),
        icon_url=img_url(event.creator.profile_image, crop_square=True)
    )

    # Add the banner
    if event.image_name: 
        em.set_image(url=img_url(event.image_name))
        if not is_room_private: em.set_thumbnail(url=img_url(event.room.image_name, crop_square=True))
    elif not is_room_private and event.room.image_name: 
        em.set_image(url=img_url(event.room.image_name))

    return em  # Return the embed.