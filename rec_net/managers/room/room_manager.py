from .room import Room
from ..base import BaseManager

class RoomManager(BaseManager):
    def __init__(self, client):
        super().__init__(client, Room)
        self.configurables = {
            "images": self.get_images,
            "events": self.get_events,
            "creator": self.resolve_creator,
            "roles": self.resolve_roles
        }

    async def create_builder(self, id = None, name = None, data = None, info = None, **kwargs):
        if data is None:
            data = await self.get_data(name, "name", info=info) if id is None else await self.get_data(id, "id", info=info)
        dataobject = await self._dataclass.from_data(data, **kwargs.pop("data", {}))
        return await self.build(dataobject, kwargs.pop("includes", []), kwargs.pop("options", {}))

    @BaseManager.data_method
    def get_data(self, id, info = None):
        include = 0
        if info is not None:
            if "subrooms" in info: include += 2
            if "roles" in info: include += 4
            if "tags" in info: include += 8
            if "promo" in info: include += 32
            if "scores" in info: include += 64
            if "loading screens" in info: include += 256
        return {
            "bulk": self.rec_net.rooms.rooms.bulk.post(),
            "name": self.rec_net.rooms.rooms.get(params={"name": id, "include": include}),
            "id": self.rec_net.rooms.rooms(id).get(params={"include": include})
        }
           
    @BaseManager.get_method("images", "image")
    async def get_images(self, id, **options):
        params = {}
        params["take"] = options.pop("take", 64)
        params["skip"] = options.pop("skip", 0)
        params["sort"] = options.pop("sort", 0)
        resp = await self.rec_net.api.images.v4.room(id).get(params=params).fetch()
        return resp.data

    @BaseManager.get_method("events", "event")
    async def get_events(self, id, **options):
        params = {}
        params["take"] = options.pop("take", 64)
        params["skip"] = options.pop("skip", 0)
        resp = await self.rec_net.api.playerevents.v1.room(id).fetch
        return resp.data

    @BaseManager.resolve_method("creator", "account")
    def resolve_creator(self, room, **options):
        if isinstance(room.creator, int): return room.creator
        return None

    async def resolve_roles(self, id, **options):
        pass


