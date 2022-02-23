from discord import Embed
from embeds.finalize_embed import finalize_embed
from utility import Emoji

def loading_embed(ctx):
    # Define embed
    em = Embed(
        description = f"{Emoji.loading} Processing your command!"
    )
    em = finalize_embed(ctx, em)
    return em