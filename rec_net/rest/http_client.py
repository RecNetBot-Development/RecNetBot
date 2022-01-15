import aiohttp
import asyncio
from .response import Response

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
            if ResponseData.success:
                return ResponseData
            print(ResponseData)
            #Possibly make these request more detailed (low priority addition)
            if ResponseData.status >= 400 and ResponseData.status < 500:
                pass 
            if ResponseData.status >= 500:
                pass
    async def close(self):
        await self.__session.close()
