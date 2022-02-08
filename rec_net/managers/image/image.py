from ...helpers import date_to_unix
from attr import dataclass, field
from .image_options import ImageOptions
from ..base import BaseDataclass

@dataclass
class Image(BaseDataclass):
    """Dataclass for a RN post."""
    id: int
    image_name: str
    creator: int
    tagged: list
    room: int
    event: int
    created_at: int
    cheer_count: int
    comment_count: int
    cheers: list = field(default=None)
    comments: list = field(default=None)

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
            creator=data["PlayerId"],
            tagged=data["TaggedPlayerIds"],
            room=data["RoomId"],
            event=data["PlayerEventId"], 
            created_at=created_at, 
            cheer_count=data["CheerCount"], 
            comment_count=data["CommentCount"],
        )