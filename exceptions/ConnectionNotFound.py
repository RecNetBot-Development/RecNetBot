from embeds import get_default_embed
from .RNBException import RNBException

class ConnectionNotFound(RNBException):
    """
    Exception for when someone hasn't linked their RR account
    """
    
    def __init__(self):
        em = get_default_embed()
        em.description = "This Discord user hasn't linked their Rec Room account! </set_profile:1027713516095946842>"
        
        super().__init__(
            message=em.description, 
            embed=em
        )