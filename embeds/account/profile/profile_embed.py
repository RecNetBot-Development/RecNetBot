from owoify import owoify
from embeds.base.embed import DefaultEmbed as Embed
from embeds.headers.profile_header import profile_header
from utility.emojis import get_emoji
from utility.rec_net_helpers import img_url
from utility.account.create_platform_section import create_platforms_section
from utility.account.create_pronoun_section import create_pronoun_section
from utility.account.create_identity_section import create_identity_section
from utility.funcs import unix_timestamp
from owoify.owoify import Owoness
        
"""Makes an embed for a single profile"""
def profile_embed(user, specify = "", owo = False):
    em = profile_header(user, Embed())
    
    match specify.lower():  # If only something specific is wanted
        case "platforms":
            platforms_section = create_platforms_section(platform_names=user.platforms)
            em.title = f"{user.display_name}'s platforms"
            em.description = platforms_section if platforms_section else 'No known platforms!'
            return em
        case "bio":
            em.title = f"{user.display_name}'s bio"
            em.description = f"```{user.bio}```" if user.bio else "User hasn't written a bio!"
            return em
        case "junior":
            em.title = f"{user.display_name}'s junior status"
            em.description = f"{user.display_name} is a junior." if user.is_junior else f"{user.display_name} is NOT a junior."
            return em
        case "level":
            em.title = f"{user.display_name}'s level"
            em.description = f"{user.display_name} is level `{user.level}`."
            return em
        case "identities":
            identities = create_identity_section(user.identities) 
            em.title = f"{user.display_name}'s identities"
            em.description = identities if identities else "User hasn't set identities yet!"
            return em
        case "pronouns":
            pronouns = create_identity_section(user.pronouns)
            em.title = f"{user.display_name}'s pronouns"
            em.description = pronouns if pronouns else "User hasn't set pronouns yet!"
            return em
        case "profile picture":
            em.title = f"{user.display_name}'s profile picture"
            if user.profile_image:
                full_image = img_url(user.profile_image, False)
                cropped_image = img_url(user.profile_image, True)
                em.set_image(url=full_image)
                em.description = f"""
[Full Image Link]({full_image})
[Cropped Image Link]({cropped_image})
                """
            else:
                em.description = "User hasn't set a profile picture!"
            return em
        case "banner":
            em.title = f"{user.display_name}'s banner"
            if user.banner_image:
                banner_image =img_url(user.banner_image, False)
                em.set_image(url=banner_image)
                em.description = f"[Banner Image Link]({banner_image})"
            else:
                em.description = "User hasn't set a banner!"
            return em
        case _:
            em.remove_author()
            
    platforms_section = create_platforms_section(platform_names=user.platforms)
    pronouns_section = create_pronoun_section(user.pronouns)
    identity_section = create_identity_section(user.identities)
    
    if not owo:
        profile_desc = f"""
    {get_emoji('username')} @{user.username}
    {get_emoji('level')} Level `{user.level}`
    {get_emoji('subscribers')} Subscribers `{user.subscriber_count:,}`
    {get_emoji('pronouns')} {f"Pronouns {pronouns_section if pronouns_section else 'not set!'}"}
    {get_emoji('identities')} {f"Identities {identity_section if identity_section else 'not set!'}"}
    ```{user.bio}```
    {get_emoji('junior') if user.is_junior else get_emoji('mature')} {'Junior account!' if user.is_junior else 'Adult account!'}
    {get_emoji('controller')} {f'Platforms {platforms_section}' if platforms_section else 'No known platforms!'}
    {get_emoji('date')} Joined {unix_timestamp(user.created_at)}
        """
    else:
        # An owoified version. Because why the hell not.
        profile_desc = f"""
    {get_emoji('username')} @{owoify(user.username, Owoness.Uvu)}
    {get_emoji('level')} Wevew `{user.level}`
    {get_emoji('subscribers')} Subscwibews `{user.subscriber_count:,}`
    {get_emoji('pronouns')} {f"Pwonyouns OwO {pronouns_section if pronouns_section else 'nyot set!'}"}
    {get_emoji('identities')} {f"I-Identities {identity_section if identity_section else 'nyot set!'}"}
    ```{owoify(user.bio, Owoness.Uvu)}```
    {get_emoji('junior') if user.is_junior else get_emoji('mature')} {'Junyiow a-account (*￣з￣)!' if user.is_junior else 'Aduwt accwound (*￣з￣)!'}
    {get_emoji('controller')} {f'hehe Pwatfowms OwO {platforms_section}' if platforms_section else 'Nyo knyown pwatfowms!'}
    {get_emoji('date')} Joinyed {unix_timestamp(user.created_at)}
        """

    # Define embed 
    em.title = owoify(user.username, Owoness.Uvu)
    em.description = profile_desc

    # Add the pfp
    em.set_thumbnail(url=img_url(user.profile_image, crop_square=True))

    # Add the banner
    if user.banner_image: em.set_image(url=img_url(user.banner_image))
    # em.set_image(url=img_url(user.banner_image) if user.banner_image else 'https://cdn.rec.net/static/banners/default_player.png')
    
    return em  # Return the embed.