from dataclasses import dataclass
from .breed import Breed
from typing import Optional, List

@dataclass
class Cat:
    id: str
    img_url: str
    breeds: Optional[List[Breed]]
    favorite_id: Optional[int]
