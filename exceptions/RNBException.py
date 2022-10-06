import discord

class RNBException(Exception):
    """
    Base exception for RNB invoked exceptions.
    """
    
    def __init__(self, message: str = "An error occurred.", embed: discord.Embed = None):
        super().__init__(message)
        self.embed = embed