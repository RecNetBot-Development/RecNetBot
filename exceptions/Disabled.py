from embeds import get_default_embed
from .RNBException import RNBException
from resources import get_icon
from utils import load_config

config = load_config()

class Disabled(RNBException):
    """
    Exception for when a command has been disabled due to external reasons
    """
    
    def __init__(self):
        em = get_default_embed()
        em.title = "This command has been disabled."
        em.description = "Due to a breaking change in Rec Room's API, we were unfortunately forced to disable this command.\n\n" \
                         "We are working with Rec Room to attempt to restore functionality. We apologize for the inconvenience this causes.\n\n"
        
        if "server_link" in config:
            em.description += f"Feel free to voice your concerns in our [test server.]({config['server_link']})"

        em.set_thumbnail(url=get_icon("rectnet"))

        super().__init__(
            embed=em
        )