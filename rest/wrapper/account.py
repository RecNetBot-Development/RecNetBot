from ..dataclasses import User, Progression
from .exceptions import *
from ..helpers import split_bulk
from scripts import remove_dupes_from_list

class AccountManager:
    def __init__(
        self, 
        rec_net,
        client,
        account_id: int or list = None, 
        username: str = None,
        include_bio: bool = False,
        include_progression: bool = False,
        include_subscriber_count: bool = False,
        include_posts: bool = False,
        include_feed: bool = False
        ):

        self.rec_net = rec_net
        self.client = client
        self.account_id = account_id
        self.username = username
        self.include_bio = include_bio
        self.include_progression = include_progression
        self.include_subscriber_count = include_subscriber_count
        self.include_posts = include_posts
        self.include_feed = include_feed

    """Used to get the user dataclass."""
    async def get_user(self):
        acc_data = await self.get_account_data()
        #if len(acc_data) == 1: self.account_id = acc_data[0]['accountId']
        bulk = []

        if self.include_progression:  # Fetch progression if wanted
            progression = await self.get_account_progression(self.account_id)

        for index, account in enumerate(acc_data):
            kwargs = {}
            account_id = account['accountId']

            if self.include_progression:  # If lvl & xp are wanted
                kwargs["progression"] = progression[index]

            if self.include_bio:  # If bio is wanted
                kwargs["bio"] = await self.get_account_bio(account_id)

            if self.include_subscriber_count:  # If subscriber count is wanted
                kwargs["subscriber_count"] = await self.get_account_subscriber_count(account_id)

            if self.include_posts:  # If posts are wanted
                post_data = await self.get_account_posts(account_id)
                kwargs["posts"] = post_data

            if self.include_feed:  # If feed is wanted
                feed_data = await self.get_account_feed(account_id)
                kwargs["feed"] = feed_data

            user = User.from_data(acc_data[index], **kwargs)  # Create the dataclass
            bulk.append(user)

        if len(bulk) == 1: return bulk[0]  # If only 1 account, only return it
        return bulk  # Otherwise the whole bulk

    async def get_account_data(self):
        try:
            if self.account_id is not None:  # 0 is falsy, so this prevents issues if user inputs 0
                if type(self.account_id) is list and len(self.account_id) > 150:  # If over bulk limit
                    bulk = remove_dupes_from_list(self.account_id)
                    split_groups = split_bulk(bulk)

                    acc_data = []
                    for id_group in split_groups:
                        resp = await self.rec_net.accounts.account.bulk.get({"id": id_group}).fetch()
                        acc_data += resp.data
                else:
                    resp = await self.rec_net.accounts.account.bulk.get({"id": self.account_id}).fetch()
                    acc_data = resp.data
            elif self.username:
                resp = await self.rec_net.accounts.account.get({"username": self.username}).fetch()
                acc_data = [resp.data]
            else:
                raise AccountDetailsMissing("Missing account details! Can't find an account without them.")
        except APIFailure:
            raise AccountNotFound("Couldn't find the account you were looking for!")

        return acc_data

    async def get_account_bio(self, acc_id=None):
        if not acc_id: acc_id = self.account_id
        resp = await self.rec_net.accounts.account(acc_id).bio.get().fetch()
        bio = resp.data['bio']
        return bio

    async def get_account_progression(self, acc_id=None):
        if not acc_id: acc_id = self.account_id
        if type(acc_id) is not list: acc_id = [acc_id]  # Turn to list for bulk
        resp = await self.rec_net.api.players.v2.progression.bulk.get({"id": acc_id}).fetch()
        data = resp.data

        bulk = []
        for account in data:
            progression = Progression(account['XP'], account['Level'])
            bulk.append(progression)
        return bulk

    async def get_account_subscriber_count(self, acc_id=None): 
        if not acc_id: acc_id = self.account_id
        resp = await self.rec_net.clubs.subscription.subscriberCount(acc_id).get().fetch()
        subscriber_count = resp.data
        return subscriber_count

    async def get_account_posts(self, acc_id=None): 
        if not acc_id: acc_id = self.account_id
        resp = await self.rec_net.api.images.v4.player(acc_id).get({"take": 9999999}).fetch()
        posts = await self.client.image(image_data=resp.data, fetch_tagged_users=True).get_image()
        return posts

    async def get_account_feed(self, acc_id=None): 
        if not acc_id: acc_id = self.account_id
        resp = await self.rec_net.api.images.v3.feed.player(acc_id).get({"take": 9999999}).fetch()
        feed = await self.client.image(image_data=resp.data, fetch_tagged_users=True).get_image()
        return feed