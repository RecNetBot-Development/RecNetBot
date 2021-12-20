from ..base import Options

class EventOptions(Options):
    def __init__(self, *args):
        super().__init__(*args)
        self.configurables = {
            "include_respondents": self.manager.get_respondents,
            "include_images": self.manager.get_images,
            "resolve_room": self.manager.resolve_room,
            "resolve_creator": self.manager.resolve_creator
        }