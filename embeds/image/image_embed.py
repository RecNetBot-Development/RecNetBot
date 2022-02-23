from discord import Embed

from rec_net.managers.account.user import User
from ..finalize_embed import finalize_embed
from utility import Emoji, unix_timestamp, img_url

"""Makes an embed for a single RecNet post"""
def image_embed(ctx, image):
    user = image.creator

    # Information of the post that'll be included in the embed
    info = f"""
{Emoji.cheer} `{image.cheer_count}` {Emoji.comment} `{image.comment_count}`
{Emoji.door} `^{image.room}`
{f"{Emoji.event} `{image.event}`"}
{f"{Emoji.visitors} {' '.join(f'[`@{user}`](https://rec.net/user/{user})' for user in image.tagged)} ({len(image.tagged)})"}
{Emoji.date} {unix_timestamp(image.created_at)}
    """

    # Define embed  
    em = Embed(
        title = f"Taken by @{user}",
        description = info,
        url=f"https://rec.net/user/{user}"
    )

    # Set the image as the post
    em.set_image(url=img_url(image.image_name))  # Just in case it somehow doesn't exist.

    em = finalize_embed(ctx, em)
    return em  # Return the embed.