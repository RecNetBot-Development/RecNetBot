import asyncio
from discord import Embed
from rest.dataclasses.image import Image
from discord.ext.commands import Context
from embeds.finalize_embed import finalize_embed
from rest.wrapper.exceptions import ImageDetailsMissing
from scripts import Emoji

"""Makes an embed for a single RecNet post"""
def image_embed(ctx: Context, image: Image):
    # Unpack required data
    try:
        img_name, acc_id, unix, cheers, comments, event_id, tagged, post_id = image.image_name, image.account_id, image.created_at, image.cheer_count, image.comment_count, image.event_id, image.tagged, image.id
    except TypeError:  # Missing required data
        raise ImageDetailsMissing("Missing required image data!")

    # Information of the post that'll be included in the embed
    info = f"""
        {Emoji.date} <t:{unix}:f>
        {Emoji.cheer} `{cheers}` {Emoji.comment} `{comments}`
        {f"During event: `{event_id}`" if event_id else ""}
        {f"Tagged: `{', '.join(user.username for user in tagged)}`" if tagged else ""}
    """

    # Define embed  
    em = Embed(
        title = f"Taken by @{acc_id}",
        description = info,
        url=f"https://rec.net/image/{post_id}"
    )

    # Set the image as the post
    em.set_image(url="https://img.rec.net/" + img_name if img_name is not None else "DefaultProfileImage")  # Just in case it somehow doesn't exist.

    em = finalize_embed(ctx, em)
    return em  # Return the embed.

    
"""Makes embeds for all posts in a list"""
def image_embed_bulk(post_data_list: list):
    post_embeds = []
    for post in post_data_list:
        post_embeds.append(image_embed(post))

    return post_embeds