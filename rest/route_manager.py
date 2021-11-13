from rest import route_builder

class APIRouteManager:
    def __init__(self, client=None):
        self.client = client

    @property
    def api(self):
        return route_builder.APIRouteBuilder("https://api.rec.net/api/")

    @property
    def rooms(self):
        return route_builder.APIRouteBuilder("https://rooms.rec.net/")

    @property
    def accounts(self):
        return route_builder.APIRouteBuilder("https://accounts.rec.net/")
