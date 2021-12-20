from ..base import Options

class ImageOptions(Options):
    def __init__(self, *args):
        super().__init__(*args)
        self.configurables = {
            "include_cheers": self.manager.get_cheers,
            "include_comments": self.manager.get_comments,
            "resolve_creator": self.manager.resolve_creator,
            "resolve_room": self.manager.resolve_room,
            "resolve_event": self.manager.resolve_event
        }