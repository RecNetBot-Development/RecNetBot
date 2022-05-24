from embeds.base.embed import DefaultEmbed as Embed

def error_embed(error = "", custom_text = ""):
    # Define embed
    em = Embed(
        title="Uh oh!",
        description = error if error else custom_text
    )
    em.set_thumbnail(url="https://i.imgur.com/paO6CDA.png")
    return em