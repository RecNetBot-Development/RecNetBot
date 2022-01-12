from attr import dataclass

@dataclass
class EventResponse:

    id: int
    event: int
    player: int
    created_at: int
    state: str
