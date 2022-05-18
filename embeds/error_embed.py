from discord import Embed
import time
from datetime import datetime
from utility.funcs import unix_timestamp
from utility.image.finalize_embed import finalize_embed

def error_embed(error = "", custom_text = ""):
    # Define embed
    em = Embed(
        title="Uh oh!",
        description = error if error else custom_text
    )
    em.set_thumbnail(url="https://i.imgur.com/paO6CDA.png")
    return em