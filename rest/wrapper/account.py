from rest import route_manager as route
from dataclasses import dataclass

class Account:
    def __init__(
        self, 
        rest_obj=route.APIRouteManager(),
        account_id: int = 0, 
        username: str = ""
        ):

        self.rn = rest_obj
        self.account_id = account_id
        self.username = username

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

    async def get_account_by_id(self):
        acc_data = await self.rn.accounts.account(self.account_id).get().data
        user = self.create_user_dataclass(acc_data)
        return user

    async def get_account_by_username(self):
        acc_data = await self.rn.accounts.account.get({"username": self.username}).data
        user = self.create_user_dataclass(acc_data)
        return user
        
    def create_user_dataclass(self, account_data: dict):
        return self.User(
            account_id=account_data['accountId'], 
            username=account_data['username'], 
            display_name=account_data['displayName'], 
            profile_image=account_data['profileImage'], 
            is_junior=account_data['isJunior'],
            platforms=account_data['platforms'],
            created_at=account_data['createdAt']
        )

"""Exceptions for the Account class"""
class Error(Exception):
    """Base class for other exceptions"""
    pass

class AccountIdMissing(Error):
    """Raised when trying to access the account id without it being defined"""
    pass

class UsernameMissing(Error):
    """Raised when trying to access the account id without it being defined"""
    pass

class AccountNotFound(Error):
    """Raised when an account couldn't be found"""
    pass