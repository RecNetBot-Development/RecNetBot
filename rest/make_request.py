import asyncio
import aiohttp

from rest import helpers

class APIRequest:
    def __init__(self, path, method, params=None, data=None):
        self._path = path
        self._method = method
        self._params = params

        if data is type(dict):
            data = helpers.data_to_multidict(data)

        self._data = data
        self.data = asyncio.create_task(self.make_request())


    async def make_request(self):
        async with aiohttp.request(method=self._method, url=self._path, params=self._params, data=self._data) as response:
            if response.ok:
                data = await response.json()
                return data
            else:
                return None
