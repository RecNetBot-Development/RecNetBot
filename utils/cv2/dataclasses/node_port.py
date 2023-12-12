from dataclasses import dataclass

@dataclass(kw_only=True)
class NodePort:
    name: str
    description: str
    type: str
    is_union: bool # should the port be displayed as white
    is_list: bool # should the port be displayed as a list
    is_input: bool