from discord import Embed
from utility.image.finalize_embed import finalize_embed

def json_embed(json: dict, *args, **kwargs):
    if isinstance(json, list):
        json = json[0]
    
    em = Embed()
    for key in json:
        em.add_field(name=key, value=f"```{json[key]}```", inline=False)
    return em