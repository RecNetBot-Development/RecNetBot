import aiohttp
import asyncio
from .response import Response
from ..exceptions import APIFailure

class HTTPClient():
    def __init__(self):
        self.__locks = {}
        self.__session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))

    async def push(self, Request):
        lock = self.__locks.get(Request.bucket)
        if lock is None:
            lock = asyncio.Lock()
            self.__locks[Request.bucket] = lock
        async with lock:
            return await self.execute(Request)

    async def execute(self, Request):
        kwargs = {}
        if Request.body is not None: kwargs["data"] = Request.body
        if Request.params is not None: kwargs["params"] = Request.params

        async with self.__session.request(Request.method, Request.url, **kwargs) as res:
            ResponseData = await Response.parse_response(res)
            return ResponseData
        
            if ResponseData.status == 401:
                return None
            if not ResponseData.status == 200: 
                raise APIFailure(ResponseData, Request)
            
            return ResponseData
        
    async def close(self):
        await self.__session.close()
