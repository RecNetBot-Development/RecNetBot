from discord import Embed
from ..finalize_embed import finalize_embed
from utility import img_url

"""Makes an embed for a single RecNet post"""
def self_cheers_embed(ctx, user, self_cheers):
    # Information of the post that'll be included in the embed
    if self_cheers:
        info = f"""
`{self_cheers}` self-cheered posts found! Shame on this user.
That's `{round(self_cheers / len(user.posts)* 10)}`% of their posts!
        """
    else:
        info = f"""
No self-cheers found! This user is pure.
        """

    # Define embed  
    em = Embed(
        title = f"{user.display_name}'s self-cheered posts",
        description = info,
        url=f"https://rec.net/user/{user.username}"
    )
    
    em.set_thumbnail(url=img_url(user.profile_image, crop_square=True))
    em = finalize_embed(ctx, em, set_author_footer=not bool(self_cheers), set_timestamp_footer=not bool(self_cheers))
    return em  # Return the embed.