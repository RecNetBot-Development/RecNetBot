from embeds import get_default_embed
from .RNBException import RNBException

class InvalidURL(RNBException):
    """
    Exception for when a user pastes a url that isn't rec.net
    """
    
    def __init__(self, loc: str = "https://...rec.net", path: str = "/..."):
        em = get_default_embed()
        em.description = f"Please input a RecNet link! ({loc}{path})"
        
        super().__init__(
            message=em.description, 
            embed=em
        )