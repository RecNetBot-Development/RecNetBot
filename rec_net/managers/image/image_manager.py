from .image import Image
from .comment import Comment
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
        return {
            "bulk": self.rec_net.api.images.v3.bulk.post(),
            "id": self.rec_net.api.images.v4(id).get()
        }

    @BaseManager.get_method("comments")
    async def get_comments(self, id, **options):
        resp = await self.rec_net.api.images.v1(id).comments().get().fetch()
        return Comment.from_data(resp.data)

    @BaseManager.get_method("cheers", "account", "id")
    async def get_cheers(self, id, **options):
        image = options.pop("data_object")
        if image.cheer_count == 0:
            return []
        resp = await self.rec_net.api.images.v1(id).cheers.get().fetch()
        return resp.data

    @BaseManager.resolve_method("creator", "account")
    def resolve_creator(self, image, **options):
        if isinstance(image.creator, int): return image.creator
        return None
    
    @BaseManager.resolve_method("room", "room")
    async def resolve_room(self, image, **options):
        if isinstance(image.room, int): return image.room
        return None

    @BaseManager.resolve_method("event", "event")
    async def resolve_event(self, image, **options):
        if isinstance(image.event, int): return image.event
        return None

    async def resolve_commenters(self, image, **options):
        pass

