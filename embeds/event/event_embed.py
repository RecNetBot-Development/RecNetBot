from discord import Embed
from utility.rec_net_helpers import img_url
from utility.funcs import unix_timestamp

"""Makes an embed for a single profile"""
def event_embed(event, specify = ""):
    em = Embed()
    
    match specify.lower():  # If only something specific is wanted
        case _:
            ...
            
    event_desc = f"""
```{event.description}```
Start Time {unix_timestamp(event.start_time)}
End Time {unix_timestamp(event.end_time)}
    """

    # Define embed
    em = Embed(
        title = event.name,
        description = event_desc
    )

    # Add the banner
    if event.image_name: em.set_image(url=img_url(event.image_name))
    elif event.room.image_name: em.set_image(url=img_url(event.room.image_name))

    return em  # Return the embed.