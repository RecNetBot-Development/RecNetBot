from .dataclasses.chip import Chip
from .fetch_circuits import fetch_circuits
from typing import Optional

async def get_chip(chip_uuid: str) -> Optional[Chip]:
    chips = await fetch_circuits()

    # Returns the chip with the given UUID, otherwise returns None
    return chips.get(chip_uuid, None)