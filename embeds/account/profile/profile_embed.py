from discord import Embed
from embeds.finalize_embed import finalize_embed
from utility import Emoji, img_url, unix_timestamp, create_platforms_section

"""Makes an embed for a single profile"""
def profile_embed(ctx, user, specify = ""):
    em = Embed()
    em = finalize_embed(ctx, em)
    
    match specify:  # If only something specific is wanted
        case "Platforms":
            platforms_section = create_platforms_section(platform_names=user.platforms)
            em.title = f"{user.display_name}'s platforms"
            em.description = platforms_section if platforms_section else 'No known platforms!'
            em.set_thumbnail(url=img_url(user.profile_image, True))
            return em
        case "Bio":
            em.title = f"{user.display_name}'s bio"
            em.description = f"```{user.bio}```" if user.bio else "User hasn't written a bio!"
            em.set_thumbnail(url=img_url(user.profile_image, True))
            return em
        case "Junior":
            em.title = f"{user.display_name}'s junior status"
            em.description = f"{user.display_name} is a junior." if user.is_junior else f"{user.display_name} is NOT a junior."
            em.set_thumbnail(url=img_url(user.profile_image, True))
            return em
        case "Level":
            em.title = f"{user.display_name}'s level"
            em.description = f"{user.display_name} is level `{user.level}`."
            em.set_thumbnail(url=img_url(user.profile_image, True))
            return em
        case "Profile Picture":
            em.title = f"{user.display_name}'s profile picture"
            if user.profile_image:
                full_image = img_url(user.profile_image, False)
                cropped_image = img_url(user.profile_image, True)
                em.set_image(url=full_image)
                em.set_thumbnail(url=cropped_image)
                em.description = f"""
[Full Image Link]({full_image})
[Cropped Image Link]({cropped_image})
                """
            else:
                em.description = "User hasn't set a profile picture!"
            return em
        case "Banner":
            em.title = f"{user.display_name}'s banner"
            if user.banner_image:
                banner_image =img_url(user.banner_image, False)
                em.set_image(url=banner_image)
                em.description = f"[Banner Image Link]({banner_image})"
            else:
                em.description = "User hasn't set a banner!"
            return em
        case _:
            ...
            
    platforms_section = create_platforms_section(user)
    profile_desc = f"""
@{user.username}
{Emoji.level} Level `{user.level}`
{Emoji.subscribers} Subscribers `{user.subscriber_count:,}`
```{user.bio}```
{Emoji.junior} {'Junior account!' if user.is_junior else 'Adult account!'}
{Emoji.controller} {f'Platforms {platforms_section}' if platforms_section else 'No known platforms!'}
{Emoji.date} Joined {unix_timestamp(user.created_at)}
    """

    # Define embed
    em = Embed(
        title = user.username,
        description = profile_desc
    )

    # Add the pfp
    em.set_thumbnail(url=img_url(user.profile_image, crop_square=True))

    # Add the banner
    if user.banner_image: em.set_image(url=img_url(user.banner_image))
    # em.set_image(url=img_url(user.banner_image) if user.banner_image else 'https://cdn.rec.net/static/banners/default_player.png')

    em = finalize_embed(ctx, em)
    return em  # Return the embed.