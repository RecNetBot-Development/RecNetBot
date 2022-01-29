import asyncio
from discord import Embed
from rec_net.managers.image import Image
from discord.ext.commands import Context
from embeds.finalize_embed import finalize_embed
from rec_net.exceptions import ImageDetailsMissing
from scripts import Emoji, unix_timestamp
from scripts.rec_net_helpers import img_url

"""Makes an embed for a single RecNet post"""
def image_embed(ctx: Context, image: Image):
    user = image.user

    # Information of the post that'll be included in the embed
    info = f"""
{Emoji.date} {unix_timestamp(image.created_at)}
{Emoji.cheer} `{image.cheer_count}` {Emoji.comment} `{image.comment_count}`
{f"During event: `{image.event_id}`" if image.event_id else ""}
{f"Tagged: {', '.join(f'[@{user}](https://rec.net/user/{user})' for user in image.tagged)}" if image.tagged else ""}
    """

    # Define embed  
    em = Embed(
        title = f"Taken by @{user}",
        description = info,
        url=f"https://rec.net/image/{image.id}"
    )

    # Set the image as the post
    em.set_image(url=img_url(image.image_name))  # Just in case it somehow doesn't exist.

    em = finalize_embed(ctx, em)
    return em  # Return the embed.

    
"""Makes embeds for all posts in a list"""
def image_embed_bulk(post_data_list: list):
    post_embeds = []
    for post in post_data_list:
        post_embeds.append(image_embed(post))

    return post_embeds