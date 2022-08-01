from ..base import Options

class InventionOptions(Options):
    def __init__(self, *args):
        super().__init__(*args)
        self.configurables = {
            "include_creator": self.manager.get_creator,
            "include_room": self.manager.get_room
        }