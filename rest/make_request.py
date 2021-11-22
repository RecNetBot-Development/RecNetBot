import asyncio
from os import stat
import aiohttp
from aiohttp.helpers import strip_auth_from_url
from attr import dataclass

from rest import helpers
from rest.wrapper.exceptions import AccountNotFound

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
                body = await response.json()
                status_code = response.status
                success = response.ok
        
        @dataclass
        class Response:
            status: int
            success: bool
            data: int | dict | str

        return Response(status_code, success, body)


