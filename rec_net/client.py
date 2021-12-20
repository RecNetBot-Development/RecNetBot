from .rest import APIRouteManager
from .managers import AccountManager, EventManager, ImageManager, RoomManager

class Client:
    def __init__(self):
        self.rec_net = APIRouteManager()
        self.accounts = AccountManager(self)
        self.events = EventManager(self)
        self.images = ImageManager(self)
        self.rooms = RoomManager(self)

    async def account(self, *args, **kwargs):
        return await self.accounts.create_builder(*args, **kwargs)

    async def event(self, *args, **kwargs):
        return await self.events.create_builder(*args, **kwargs)

    async def image(self, *args, **kwargs):
        return await self.images.create_builder(*args, **kwargs)

    async def room(self, *args, **kwargs):
        return await self.rooms.create_builder(*args, **kwargs)

    async def end(self):
        await self.rec_net.terminate()