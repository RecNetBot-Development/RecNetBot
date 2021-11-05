import discord
from .funcs import date_to_unix


# Makes an embed for a RecNet post
async def image_embed(post_data):
    # Unpack required data
    img_name, acc_id, unix, cheers, comments, event_id, tagged = post_data['ImageName'], post_data['PlayerId'], date_to_unix(post_data['CreatedAt']), post_data['CheerCount'], post_data['CommentCount'], post_data['PlayerEventId'], post_data['TaggedPlayerIds']
    
    # Information of the post that'll be included in the embed
    info = f"""
        Posted by {acc_id}
        Posted at <t:{unix}:f>
        Cheers: {cheers}
        Comments: {comments}
        During event: {event_id}
        Tagged: {tagged}
    """

    # Define embed
    em = discord.Embed(
        title = "Image",
        description = info,
        colour = discord.Colour.orange(),
    )

    # Set the image as the post
    em.set_image(url="https://img.rec.net/" + img_name)

    return em  # Return the embed.
