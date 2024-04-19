import aiohttp
from .dataclass.cat import Cat, Breed
from typing import List, Optional

class CatAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = None
        self.cat_cache = []

    async def initialize(self) -> aiohttp.ClientSession:
        """Initialize the aiohttp client

        Returns:
            aiohttp.ClientSession: aiohttp client
        """
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

        self.client = aiohttp.ClientSession(headers=headers)
        return self.client
    

    async def favorite_cat(self, cat_id: str, user_id: int) -> Optional[int]:
        """Favorite a cat

        Args:
            cat_id (str): ID of the cat
            user_id (int): ID of the user who favorited

        Returns:
            id: Favorite ID if successful
        """

        data = {
            "image_id": cat_id,
            "sub_id": str(user_id)
        }

        async with self.client.post("https://api.thecatapi.com/v1/favourites", json=data) as resp:
            if resp.ok:
                data = await resp.json()
                return data.get("id", None)
            else:
                return None
        
    async def unfavorite_cat(self, favorite_id: int) -> bool:
        """Unfavorite a cat

        Args:
            favorite_id (int): ID of the favorite

        Returns:
            bool: success
        """

        async with self.client.delete(f"https://api.thecatapi.com/v1/favourites/{favorite_id}") as resp:
            return resp.ok

    async def get_favorite_cats(self, user_id: int) -> Optional[List[Cat]]:
        """Fetches an user's favorite cats

        Args:
            user_id (int): User ID

        Returns:
            List[Cat]: le cats :3
        """

        async with self.client.get(f"https://api.thecatapi.com/v1/favourites?sub_id={user_id}&order=DESC") as resp:
            if resp.ok:
                raw_cats = await resp.json()
            else:
                return [] 
                
        # Bake raw JSON cats into dataclasses :3
        dataclass_cats = []
        for i in raw_cats:
            dataclass_cats.append(self.raw_fav_cat_to_dataclass(i))

        return dataclass_cats

    async def get_cats(self, limit: int = 1) -> List[Cat]:
        """Cat distribution center

        Args:
            limit (int, optional): The amount of cats you want. Defaults to 1.

        Returns:
            List[Cat]: le cats :3
        """

        # Check if we have any cats left in our shelter
        if len(self.cat_cache) < limit:
            # Hunt more cats to distribute
            async with self.client.get("https://api.thecatapi.com/v1/images/search?limit=50") as resp:
                if resp.ok:
                    raw_cats = await resp.json()
                else:
                    return None
                
            # Bake raw JSON cats into dataclasses :3
            dataclass_cats = []
            for i in raw_cats:
                dataclass_cats.append(self.raw_cat_to_dataclass(i))

            # Add our newly baked cats into our shelter
            self.cat_cache += dataclass_cats

        # Distribute cats
        share_cats = self.cat_cache[:limit]

        # Take our distributed cats away from the shelter
        self.cat_cache = self.cat_cache[limit:]

        # Off you go!
        return share_cats

    def raw_cat_to_dataclass(self, raw_cat: dict) -> Cat:
        """Turns a JSON cat into a dataclass

        Args:
            raw_cat (dict): Raw JSON cat

        Returns:
            Cat: Cat dataclass
        """
        # Include breeds if any
        breeds = []
        if raw_cat['breeds']:
            for i in raw_cat['breeds']:
                breeds.append(
                    Breed(
                        name=i['name'],
                        description=i['description'],
                        temperament=i['temperament']
                    )
                )

        # Bake the cat into a dataclass
        return Cat(
            id=raw_cat['id'], 
            img_url=raw_cat['url'],
            breeds=breeds,
            favorite_id=None
        )
    
    def raw_fav_cat_to_dataclass(self, raw_cat: dict) -> Cat:
        """Turns a favorited JSON cat into a dataclass

        Args:
            raw_cat (dict): Raw JSON cat

        Returns:
            Cat: Cat dataclass
        """

        # Bake the cat into a dataclass
        return Cat(
            id=raw_cat['image']['id'], 
            img_url=raw_cat['image']['url'],
            breeds=[],
            favorite_id=raw_cat['id']
        )

    async def close(self) -> None:
        """Close the aiohttp client
        """
        await self.client.close()
