from discord import Embed, Colour
from .finalize_embed import finalize_embed

def raw_image_embed(ctx, url):
    em = Embed(colour=Colour.orange()).set_image(url=url)
    return em