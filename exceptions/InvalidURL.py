from embeds import get_default_embed
from .RNBException import RNBException

class InvalidURL(RNBException):
    """
    Exception for when a user pastes a url that isn't rec.net
    """
    
    def __init__(self, path = "/..."):
        em = get_default_embed()
        em.description = f"Please input a RecNet link! (https://rec.net{path})"
        
        super().__init__(
            message=em.description, 
            embed=em
        )