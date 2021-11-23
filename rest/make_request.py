import asyncio
import aiohttp
from rest import helpers
from .dataclasses import Response
from .wrapper.exceptions import APIFailure

class APIRequest:
    def __init__(self, path, method, params=None, data=None):
        self._path = path
        self._method = method
        self._params = params

        if data is type(dict):
            data = helpers.data_to_multidict(data)

        self._data = data
        self.response = asyncio.create_task(self.make_request())

    async def make_request(self):
        async with aiohttp.request(method=self._method, url=self._path, params=self._params, data=self._data) as response:
            success = response.ok
            status_code = response.status
            if not success: raise APIFailure(
f"""
Failed to send request to RecNet!
Method: '{self._method}'
Path: '{self._path}'
Params: '{self._params}'
Data: '{self._data}'
"""
            )

            body = await response.json()
            
        return Response(status_code, success, body)


