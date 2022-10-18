from embeds import get_default_embed
from .RNBException import RNBException

class ImagesNotFound(RNBException):
    """
    Exception for when a user searches for images that doesn't exist
    """
    
    def __init__(self):
        em = get_default_embed()
        em.description = "Could not find any images based on your search!"
        
        super().__init__(
            message=em.description, 
            embed=em
        )