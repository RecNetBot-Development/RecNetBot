from ..dataclasses import Image
from .exceptions import *

class ImageManager:
    def __init__(
        self, 
        rn,
        client,
        image_id: list or int = None,
        image_data: list or dict = None
        ):

        self.rn = rn
        self.client = client
        self.image_id = image_id
        self.image_data = image_data

    async def get_image(self):
        if self.image_data: 
            if type(self.image_data) is dict:
                image_data = [self.image_data]
            else:
                image_data = self.image_data
        else:
            image_data = await self.get_image_data()

        bulk = []
        for index, image in enumerate(image_data):
            image_id = image['Id']
            image = self.create_image_dataclass(
                image_data = image
            )  # Create the dataclass
            bulk.append(image)

        if len(bulk) == 1: return bulk[0]  # If only 1 image, only return it
        return bulk  # Otherwise the whole bulk

    async def get_image_data(self):
        try:
            if self.image_id is not None:  # 0 is falsy, so this prevents issues if user inputs 0
                resp = await self.rn.api.images.v3.post({"id": self.image_id}).response
                image_data = resp.data
            else:
                raise ImageDetailsMissing("Missing image details! Can't find a image without them.")
        except APIFailure:
            raise ImageNotFound("Couldn't find the image you were looking for!")

        return image_data

    def create_image_dataclass(self, image_data: dict):
        return Image(
            id=image_data['Id'],
            image_name=image_data['ImageName'],
            account_id=image_data['PlayerId'],
            tagged=image_data['TaggedPlayerIds'],
            room_id=image_data['RoomId'],
            event_id=image_data['PlayerEventId'],
            created_at=image_data['CreatedAt'],
            cheer_count=image_data['CheerCount'],
            comment_count=image_data['CommentCount']
        )
    