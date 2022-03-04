from .progression import Progression
from attr import dataclass, field
from ...helpers import date_to_unix
from ..base import BaseDataclass
from .account_options import AccountOptions
from utility.account.resolve_platforms import resolve_platforms

@dataclass
class User(BaseDataclass):
    """Dataclass for an RR account."""
    id: int
    username: str
    display_name: str
    is_junior: bool
    platforms: list
    created_at: int
    profile_image: str
    banner_image: str = field(default=None)
    level: int = field(default=None)
    bio: str = field(default=None)
    progression: Progression = field(default=None)
    subscriber_count: int = field(default=None)
    posts: list = field(default=None)
    feed: list = field(default=None)

    @staticmethod
    def configure(manager, user):
        return AccountOptions(manager, user)

    @classmethod
    def from_data(cls, data, **kwargs):
        if isinstance(data, list): return [*map(User.from_data, data)]
        platforms = [platform for platform in resolve_platforms(data["platforms"])]
        created_at = date_to_unix(data['createdAt'])
        banner_image = data.get("bannerImage", None)
        return cls(
            id=data["accountId"],
            username=data["username"],
            display_name=data["displayName"],
            profile_image=data["profileImage"],
            banner_image=banner_image,
            is_junior=data["isJunior"],
            platforms=platforms,
            created_at=created_at, 
            **kwargs
        )
