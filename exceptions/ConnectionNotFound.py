from embeds import get_default_embed
from resources import get_icon
from .RNBException import RNBException

class ConnectionNotFound(RNBException):
    """
    Exception for when someone hasn't linked their RR account
    """
    
    def __init__(self, is_self: bool = True):
        em = get_default_embed()
        
        if is_self:
            em.description = "**You didn't fill out the** `username` **option!**" \
                             "\n\nP.S. You can verify your Rec Room account to autofill the `username` slot! Get started with {}."
            em.set_image(url=get_icon("verify_command"))
        else:
            em.description = "This Discord user hasn't verified their Rec Room account!"
        
        em.set_thumbnail(url=get_icon("helpful"))
        
        super().__init__(
            message=em.description, 
            embed=em
        )