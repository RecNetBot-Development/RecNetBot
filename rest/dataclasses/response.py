from attr import dataclass

@dataclass
class Response:
    status: int
    success: bool
    data: int or dict or str

    @classmethod
    async def parse_response(cls, res):
        data: str or dict
        if "application/json" in res.headers["Content-type"]:
            data = await res.json()
        else:
            data = await res.text()
        return cls(status=res.status, success=res.ok, data=data)