from embeds import get_default_embed
from .RNBException import RNBException

class ImageNotFound(RNBException):
    """
    Exception for when a user searches for a RR image that doesn't exist
    """
    
    def __init__(self, query: str = None):
        em = get_default_embed()
        em.description = "Could not find the Rec Room image you were looking for."
        
        if query:
            em.description += f"\n\nQuery: `{query}`"

        super().__init__(
            message=em.description, 
            embed=em
        )