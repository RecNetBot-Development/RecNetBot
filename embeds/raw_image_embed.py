from discord import Embed, Colour

def raw_image_embed(url):
    em = Embed(colour=Colour.orange()).set_image(url=url)
    return em