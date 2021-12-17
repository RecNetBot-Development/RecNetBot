import asyncio
import aiohttp
from rest import helpers
from .dataclasses import Response
from .wrapper.exceptions import APIFailure

class APIRequest:
    def __init__(self, client, path, method, params=None, data=None):
        self.url = path
        self.method = method
        self.params = params
        self._client = client

        if data is type(dict):
            data = helpers.data_to_multidict(data)

        self.body = data

    async def fetch(self):
        return await self._client.push(self)

    @property
    def bucket(self):
        return f"{self.url}:{self.params}:{self.body}"


