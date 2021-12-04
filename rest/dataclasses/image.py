from scripts import date_to_unix
from attr import dataclass, field

@dataclass
class Image:
    """Dataclass for a RN post."""
    id: int
    image_name: str
    account_id: int
    tagged: list
    room_id: int
    event_id: int
    created_at: int
    cheer_count: int
    comment_count: int
    cheers: list = field(default=None)
    comments: list = field(default=None)

    @classmethod
    def from_data(cls, data, **kwargs):
        created_at = date_to_unix(data['CreatedAt'])
        return cls(
            data["Id"],
            data["ImageName"],
            data["PlayerId"],
            data["TaggedPlayerIds"],
            data["RoomId"],
            data["PlayerEventId"], 
            created_at, 
            data["CheerCount"], 
            data["CommentCount"], 
            **kwargs
        )