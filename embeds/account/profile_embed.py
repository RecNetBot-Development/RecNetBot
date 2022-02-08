from discord import Embed
from embeds.finalize_embed import finalize_embed
from scripts import Emoji, img_url, unix_timestamp

"""Makes an embed for a single profile"""
def profile_embed(ctx, user, specify = ""):
    match specify:  # If only something specific is wanted
        case "platforms":
            platforms_section = create_platforms_section(user)

            em = Embed(
                title=f"{user.display_name}'s platforms",
                description=platforms_section if platforms_section else 'No known platforms!'
            )

            em = finalize_embed(ctx, em)
            return em

    platforms_section = create_platforms_section(user)

    profile_desc = f"""
@{user.username}
{Emoji.level} Level `{user.level}`
{Emoji.visitors} Subscribers `{user.subscriber_count:,}`
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
    em.set_image(url=img_url(user.banner_image) if user.banner_image else 'https://cdn.rec.net/static/banners/default_player.png')

    em = finalize_embed(ctx, em)
    return em  # Return the embed.

def create_platforms_section(user):
    platform_info = {
        'Steam': f'{Emoji.steam} [`Steam`](https://store.steampowered.com/app/471710/Rec_Room/)', 
        'Oculus': f'{Emoji.oculus} [`Oculus`](https://www.oculus.com/experiences/quest/2173678582678296/)', 
        'PlayStation': f'{Emoji.playstation} [`PlayStation`](https://store.playstation.com/en-us/product/EP2526-CUSA09539_00-RECROOM000000001)', 
        'Xbox': f'{Emoji.xbox} [`XBox`](https://www.xbox.com/en-ZA/games/store/rec-room/9pgpqk0xthrz)',
        'iOS': f'{Emoji.ios} [`iOS`](https://apps.apple.com/us/app/rec-room/id1450306065)', 
        'Android': f'{Emoji.android} [`Android`](https://play.google.com/store/apps/details?id=com.AgainstGravity.RecRoom)'
    }

    platform_text_list = []
    if user.platforms:
        for platform in user.platforms:
            platform_text_list.append(platform_info.get(platform, ""))
        return ', '.join(platform_text_list)
    else:
        return