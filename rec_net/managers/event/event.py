from attr import dataclass, field
from .event_options import EventOptions
from ..base import BaseDataclass

@dataclass
class Event(BaseDataclass):
    
    @staticmethod
    def configure(manager, event):
        return EventOptions(manager, event)

    @classmethod
    def from_data(cls, data, **kwargs):
        return cls()
