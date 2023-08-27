from dataclasses import dataclass
from typing import List

@dataclass
class NodePort:
    name: str
    description: str
    type: List[str] # more than one type means the port is a union
    is_list: bool # flag to tell if the port is a list of the above type
    is_input: bool