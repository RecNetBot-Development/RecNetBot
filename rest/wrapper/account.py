from dataclasses import dataclass
from .exceptions import *

class Account:
    def __init__(
        self, 
        rn_client,
        account_id: int = None, 
        username: str = None,
        include_bio: bool = False
        ):

        self.rn = rn_client
        self.account_id = account_id
        self.username = username
        self.include_bio = include_bio

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

        @property
        def platform_names(self):
            chk_tuple = ('Steam', 'Oculus', 'PlayStation', 'Xbox', 'HeadlessBot', 'iOS', 'Android')
            platform_list, pos = [], 0
            while self.platforms:
                if self.platforms & 1:
                    platform_list.append(chk_tuple[pos])
                pos += 1
                self.platforms >>= 1
            return platform_list

    async def get_account_by_id(self):
        if self.account_id == None:  # None instead of 'not (variable)' so if user inputs 0, it won't fail because 0 is falsy
            raise AccountIdMissing("Please include an account id in the 'Account' class arguments.")
        return await self.get_account_data(self.account_id)

    async def get_account_by_username(self):
        assert self.username, UsernameMissing("Please include a username in the 'Account' class arguments.")
        return await self.get_account_data(self.username)

    async def get_account_data(self, _account):
        if type(_account) is int:  # If it's an account id
            acc_data = await self.rn.accounts.account(_account).get().data
        else:  # If username
            acc_data = await self.rn.accounts.account.get({"username": _account}).data

        user = self.create_user_dataclass(acc_data)  # Create the dataclass

        if self.include_bio:  # If bio is wanted
            bio_response = await self.rn.accounts.account(user.account_id).bio.get().data
            user.bio = bio_response['bio']
        
        return user

    async def get_account_bio(self):
        if self.account_id == None:  # None instead of 'not (variable)' so if user inputs 0, it won't fail because 0 is falsy
            raise AccountIdMissing("Please include an account id in the 'Account' class arguments.")
        acc_data = await self.rn.accounts.account(self.account_id).get().data
        user = self.create_user_dataclass(acc_data)
        return user

    def create_user_dataclass(self, account_data: dict):
        try:
            return self.User(
                account_id=account_data['accountId'], 
                username=account_data['username'], 
                display_name=account_data['displayName'], 
                profile_image=account_data['profileImage'], 
                is_junior=account_data['isJunior'],
                platforms=account_data['platforms'],
                created_at=account_data['createdAt']
            )
        except KeyError:
            raise AccountNotFound("Couldn't find the account you were looking for!")