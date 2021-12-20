from ..base import Options

class RoomOptions(Options):
    def __init__(self, *args):
        super().__init__(*args)
        self.configurables = {
            "include_images": self.manager.get_images,
            "include_events": self.manager.get_events,
            "resolve_creator": self.manager.resolve_creator,
            "resolve_roles": self.manager.resolve_roles,
        }