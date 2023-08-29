from resources import get_emoji
from .dataclasses.node_port import NodePort


PORT_EMOJI = {
    "exec": get_emoji("port_exec"),
    "string": get_emoji("port_string"),
    "int": get_emoji("port_int"),
    "float": get_emoji("port_float"),
    "bool": get_emoji("port_bool"),
    "union": get_emoji("port_union"),
    "any": get_emoji("port_union"),
    "color": get_emoji("port_color"),
    "yellow": get_emoji("port_yellow")
}


def generate_port_listing(port: NodePort, format: str) -> str:
    # Port is union and list
    if len(port.type) > 1 and port.is_list:
        type_str = f"List<{' | '.join(port.type)}>"
        port_emoji = PORT_EMOJI["union"]
    # Port is list
    elif port.is_list:
        type_str = f"List<{port.type[0]}>"
        if port.type[0] in PORT_EMOJI.keys():
            port_emoji = PORT_EMOJI[port.type[0]]
        else:
            port_emoji = PORT_EMOJI["yellow"]
    # Port is union
    elif len(port.type) > 1:
        type_str = " | ".join(port.type)
        port_emoji = PORT_EMOJI["union"]
    # Port is neither union or list
    else:
        type_str = port.type[0]
        if port.type[0] in PORT_EMOJI.keys():
            port_emoji = PORT_EMOJI[port.type[0]]
        else:
            port_emoji = PORT_EMOJI["yellow"]
    
    return format.format(name=port.name, type=type_str, port=port_emoji)