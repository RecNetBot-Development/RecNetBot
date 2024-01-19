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


def get_formatted_port(port: NodePort, format: str) -> str:
    """`format` param uses `format`, `type`, and `port` placeholders to use for formatting"""
    # Port is union
    if port.is_union:
        port_emoji = PORT_EMOJI["union"]
    # Port is not union
    else:
        port_type = port.type
        if port_type.startswith("List<"):
            port_type = port_type[5:-1]
        if port_type in PORT_EMOJI.keys():
            port_emoji = PORT_EMOJI[port_type]
        else:
            port_emoji = PORT_EMOJI["yellow"]
    
    return format.format(name=port.name, type=port.type, port=port_emoji)