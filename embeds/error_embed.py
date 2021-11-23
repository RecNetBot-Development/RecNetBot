from discord import Embed
from discord.ext.commands import Context
from embeds.finalize_embed import finalize_embed

def error_embed(ctx: Context, error):
    # Define embed
    em = Embed(
        description = str(error)
    )
    #em.set_thumbnail(url="https://i.imgur.com/paO6CDA.png")
    em = finalize_embed(ctx, em)
    return em