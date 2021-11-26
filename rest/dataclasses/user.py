from attr import dataclass
from scripts import date_to_unix

@dataclass
class User:
    """Dataclass for an RR account."""
    account_id: int
    username: str
    display_name: str
    profile_image: str
    is_junior: bool
    platforms: int
    created_at: str
    bio: str = None
    progression: dict = None
    subscriber_count: int = None
    posts: list = None
    feed: list = None

    @property
    def platform_names(self):
        if not self.platforms: return []
        chk_tuple = ('Steam', 'Oculus', 'PlayStation', 'Xbox', 'HeadlessBot', 'iOS', 'Android')
        platform_list, pos = [], 0
        while self.platforms:
            if self.platforms & 1:
                platform_list.append(chk_tuple[pos])
            pos += 1
            self.platforms >>= 1
        return platform_list

    @property
    def unix_created_at(self):
        return date_to_unix(self.created_at)