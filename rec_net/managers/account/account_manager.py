from .user import User
from ..base import BaseManager
from ...rest import run_in_queue


class AccountManager(BaseManager):
    def __init__(self, client):
        super().__init__(client, User)

    async def build_dataclass(self, config, **options):
        (config
            .include_bio(options.get("include_bio", False))
            .include_progress(options.get("include_progress", False))
            .include_subs(options.get("include_subs", False))
            .include_feed(options.get("include_feed", False), **options.get("feed_options", {}))
            .include_posts(options.get("include_posts", False), **options.get("posts_options", {}))
            .include_owned_rooms(options.get("include_owned_rooms", False), **options.get("owned_rooms_options", {}))
            .include_created_rooms(options.get("include_created_rooms", False), **options.get("created_rooms_options", {}))
            .include_room_showcase(options.get("include_room_showcase", False), **options.get("room_showcase_options", {}))
            .include_events(options.get("include_events", False), **options.get("events_options", {}))
        )
        return await config.build()

    async def get_data(self, user, type):
        if isinstance(user, list):
            return await self.handle_bulk(self.rec_net.accounts.account.bulk.post(), user, type)
        id = self.resolve_id(user)
        req = self.rec_net.accounts.account(id).get() if isinstance(user, int) else self.rec_net.accounts.account.get(params={"username": user})
        resp = await req.fetch()
        return resp.data

    async def get_progress(self, user):
        pass

    async def get_bio(self, user):
        if isinstance(user, list): return await run_in_queue(self.get_bio, user)
        id = self.resolve_id(user)
        resp = await self.rec_net.accounts.account(id).bio.get().fetch()
        return self.response(user, "bio", resp.data["bio"])

    async def get_subscriber_count(self, user):
        pass

    async def get_feed(self, user, **options):
        pass

    async def get_posts(self, user, **options):
        pass

    async def get_owned_rooms(self, user, **options):
        pass

    async def get_created_rooms(self, user, **options):
        pass

    async def get_room_showcase(self, user, **options):
        pass

    async def get_events(self, user, **options):
        pass

    async def resolve_showcase(self, user, **options):
        pass


