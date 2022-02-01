from discord import Embed
from .. import finalize_embed, filter_embed
from scripts import Emoji, img_url, post_url

"""Makes an embed for RecNet post stats"""
def stats_embed(ctx, user):
    # Embed description stats
    info = f"""
Pictures shared `{len(user.posts):,}`
Posts tagged in `{len(user.feed):,}`
    """

    # Define embed  
    em = Embed(
        title = f"RecNet statistics of {user.display_name}",
        description = info
    )

    # GATHER STATS
    total_cheers, total_comments, unique_cheered_posts, unique_commented_posts, most_cheered_post, most_commented_post = 0, 0, 0, 0, None, None
    for post in user.posts:
        if not user.posts: break

        if post.cheer_count: unique_cheered_posts += 1  # Unique cheered posts
        if post.comment_count: unique_commented_posts += 1  # Unique commented posts

        if not hasattr(most_cheered_post, 'cheer_count') or post.cheer_count > most_cheered_post.cheer_count:
            most_cheered_post = post  # Most cheered post

        if not hasattr(most_commented_post, 'comment_count') or post.comment_count > most_commented_post.comment_count:
            most_commented_post = post  # Most commented post

        total_cheers += post.cheer_count  # Total cheers
        total_comments += post.comment_count  # Total comments

    if user.posts:
        em.add_field(name=f"{Emoji.cheer} Cheers", value=create_cheer_section(total_cheers, unique_cheered_posts, most_cheered_post), inline=True)
        em.add_field(name=f"{Emoji.comment} Comments", value=create_comment_section(total_comments, unique_commented_posts, most_commented_post), inline=True)
        if user.feed:
            em.add_field(name="Posts", value=create_important_posts_section(user.posts, user.feed), inline=False)

    # Set the image as the post
    em.set_thumbnail(url=img_url(user.profile_image, crop_square=True))  # Just in case it somehow doesn't exist.

    em = finalize_embed(ctx, em)
    return em  # Return the embed.

def create_important_posts_section(posts, feed):
    return f"""
[First post]({post_url(posts[0].id)}) | [Latest post]({post_url(posts[-1].id)})
[First post tagged in]({post_url(feed[0].id)}) | [Latest post tagged in]({post_url(feed[-1].id)})
    """

def create_comment_section(total_comments, unique_commented_posts, most_commented_post):
    if total_comments: avg_comments = round(total_comments / unique_commented_posts, 1)
    else: avg_comments = 0

    if most_commented_post.comment_count > 0:
        most_commented_post_section = f"""
[Most commented post]({post_url(most_commented_post.id)})
{Emoji.cheer} `{most_commented_post.cheer_count:,}` {Emoji.comment} `{most_commented_post.comment_count:,}`
        """
    else: most_commented_post_section = ""

    return f"""
Total comments `{total_comments:,}`
Total commented posts `{unique_commented_posts:,}`
Average comments per commented posts `{avg_comments:,}`
{most_commented_post_section}
    """
    
def create_cheer_section(total_cheers, unique_cheered_posts, most_cheered_post):
    if total_cheers: avg_cheers = round(total_cheers / unique_cheered_posts, 1)
    else: avg_cheers = 0

    if most_cheered_post.cheer_count > 0:
        most_cheered_post_section = f"""
[Most cheered post]({post_url(most_cheered_post.id)})
{Emoji.cheer} `{most_cheered_post.cheer_count:,}` {Emoji.comment} `{most_cheered_post.comment_count:,}`
        """
    else: most_cheered_post_section = ""

    return f"""
Total cheers `{total_cheers:,}`
Total cheered posts `{unique_cheered_posts:,}`
Average cheers per cheered posts `{avg_cheers:,}`
{most_cheered_post_section}
    """