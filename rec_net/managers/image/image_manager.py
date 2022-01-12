from .image import Image
from ..base import BaseManager
from ...rest import run_in_queue

class ImageManager(BaseManager):
    def __init__(self, client):
        super().__init__(client, Image)
        self.configurables = {
            "cheers": self.get_cheers,
            "comments": self.get_comments,
            "creator": self.resolve_creator,
            "room": self.resolve_room,
            "event": self.resolve_event
        }

    @BaseManager.data_method
    async def get_data(self, image, type):
        pass

    async def get_comments(self, image, **options):
        pass

    @BaseManager.get_method("cheers", "account", "id")
    async def get_cheers(self, id, **options):
        image = options.pop("data_object")
        if image.cheer_count == 0:
            return []
        resp = await self.rec_net.api.images.v1(id).cheers.get().fetch()
        return resp.data

    async def resolve_creator(self, image, **options):
        pass
    
    async def resolve_room(self, image, **options):
        pass

    async def resolve_event(self, image, **options):
        pass

    async def resolve_commenters(self, image, **options):
        pass

    async def resolve_cheers(self, image, **options):
        pass
