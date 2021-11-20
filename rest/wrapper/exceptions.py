class Error(Exception):
    """Base class for other exceptions"""
    pass

class AccountIdMissing(Error):
    """Raised when trying to access the account id without it being defined"""
    pass

class UsernameMissing(Error):
    """Raised when trying to access the account id without it being defined"""
    pass

class AccountNotFound(Error):
    """Raised when an account couldn't be found"""
    pass