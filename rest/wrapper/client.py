from rest import route_manager as route
from .account import AccountManager
from .image import ImageManager

class Client:
    def __init__(
        self, 
        route_manager=route.APIRouteManager()
        ):
        self.rec_net = route_manager

    def account(self, *args, **kwargs):
        return AccountManager(rec_net=self.rec_net, client=self, *args, **kwargs)

    def image(self, *args, **kwargs):
        return ImageManager(rec_net=self.rec_net, client=self, *args, **kwargs)
