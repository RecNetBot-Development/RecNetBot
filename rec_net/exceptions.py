from utility.emojis import get_emoji

class Error(Exception):
    """Base class for other exceptions"""
    ...

class NotFound(Exception):
    """Raised when something couldn't be found"""
    def __init__(self, name):
        super().__init__(
            f"{name} not found! Make sure you spelled it right."
        )
        
class AccountNotFound(NotFound):
    def __init__(self, name = ""):
        self._name = f"`@{name}`"
        super().__init__(
            name=f"{get_emoji('username')} {self._name}" if name else 'User'
        )
        
class RoomNotFound(NotFound):
    def __init__(self, name = ""):
        self._name = f"`^{name}`"
        super().__init__(
            name=f"{get_emoji('room')} {self._name}" if name else 'Room'
        )
        
class ImageNotFound(NotFound):
    def __init__(self, name = ""):
        self._name = f"`{name}`"
        super().__init__(
            name=f"{get_emoji('image')} {self._name}" if name else 'Image'
        )
        
class EventNotFound(NotFound):
    def __init__(self, name = ""):
        self._name = f"`{name}`"
        super().__init__(
            name=f"{get_emoji('event')} {self._name}" if name else 'Event'
        )

class NoSharedPosts(Exception):
    def __init__(self):
        super().__init__(
            "User hasn't shared a single post!"
        )
        
class NoTaggedPosts(Exception):
    def __init__(self):
        super().__init__(
            "User hasn't been tagged in a single post!"
        )

class NameServerUnavailable(Exception):
    def __init__(self):
        super().__init__(
            "Name Server cannot be reached at this time!\nThe servers may be under maintenance."
        )

"""REQUESTOR"""
class APIFailure(Error):
    def __init__(self, res, req):
        self.response, self.request = res, req
        super().__init__(
            f"""
Failed to send request to RecNet! 
Status: {self.response.status}
URL: {self.request.url}
Method: {self.request.method}
Params: {self.request.params}
Body: {self.request.body}
Bucket: {self.request.bucket}
            """
        )