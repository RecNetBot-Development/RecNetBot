from scripts import date_to_unix
from attr import dataclass, field
from .image_options import ImageOptions
from ..base import BaseDataclass

@dataclass
class Image(BaseDataclass):
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
    user: int = field(default=None)
    tagged_users: list = field(default=None)

    @staticmethod
    def configure(manager, event):
        return ImageOptions(manager, event)

    @classmethod
    def from_data(cls, data, **kwargs):
        if isinstance(data, list): return [*map(Image.from_data, data)]
        created_at = date_to_unix(data['CreatedAt'])
        return cls(
            id=data["Id"],
            image_name=data["ImageName"],
            account_id=data["PlayerId"],
            tagged=data["TaggedPlayerIds"],
            room_id=data["RoomId"],
            event_id=data["PlayerEventId"], 
            created_at=created_at, 
            cheer_count=data["CheerCount"], 
            comment_count=data["CommentCount"],
            cheers=None,
            comments=None,
            user=None,
            tagged_users=data['TaggedUsers'] if "TaggedUsers" in data else None,
            **kwargs
        )