from .image import Image
from ..base import BaseManager

class ImageManager(BaseManager):
    def __init__(self, client):
        return super().__init__(client, Image)

    async def build_dataclass(self, config, **options):
        (config
            .include_comments(options.get("include_comments", False), **options.get("comments_options", {}))
            .include_cheers(options.get("include_cheers", False), **options.get("cheers_options", {}))
            .resolve_creator(options.get("resolve_creator", False), **options.get("creator_options", {}))
            .resolve_room(options.get("resolve_room", False), **options.get("room_options", {}))
            .resolve_event(options.get("resolve_event", False), **options.get("event_options", {}))
        )
        return await config.build()

    async def get_data(self, image, type):
        pass

    async def get_comments(self, image, **options):
        pass

    async def get_cheers(self, image, **options):
        pass

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
