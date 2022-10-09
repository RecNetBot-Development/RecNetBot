from embeds import get_default_embed
from .RNBException import RNBException

class EventNotFound(RNBException):
    """
    Exception for when a user searches for a RR event that doesn't exist
    """
    
    def __init__(self):
        em = get_default_embed()
        em.description = "Could not find the Rec Room event you were looking for."
        
        super().__init__(
            message=em.description, 
            embed=em
        )