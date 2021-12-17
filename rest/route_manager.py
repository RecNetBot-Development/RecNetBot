from rest import route_builder, http_client

class APIRouteManager:
    def __init__(self, client=None):
        self.client = client
        self.http_client = http_client.HTTPClient()

    @property
    def api(self):
        return route_builder.APIRouteBuilder(self, "https://api.rec.net/api/")

    @property
    def rooms(self):
        return route_builder.APIRouteBuilder(self, "https://rooms.rec.net/")

    @property
    def accounts(self):
        return route_builder.APIRouteBuilder(self, "https://accounts.rec.net/")

    @property
    def clubs(self):
        return route_builder.APIRouteBuilder(self, "https://clubs.rec.net/")