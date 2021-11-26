from attr import dataclass, field
from scripts import date_to_unix

def reslove_platforms(x):
    platforms = ['Steam', 'Oculus', 'PlayStation', 'Xbox', 'HeadlessBot', 'iOS', 'Android']
    for index, platform in enumerate(platforms):
        if 1 << index & x:
            yield platform

@dataclass
class User:
    """Dataclass for an RR account."""
    account_id: int
    username: str
    display_name: str
    profile_image: str
    is_junior: bool
    platforms: list
    created_at: str
    bio: str = field(default=None)
    progression: dict = field(default=None)
    subscriber_count: int = field(default=None)
    posts: list = field(default=None)
    feed: list = field(default=None)

    @classmethod
    def from_data(cls, data, **kwargs):
        platforms = [platform for platform in reslove_platforms(data["platforms"])]
        return cls(data["accountId"],data["username"],data["displayName"],data["profileImage"],data["isJunior"],platforms,data['createdAt'], **kwargs)

    @property
    def unix_created_at(self):
        return date_to_unix(self.created_at)
