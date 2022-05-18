from .route_builder import APIRouteBuilder
from .http_client import HTTPClient

class APIRouteManager:
    def __init__(self, client=None):
        self.client = client
        self.http_client = HTTPClient()

    @property
    def api(self):
        return APIRouteBuilder(self, "https://api.rec.net/api/")

    @property
    def rooms(self):
        return APIRouteBuilder(self, "https://rooms.rec.net/")

    @property
    def accounts(self):
        return APIRouteBuilder(self, "https://accounts.rec.net/")

    @property
    def clubs(self):
        return APIRouteBuilder(self, "https://clubs.rec.net/")
    
    @property
    def cdn(self):
        return APIRouteBuilder(self, "https://cdn.rec.net/")
    
    @property
    def namespace(self):
        return APIRouteBuilder(self, "https://ns.rec.net/")
    
    def custom(self, host: str):
        return APIRouteBuilder(self, host)
    
    async def terminate(self):
        await self.http_client.close()