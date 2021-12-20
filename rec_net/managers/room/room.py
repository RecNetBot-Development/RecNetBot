from attr import dataclass, field
from .room_options import RoomOptions
from ..base import BaseDataclass

@dataclass
class Room(BaseDataclass):
    
    @staticmethod
    def configure(manager, event):
        return EventOptions(manager, event)

    @classmethod
    def from_data(cls, data, **kwargs):
        return cls()