from discord import Embed
from discord.ext.commands import Context
from embeds.finalize_embed import finalize_embed
from scripts import Emoji, img_url, unix_timestamp
from rec_net.managers.account import User

"""Makes an embed for a single profile"""
def profile_embed(ctx: Context, user: User):
    platform_info = {
        'Steam': f'{Emoji.steam} `Steam`', 
        'Oculus': f'{Emoji.oculus} `Oculus`', 
        'PlayStation': f'{Emoji.playstation} `PlayStation`', 
        'Xbox': f'{Emoji.xbox} `XBox`',
        'iOS': f'{Emoji.ios} `iOS`', 
        'Android': f'{Emoji.android} `Android`'
    }
    platform_text_list, platform_text = [], ""
    if user.platforms:
        for platform in user.platforms:
            platform_text_list.append(platform_info.get(platform, ""))
        platform_text = f"Platforms {', '.join(platform_text_list)}"
    else:
        platform_text = "No known platforms!"


    profile_desc = f"""
@{user.username}
{Emoji.level} Level `{user.level}`
{Emoji.visitors} Subscribers `{user.subscriber_count:,}`
```{user.bio}```
{Emoji.junior} {'Junior account!' if user.is_junior else 'Adult account!'}
{Emoji.controller} {platform_text}
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