from .user import User
from ..base import BaseManager
from ...rest import run_in_queue

class AccountManager(BaseManager):
    def __init__(self, client):
        super().__init__(client, User)
        self.configurables = {
            "bio": self.get_bio,
            "progress": self.get_progress,
            "subs": self.get_subscriber_count,
            "feed": self.get_feed,
            "posts": self.get_posts,
            "owned_rooms": self.get_owned_rooms,
            "created_rooms": self.get_created_rooms,
            "room_showcase": self.get_room_showcase,
            "events": self.get_events,
        }

    @BaseManager.data_method
    def get_data(self, id):
        return {
            "bulk": self.rec_net.accounts.account.bulk.post(),
            "name": self.rec_net.accounts.account.get(params={"username": id}),
            "id": self.rec_net.accounts.account(id).get()
        }

    @BaseManager.bulk_get_method("level", data_key = "Level")
    def get_progress(self):
        return self.rec_net.api.players.v2.progression.bulk.post()

    @BaseManager.get_method("bio")
    async def get_bio(self, id, **options):
        resp = await self.rec_net.accounts.account(id).bio.get().fetch()
        return resp.data["bio"]

    @BaseManager.get_method("subscriber_count")
    async def get_subscriber_count(self, id, **options):
        resp = await self.rec_net.clubs.subscription.subscriberCount(id).get().fetch()
        return resp.data

    @BaseManager.get_method("feed", "image")
    async def get_feed(self, id, **options):
        resp = await self.rec_net.api.images.v3.feed.player(id).get().fetch()
        return resp.data

    @BaseManager.get_method("posts", "image")
    async def get_posts(self, id, **options):
        params = {}
        params["take"] = options.pop("take", 64)
        params["skip"] = options.pop("skip", 0)
        resp = await self.rec_net.api.images.v4.player(id).get(params=params).fetch()
        return resp.data

    @BaseManager.get_method("owned_rooms", "room")
    async def get_owned_rooms(self, id, **options):
        resp = await self.rec_net.rooms.rooms.ownedby(id).get().fetch()
        return resp.data

    @BaseManager.get_method("created_rooms", "room")
    async def get_created_rooms(self, id, **options):
        resp = await self.rec_net.rooms.rooms.createdby(id).get().fetch()
        return resp.data

    @BaseManager.get_method("room_showcase", "room", "id")
    async def get_room_showcase(self, id, **options):
        resp = await self.rec_net.rooms.showcase(id).get().fetch()
        return resp.data

    @BaseManager.get_method("events", "event")
    async def get_events(self, id, **options):
        resp = await self.rec_net.api.playerevents.v1.creator(id).get().fetch()
        return resp.data


