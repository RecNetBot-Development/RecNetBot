from attr import dataclass

@dataclass
class Response:
    status: int
    success: bool
    data: int or dict or str

    @classmethod
    async def parse_response(cls, resp):
        content_type = resp.content_type
        if resp.content_type == "application/json":
            data = await resp.json()
        elif resp.content_type == "text/plain":
            data = await resp.text()
        else:
            data = resp.content
        return cls(status=resp.status, success=resp.ok, data=data)