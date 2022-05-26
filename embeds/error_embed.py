from embeds.base.embed import DefaultEmbed as Embed
from utility.emojis import get_icon

def error_embed(error = "", custom_text = ""):
    # Define embed
    em = Embed(
        title="Uh oh!",
        description = error if error else custom_text
    )
    em.set_thumbnail(url=get_icon("unknown"))
    return em