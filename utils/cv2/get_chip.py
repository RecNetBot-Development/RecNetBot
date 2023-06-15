from .dataclasses.chip import Chip
from .fetch_circuits import fetch_circuits
from typing import Optional

async def get_chip(chip_name: str) -> Optional[Chip]:
    chips = await fetch_circuits()

    lower_name = chip_name.lower()
    for chip in chips:
        if lower_name == chip.name.lower():
            return chip

    # Chip wasn't found
    return None