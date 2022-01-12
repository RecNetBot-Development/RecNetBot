from attr import dataclass, field
from .event_options import EventOptions
from ..base import BaseDataclass

@dataclass
class Event(BaseDataclass):
    
    id: int
    name: str
    description: str
    image_name: str
    start_time: int
    end_time: int
    attendee_count: int
    room: int
    subroom_id: int
    state: int
    accessibility: int
    responses: dict = field(default=None)


    @classmethod
    def from_data(cls, data, **kwargs):
        return cls()
