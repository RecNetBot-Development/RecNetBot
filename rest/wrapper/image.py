from ..helpers import split_bulk
from ..dataclasses import Image
from .exceptions import *

class ImageManager:
    def __init__(
        self, 
        rec_net,
        client,
        image_id: list or int = None,
        image_data: list or dict = None,
        fetch_tagged_users: bool = False
        ):

        self.rec_net = rec_net
        self.client = client
        self.image_id = image_id
        self.image_data = image_data
        self.fetch_tagged_users = fetch_tagged_users

    async def get_image(self):
        if self.image_data:  # Prioritize pure image data
            if type(self.image_data) is dict:  # if it's a single image's data
                image_data = [self.image_data]
            else:  # if it's a list of image data
                image_data = self.image_data
        else:  # Fetch images
            image_data = await self.get_image_data()

        if self.fetch_tagged_users:  # If tagged users wanted
            """I'm sure this could all be made much more optimal, but at least it works for now"""

            # Get all of the tagged account's ids for a bulk fetch
            tagged_ids = []
            for image in image_data:  
                for account_id in image['TaggedPlayerIds']:
                    if account_id not in tagged_ids: tagged_ids.append(account_id)

            # If any were found, fetch them
            tagged_users = {}
            if tagged_ids:
                users = await self.client.account(account_id=tagged_ids).get_user()
                for user in users: tagged_users[user.account_id] = user  # Assign users on a dictionary
                
                # Replace tagged account ids with user dataclasses
                for data_index in range(len(image_data)):
                    image_data[data_index]['TaggedUsers'] = []
                    if not image_data[data_index]['TaggedPlayerIds']: continue  # Don't bother with below if nobody tagged
                    for account_id in image_data[data_index]['TaggedPlayerIds']:   
                        if account_id in tagged_users:
                            image_data[data_index]['TaggedUsers'].append(tagged_users[account_id])

        bulk = []
        for index, image_data in enumerate(image_data):
            kwargs = {}
            image = Image.from_data(image_data, **kwargs)  # Create the dataclass
            bulk.append(image)

        if len(bulk) == 1: return bulk[0]  # If only 1 image, only return it
        return bulk  # Otherwise the whole bulk

    async def get_image_data(self):
        try:
            if self.image_id is not None:  # 0 is falsy, so this prevents issues if user inputs 0
                if type(self.account_id) is list and len(self.account_id) > 150:  # If over bulk limit
                    split_groups = split_bulk(self.account_id)

                    image_data = []
                    for id_group in split_groups:
                        resp = await self.rec_net.api.images.v3.post({"id": id_group}).fetch()
                        image_data += resp.data
                else:
                    resp = await self.rec_net.api.images.v3.post({"id": self.image_id}).fetch()
                image_data = resp.data
            else:
                raise ImageDetailsMissing("Missing image details! Can't find a image without them.")
        except APIFailure:
            raise ImageNotFound("Couldn't find the image you were looking for!")

        return image_data
    