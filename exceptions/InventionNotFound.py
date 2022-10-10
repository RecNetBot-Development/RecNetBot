from embeds import get_default_embed
from .RNBException import RNBException

class InventionNotFound(RNBException):
    """
    Exception for when a user searches for a RR invention that doesn't exist
    """
    
    def __init__(self):
        em = get_default_embed()
        em.description = "Could not find the Rec Room invention you were looking for."
        
        super().__init__(
            message=em.description, 
            embed=em
        )