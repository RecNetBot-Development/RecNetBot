from discord import Embed
from embeds.finalize_embed import finalize_embed

def adjective_animal_embed(ctx, name):
    # Define embed
    em = Embed(
        title="Your Animal Adjective name",
        description = f"""
`{name}`
*Generated from the official adjectives and nouns!*
        """
    )
    em = finalize_embed(ctx, em)
    return em