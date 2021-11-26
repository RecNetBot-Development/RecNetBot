from attr import dataclass

@dataclass
class Image:
    """Dataclass for a RN post."""
    id: int
    image_name: str
    account_id: int
    tagged: list
    room_id: int
    event_id: int
    created_at: str
    cheer_count: int
    comment_count: int
    cheers: list = None
    comments: list = None