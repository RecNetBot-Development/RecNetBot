from discord import Embed
from discord.ext.commands import Context
from embeds.finalize_embed import finalize_embed
from scripts import Emoji

def loading_embed(ctx: Context):
    # Define embed
    em = Embed(
        description = f"{Emoji.loading} Processing your command!"
    )
    em = finalize_embed(ctx, em)
    return em