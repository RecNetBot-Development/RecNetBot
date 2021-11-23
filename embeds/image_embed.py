import discord
from discord import Embed
from discord.ext.commands import Context
from embeds.finalize_embed import finalize_embed
from scripts import date_to_unix
from scripts import Emoji  # RNB Emojis

"""Makes an embed for a single RecNet post"""
def image_embed(ctx: Context, post_data: dict):
    # Unpack required data
    try:
        img_name, acc_id, unix, cheers, comments, event_id, tagged, post_id = post_data['ImageName'], post_data['PlayerId'], date_to_unix(post_data['CreatedAt']), post_data['CheerCount'], post_data['CommentCount'], post_data['PlayerEventId'], post_data['TaggedPlayerIds'], post_data['Id']
    except TypeError:  # Missing required data
        return

    # Information of the post that'll be included in the embed
    info = f"""
        {Emoji.date} <t:{unix}:f>
        {Emoji.cheer} `{cheers}` {Emoji.comment} `{comments}`
        {f"During event: `{event_id}`" if event_id else ""}
        {f"Tagged: `{','.join(str(id) for id in tagged)}`" if tagged else ""}
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