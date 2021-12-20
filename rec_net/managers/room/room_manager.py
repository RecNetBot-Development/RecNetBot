from .room import Room
from ..base import BaseManager

class RoomManager(BaseManager):
    def __init__(self, client):
        return super().__init__(client, Room)

    async def build_dataclass(self, config, **options):
        (config
            .include_images(options.get("include_images", False), **options.get("images_options", {}))
            .include_events(options.get("include_events", False), **options.get("events_options", {}))
            .resolve_creator(options.get("resolve_creator", False), **options.get("creator_options", {}))
            .resolve_roles(options.get("resolve_roles", False), **options.get("roles_options", {}))
        )
        return await config.build()

    async def get_data(self, room, type):
        pass
    
    async def get_images(self, room, **options):
        pass

    async def get_events(self, room, **options):
        pass

    async def resolve_creator(self, room, **options):
        pass

    async def resolve_roles(self, room, **options):
        pass


