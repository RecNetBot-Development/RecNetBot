from ..base import Options

class InventionOptions(Options):
    def __init__(self, *args):
        super().__init__(*args)
        self.configurables = {
            "include_creator": self.manager.resolve_creator,
            "include_room": self.manager.resolve_room
        }