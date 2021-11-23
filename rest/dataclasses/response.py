from attr import dataclass

@dataclass
class Response:
    status: int
    success: bool
    data: int or dict or str