from .event import Event
from ..base import BaseManager

class EventManager(BaseManager):
    def __init__(self, client):
        return super().__init__(client, Event)

    async def build_dataclass(self, config, **options):
        (config
            .include_responses(options.get("include_responses", False), **options.get("responses_options", {}))
            .include_images(options.get("include_images", False), **options.get("images_options", {}))
            .resolve_room(options.get("resolve_room", False), **options.get("room_options", {}))
            .resolve_creator(options.get("resolve_creator", False), **options.get("creator_options", {}))
        )
        return await config.build()

    async def get_data(self, event, type):
        pass

    async def get_responses(self, event, **options):
        pass

    async def get_images(self, event, **options):
        pass

    async def resolve_respondents(self, event, **options):
        pass

    async def resolve_room(self, event, **options):
        pass

    async def resolve_creator(self, event, **options):
        pass
