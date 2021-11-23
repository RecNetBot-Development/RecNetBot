from discord.ext import commands

class Error(Exception):
    """Base class for other exceptions"""
    ...

class AccountDetailsMissing(Error):
    """Raised when trying to get an account without details"""
    ...

class AccountNotFound(Error):
    """Raised when an account couldn't be found"""
    ...

class APIFailure(Error):
    """Raised when request fails"""
    ...