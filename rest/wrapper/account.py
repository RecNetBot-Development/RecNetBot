from ..dataclasses import User
from .exceptions import *

class Account:
    def __init__(
        self, 
        rn_client,
        account_id: int = None, 
        username: str = None,
        include_bio: bool = False,
        include_progression: bool = False,
        include_subscribers: bool = False
        ):

        self.rn = rn_client
        self.account_id = account_id
        self.username = username
        self.include_bio = include_bio
        self.include_progression = include_progression
        self.include_subscribers = include_subscribers

    """Used to get the user dataclass."""
    async def get_user(self):
        acc_data = await self.get_account_data()
        self.account_id = acc_data['accountId']

        if self.include_bio:  # If bio is wanted
            bio = await self.get_account_bio()

        if self.include_progression:  # If lvl & xp are wanted
            progression = await self.get_account_progression()

        if self.include_subscribers:  # If subscriber count is wanted
            subscribers = await self.get_account_subscribers()

        user = self.create_user_dataclass(
            account_data = acc_data,
            bio = bio if self.include_bio else None,
            progression = progression if self.include_progression else None,
            subscribers = subscribers if self.include_subscribers else None
        )  # Create the dataclass
        return user

    async def get_account_data(self):
        try:
            if self.account_id is not None:  # 0 is falsy, so this prevents issues if user inputs 0
                resp = await self.rn.accounts.account(self.account_id).get().response
            elif self.username:
                resp = await self.rn.accounts.account.get({"username": self.username}).response
            else:
                raise AccountDetailsMissing("Missing account details! Can't find an account without them.")
        except APIFailure:
            raise AccountNotFound("Couldn't find the account you were looking for!")

        acc_data = resp.data
        return acc_data

    async def get_account_bio(self):
        resp = await self.rn.accounts.account(self.account_id).bio.get().response
        bio = resp.data['bio']
        return bio

    async def get_account_progression(self):
        resp = await self.rn.api.players.v2.progression.bulk.get({"id": [self.account_id]}).response
        data = resp.data
        progression = {
            "lvl": data[0]['Level'],
            "xp": data[0]['XP']
        }
        return progression

    async def get_account_subscribers(self): 
        resp = await self.rn.clubs.subscription.subscriberCount(self.account_id).get().response
        subscribers = resp.data
        return subscribers

    def create_user_dataclass(self, account_data: dict, bio: str = None, progression: dict = None, subscribers: int = None):
        return User(
            account_id=account_data['accountId'], 
            username=account_data['username'], 
            display_name=account_data['displayName'], 
            profile_image=account_data['profileImage'], 
            is_junior=account_data['isJunior'],
            platforms=account_data['platforms'],
            created_at=account_data['createdAt'],
            bio=bio,
            progression=progression,
            subscribers=subscribers
        )