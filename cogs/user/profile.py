import discord
from resources import get_emoji
from utils import unix_timestamp, img_url, format_platforms, format_identities, format_pronouns, sanitize_bio
from embeds import get_default_embed
from recnetpy.dataclasses.account import Account
from exceptions import AccountNotFound, ConnectionNotFound
from discord.commands import slash_command, Option

@slash_command(
    name="profile",
    description="View someone's Rec Room profile."
)
async def profile(
    self, 
    ctx: discord.ApplicationContext, 
    username: Option(str, "Enter RR username", default="", required=False)
):
    await ctx.interaction.response.defer()
    
    if not username:  # Check for a linked RR account
        connection = self.bot.cm.get_discord_connection(ctx.author.id)
        if not connection: raise ConnectionNotFound
        account: Account = await self.bot.RecNet.accounts.fetch(connection.rr_id)
    else:  # Go with specified username
        account: Account = await self.bot.RecNet.accounts.get(username)
    if not account: raise AccountNotFound
    
    await account.get_subscriber_count()
    await account.get_level()
    await account.get_bio()
    await ctx.respond(
        embed=profile_embed(account)
    )

        
def profile_embed(account: Account) -> discord.Embed:
    """
    Generates a neat embed that overhauls a RR profile
    
    Additional requirements:
        - sub count
        - level
        - bio
    """
    
    em = get_default_embed()
    info = [
        f"{get_emoji('username')} @{account.username}",
        f"{get_emoji('level')} Level `{account.level.level}`",
        f"{get_emoji('subscribers')} Subscribers `{account.subscriber_count:,}`",
        f"{get_emoji('pronouns')} {format_pronouns(account.personal_pronouns)}" if account.personal_pronouns else None,
        f"{get_emoji('identities')} {' '.join(format_identities(account.identity_flags))}" if account.identity_flags else None,
        f"```{sanitize_bio(account.bio)}```" if account.bio else None,
        f"{get_emoji('junior') if account.is_junior else get_emoji('mature')} {'Junior account!' if account.is_junior else 'Mature account!'}",
        f' '.join(format_platforms(account.platforms)) if account.platforms else None,
        f"{get_emoji('date')} Joined {unix_timestamp(account.created_at)}"
    ]
    em.description = "\n".join(filter(lambda ele: ele, info))
    
    em.title = account.display_name
    em.set_thumbnail(
        url=img_url(account.profile_image, crop_square=True)
    )
    
    if account.banner_image:
        em.set_image(url=img_url(account.banner_image))
    
    return em