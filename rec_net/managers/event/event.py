from attr import dataclass, field
from ...helpers import date_to_unix
from ..base import BaseDataclass

@dataclass
class Event(BaseDataclass):
    
    id: int
    creator: int
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
    responses: list = field(default=None)
    images: list = field(default=None)


    @classmethod
    def from_data(cls, data, **kwargs):
        if isinstance(data, list): return [*map(Event.from_data, data)]
        start_time =  date_to_unix(data["StartTime"])
        end_time =  date_to_unix(data["EndTime"])
        return cls(
            id = data["PlayerEventId"],
            creator = data["CreatorPlayerId"],
            name = data["Name"],
            description = data["Description"],
            image_name = data["ImageName"],
            start_time = start_time,
            end_time = end_time,
            attendee_count = data["AttendeeCount"],
            room = data["RoomId"],
            subroom_id = data["SubRoomId"],
            state = data["State"],
            accessibility = data["Accessibility"]
        )
