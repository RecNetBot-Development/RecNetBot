from embeds import get_default_embed
from .RNBException import RNBException

class ConnectionAlreadyDone(RNBException):
    """
    Exception for when someone tries to link to an already linked RR account
    """
    
    def __init__(self):
        em = get_default_embed()
        em.description = "This Rec Room account is already linked to someone!"
        
        super().__init__(
            message=em.description, 
            embed=em
        )