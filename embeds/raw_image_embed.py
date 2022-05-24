from embeds.base.embed import DefaultEmbed as Embed

def raw_image_embed(url):
    em = Embed().set_image(url=url)
    return em