from discord import Embed, Color

"""
The default embed for all of RNB 
"""
def get_default_embed(**kwargs) -> Embed:
    return Embed(color=Color.orange(), **kwargs)
    