from attr import dataclass

@dataclass
class Response:
    status: int
    success: bool
    data: int or dict or str

    @classmethod
    async def parse_response(cls, resp):
        data = await resp.json() if "application/json" in resp.headers["Content-Type"] else await resp.text() 
        return cls(status=resp.status, success=resp.ok, data=data)