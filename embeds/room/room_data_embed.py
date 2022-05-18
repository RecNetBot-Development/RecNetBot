from discord import Embed
from utility.image.finalize_embed import finalize_embed
from embeds.data_embed import data_embed

formatting = {}

def room_data_embed(room_data, explanations=False):
    return data_embed(formatting, room_data, explanations)