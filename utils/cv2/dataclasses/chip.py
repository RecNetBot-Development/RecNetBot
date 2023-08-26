from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from .filter_path import FilterPath
from .node_port import NodePort


@dataclass
class Chip:
    name: str
    description: str
    is_beta: bool
    is_trolling_risk: bool
    is_role_risk: bool
    is_deprecated: bool
    filters: List[FilterPath]
    inputs: List[NodePort]
    outputs: List[NodePort]
    uuid: Optional[str]


def create_dataclass(chip_json: dict, uuid: str = None) -> Chip:
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
            
            port = NodePort(
                name=i["Name"] if i["Name"] else "—",
                type=type,
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

            port = NodePort(
                name=i["Name"] if i["Name"] else "—",
                type=type,
                description=i["Description"],
                is_input=False
            )
            ports["outputs"].append(port)

    chip = Chip(
        name=chip_json["ReadonlyPaletteName"],
        description=chip_json["Description"] if chip_json["Description"] else "No description found!",
        is_beta=chip_json["IsBetaChip"],
        is_trolling_risk=chip_json["IsTrollingRisk"],
        is_role_risk=chip_json["IsRoleAssignmentRisk"],
        is_deprecated=is_deprecated,
        filters=node_filters,
        inputs=ports["inputs"],
        outputs=ports["outputs"],
        uuid=uuid
    )

    return chip