from dataclasses import dataclass

@dataclass
class NodePort:
    name: str
    description: str
    type: str
    is_input: bool