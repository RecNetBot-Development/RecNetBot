from typing_extensions import runtime
from rest import route_manager as route
from .account import Account
from .image import Image

class Client:
    def __init__(
        self, 
        route_manager=route.APIRouteManager()
        ):
        self.rn = route_manager

    def account(self, *args, **kwargs):
        return Account(rn=self.rn, client=self, *args, **kwargs)

    def image(self, *args, **kwargs):
        return Image(rn=self.rn, client=self, *args, **kwargs)
