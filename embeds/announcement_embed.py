import discord
from embeds import get_default_embed
from datetime import datetime
from database import Announcement

def announcement_embed(announcement: Announcement) -> discord.Embed:
    """
    Creates an embed for an announcement
    """
    
    em = get_default_embed()
    em.title = announcement.title
    em.description = announcement.description + "\n\n*You will only see this once!*"
    if announcement.unix_timestamp:
        em.timestamp = datetime.utcfromtimestamp(announcement.unix_timestamp)
    em.set_author(name="Unread Announcement")
    if announcement.image_url: em.set_image(url=announcement.image_url)

    return em