from .progression import Progression
from attr import dataclass, field
from scripts import date_to_unix
from ..base import BaseDataclass
from .account_options import AccountOptions

def resolve_platforms(x):
    platforms = ['Steam', 'Oculus', 'PlayStation', 'Xbox', 'HeadlessBot', 'iOS', 'Android']
    for index, platform in enumerate(platforms):
        if 1 << index & x:
            yield platform

@dataclass
class User(BaseDataclass):
    """Dataclass for an RR account."""
    id: int
    username: str
    display_name: str
    profile_image: str
    is_junior: bool
    platforms: list
    created_at: int
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
        return cls(
            data["accountId"],
            data["username"],
            data["displayName"],
            data["profileImage"],
            data["isJunior"],
            platforms,
            created_at, 
            **kwargs
        )
