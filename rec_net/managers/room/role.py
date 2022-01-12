from attr import dataclass
from ..account import User

@dataclass
class Role:

    account: int or User
    role: str
    last_change_by_account: int
    invited_role: int

    @classmethod
    def from_data(cls, data):
        if isinstance(data, list): return [*map(Role.from_data, data)]
        role = data["Role"]
        role_id = data["Role"]
        if role_id == 255: role = "owner"
        if role_id == 30: role = "co-owner"
        if role_id == 20: role =  "moderator"
        if role_id == 10: role = "host"
        return cls(
            account = data["AccountId"],    
            role = role,
            last_change_by_account = data["LastChangedByAccountId"],
            invited_role = data["InvitedRole"]
        )
 