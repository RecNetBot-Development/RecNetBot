import datetime
from discord import Colour

"""Adds finishing touches to embeds"""
def finalize_embed(em, set_author_footer=True, set_timestamp_footer=True):
    em.colour = Colour.orange()
    if not set_author_footer and not set_timestamp_footer: 
        return em
    
    if set_timestamp_footer: em.timestamp = datetime.datetime.now()
    return em