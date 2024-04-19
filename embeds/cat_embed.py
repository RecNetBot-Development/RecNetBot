import discord
from embeds import get_default_embed
from utils.cat_api import Cat

def cat_embed(cat: Cat) -> discord.Embed:
    """
    Creates an embed for a cat
    """
    
    em = get_default_embed()

    # Distribute found cat
    em.set_image(url=cat.img_url)

    # Include breeds if any
    if cat.breeds:
        em.set_footer(text=cat.breeds[0].temperament)

        for i in cat.breeds:
            em.add_field(name=i.name, value=i.description)

    return em