from rest import route_manager as route
from .account import Account

class Client:
    def __init__(
        self, 
        route_manager=route.APIRouteManager()
        ):
        self.rn = route_manager

    def account(self, *args, **kwargs):
        return Account(rn_client=self.rn, *args, **kwargs)
