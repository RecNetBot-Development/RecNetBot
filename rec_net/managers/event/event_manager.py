from .event import Event
from .event_response import EventResponse
from ..base import BaseManager

class EventManager(BaseManager):
    def __init__(self, client):
        super().__init__(client, Event)
        self.configurables = {
            "responses": self.get_responses,
            "images": self.get_images,
            "respondents": self.resolve_respondents,
            "room": self.resolve_room,
            "creator": self.resolve_creator
        }

    @BaseManager.data_method
    async def get_data(self, id, type):
        return {
            "bulk": self.rec_net.api.playerevents.v1.bulk.post(),
            "id": self.rec_net.api.playerevents.v1(id).get()
        }

    @BaseManager.get_method("responses")
    async def get_responses(self, event, **options):
        resp = await self.rec_net.api.playerevents.v1(id).get().fetch()
        responses = EventResponse.from_data(resp.data)
        return responses

    @BaseManager.get_method("images", "image")
    async def get_images(self, id, **options):
        params = {}
        params["take"] = options.pop("take", 64)
        params["skip"] = options.pop("skip", 0)
        params["sort"] = options.pop("sort", 0)
        resp = await self.rec_net.api.images.v1.playerevent(id).get(params=params).fetch()
        return resp.data
        

    async def resolve_respondents(self, event, **options):
        pass

    @BaseManager.resolve_method("room", "room")
    async def resolve_room(self, event, **options):
        if isinstance(event.room, int): return event.room
        return None
        

    @BaseManager.resolve_method("creator", "account")
    async def resolve_creator(self, event, **options):
        if isinstance(event.creator, int): return event.creator
        return None
