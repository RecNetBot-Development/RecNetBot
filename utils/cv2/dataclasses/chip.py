from dataclasses import dataclass
from typing import List
from .filter_path import FilterPath
from .node_port import NodePort


@dataclass(kw_only=True)
class Chip:
    name: str
    description: str
    is_beta: bool
    is_trolling_risk: bool
    is_role_risk: bool
    is_deprecated: bool
    is_valid_rooms1: bool
    is_valid_rooms2: bool
    filters: List[FilterPath]
    inputs: List[NodePort]
    outputs: List[NodePort]
    uuid: str


def create_chip(chip_json: dict, uuid: str) -> Chip:
    """Creates a new `Chip` object using the provided JSON and UUID and returns it."""
    # Deprecation
    is_deprecated = chip_json["DeprecationStage"] == "Deprecated"

    # Filters
    node_filters = []
    for i in chip_json["NodeFilters"]:
        node_filters.append(FilterPath(path=i["FilterPath"]))
        
    # Collect all ports
    ports = {"inputs": [], "outputs": []}
    if chip_json["NodeDescs"]:
        descs = chip_json["NodeDescs"][0]

        type_params = {}
        for key, params in descs["ReadonlyTypeParams"].items():
            # Cut off parenthesis
            if params.startswith("("):
                type_params[key] = params[1:-1]
                continue

            type_params[key] = params

        for i in descs["Inputs"]:
            type = i["ReadonlyType"]
            # Get rid of parenthesis
            if type.startswith("("):
                type = type[1:-1]
                
            for key, params in type_params.items():
                type = type.replace(key, params)
            
            is_list = False
            if type.startswith("List<"):
                is_list = True
            
            port = NodePort(
                name=i["Name"],
                type=type,
                is_union=type.find("|") != -1,
                is_list=is_list,
                description=i["Description"],
                is_input=True
            )
            ports["inputs"].append(port)
        for i in descs["Outputs"]:
            type = i["ReadonlyType"]
            # Get rid of parenthesis
            if type.startswith("("):
                type = type[1:-1]

            for key, params in type_params.items():
                type = type.replace(key, params)
            
            is_list = False
            if type.startswith("List<"):
                type = type[5:-1]
                is_list = True
            
            port = NodePort(
                name=i["Name"],
                type=type,
                is_union=type.find("|") != -1,
                is_list=is_list,
                description=i["Description"],
                is_input=False
            )
            ports["outputs"].append(port)

    chip = Chip(
        name=chip_json["ReadonlyPaletteName"],
        description=chip_json["Description"] or "No description found!",
        is_beta=chip_json["IsBetaChip"],
        is_trolling_risk=chip_json["IsTrollingRisk"],
        is_role_risk=chip_json["IsRoleAssignmentRisk"],
        is_deprecated=is_deprecated,
        is_valid_rooms1=chip_json["IsValidInRoom1"],
        is_valid_rooms2=chip_json["IsValidInRoom2"],
        filters=node_filters,
        inputs=ports["inputs"],
        outputs=ports["outputs"],
        uuid=uuid
    )

    return chip