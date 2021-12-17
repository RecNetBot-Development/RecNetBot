import aiohttp
import asyncio
from rest.dataclasses import Response
from rest.wrapper import exceptions

async def parse_response(resonse):
    if "application/json" in resp.headers["Content-type"]:
        return await resp.json()
    return await resp.text()  

class HTTPClient():
    def __init__(self):
        self.__locks = {}
        self.__session = aiohttp.ClientSession()

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
            #Possibly make these request more detailed (low priority addition)
            if ResponseData.status >= 400 and ResponseData.status < 500:
                pass 
            if ResponseData.status >= 500:
                pass
