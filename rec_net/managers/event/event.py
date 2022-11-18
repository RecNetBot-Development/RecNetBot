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
    is_multi_instance: bool
    supports_live_chat: bool
    responses: list = field(default=None)
    images: list = field(default=None)

    @classmethod
    def from_data(cls, data, **kwargs):
        if isinstance(data, list): return [*map(Event.from_data, data)]
        raw_start_time = data.get("StartTime")
        raw_end_time = data.get("EndTime")
        if raw_start_time:
            start_time =  date_to_unix(raw_start_time)
        else:
            start_time = 0
        if raw_end_time:
            end_time =  date_to_unix(raw_end_time)
        else:
            end_time = 0
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
            accessibility = data["Accessibility"],
            is_multi_instance = bool(data["IsMultiInstance"]),
            supports_live_chat = bool(data["SupportMultiInstanceRoomChat"])
        )
