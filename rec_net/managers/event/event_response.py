from attr import dataclass
from ...helpers import date_to_unix

@dataclass
class EventResponse:
    id: int
    player: int
    created_at: int
    state: str

    @classmethod
    def from_data(cls, data):
        if isinstance(data, list): return [*map(EventResponse.from_data, data)]
        type = data["Type"]
        if type == 0: state = "accepted"
        if type == 1: state = "may attend"
        if type == 2: state = "not attending"
        created_at = date_to_unix(data["CreatedAt"])
        return cls(
            id = data["PlayerEventResponseId"],
            player = data["PlayerId"],
            created_at = created_at,
            state = state
        )