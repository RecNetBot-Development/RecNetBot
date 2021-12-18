from attr import dataclass

@dataclass
class Response:
    status: int
    success: bool
    data: int or dict or str

    @classmethod
    async def parse_response(cls, res):
        data: str or dict
        async def parse_response(resp):
            if "application/json" in resp.headers["Content-Type"]:
                data = await resp.json()
            data = await resp.text()  
        return cls(status=res.status, success=res.ok, data=data)