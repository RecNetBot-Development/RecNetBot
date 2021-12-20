class Error(Exception):
    """Base class for other exceptions"""
    ...

"""ACCOUNTS"""
class AccountDetailsMissing(Error):
    """Raised when trying to get an account without details"""
    ...

class AccountNotFound(Error):
    """Raised when an account couldn't be found"""
    ...

"""IMAGES"""
class ImageDetailsMissing(Error):
    """Raised when trying to get a post without details"""
    ...

class ImageNotFound(Error):
    """Raised when a post couldn't be found"""
    ...

"""REQUESTOR"""
class APIFailure(Error):
    def __init__(self, res):
        self._response = res
        super().__init__(
            f"""
            Failed to send request to RecNet!
            Method: '{self._method}'
            Path: '{self._path}'
            Params: '{self._params}'
            Data: '{self._data}'
            """
            )