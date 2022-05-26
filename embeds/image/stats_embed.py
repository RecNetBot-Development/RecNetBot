from embeds.base.embed import DefaultEmbed as Embed
from utility.emojis import get_emoji, get_icon
from utility.rec_net_helpers import post_url
from embeds.headers.profile_header import profile_header

"""Makes an embed for RecNet post stats"""
def stats_embed(user):
    # Define embed  
    em = Embed(
        title = f"{user.display_name}'s RecNet statistics",
        description = "Statistics of public shared posts on RecNet."
    )
    em.set_thumbnail(url=get_icon("photo")) # Add slick photo icon
    em = profile_header(user, em)
    
    # Get stats
    total_shared_photos = len(user.posts)
    total_tagged_photos = len(user.feed)
    total_cheers = get_total_cheers(user.posts)
    total_comments = get_total_comments(user.posts)
    
    em.add_field(
        name="Total Stats",
        value=
        f"{get_emoji('cheer')} `{total_cheers:,}` — Cheers\n"
        f"{get_emoji('comment')} `{total_comments:,}` — Comments\n"
        f"{get_emoji('image')} `{total_shared_photos:,}` — Photos Shared\n"
        f"{get_emoji('visitors')} `{total_tagged_photos:,}` — Photos Tagged In",
        inline=False
    )
    
    # Return it if no shared posts because remaining fields require posts
    if not total_shared_photos:  return em
    
    most_cheered_post = get_most_cheered_post(user.posts)
    most_commented_post = get_most_commented_post(user.posts)
    
    em.add_field(
        name="Most Cheered Post",
        value=
        f"{get_emoji('cheer')} `{total_cheers:,}` — Cheers\n"
        f"{get_emoji('link')} [RecNet Link]({post_url(most_cheered_post.id)})",
        inline=True
    )
    
    em.add_field(
        name="Most Commented Post",
        value=
        f"{get_emoji('comment')} `{total_cheers:,}` — Comments\n"
        f"{get_emoji('link')} [RecNet Link]({post_url(most_commented_post.id)})",
        inline=True
    )
    
    return em

def get_most_cheered_post(posts):
    return max(posts, key=lambda post: post.cheer_count)

def get_most_commented_post(posts):
    return max(posts, key=lambda post: post.comment_count)

def get_total_cheers(posts):
    return sum(map(lambda post: post.cheer_count, posts))

def get_total_comments(posts):
    return sum(map(lambda post: post.cheer_count, posts))