from discord import Embed
from embeds.finalize_embed import finalize_embed

def json_embed(ctx, json: dict):
    em = Embed()
    for key in json:
        em.add_field(name=key, value=f"```{json[key]}```", inline=False)
    em = finalize_embed(ctx, em)
    return em