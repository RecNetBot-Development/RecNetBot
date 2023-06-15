import aiohttp
from os.path import exists
import datetime
import json
import asyncio
from typing import List, Optional
from .dataclasses.chip import Chip, create_dataclass

GITHUB_URL = "https://raw.githubusercontent.com/tyleo-rec/CircuitsV2Resources/master/misc/circuitsv2.json"
CACHE_DATE_PATH = "resources/cv2/cache_date.txt"
CV2_JSON = "resources/cv2/cv2.json"
cached_dataclasses = []

async def fetch_circuits() -> List[Chip]:
    """ 
    Fetch CV2 json from GitHub 
    The circuits JSON is cached for a week.
    """
    global cached_dataclasses

    if is_cache_expired():
        async with aiohttp.ClientSession() as session:
            async with session.get(GITHUB_URL) as resp:
                cv2_string = await resp.text()

        cv2_json = json.loads(cv2_string)
        cache_circuits(cv2_json)

    else:
        if cached_dataclasses:
            return cached_dataclasses
        else:
            cv2_json = load_cached_circuits()

    chips = []
    for i in cv2_json["Nodes"]:
        # Get the chip
        node = cv2_json["Nodes"][i]

        # Create dataclass and append
        chip = create_dataclass(node, i)
        chips.append(chip)

    cached_dataclasses = chips
    return chips


def load_cached_circuits() -> Optional[dict]:
    if exists(CV2_JSON):
        with open(CV2_JSON, 'r', encoding='utf-8') as f:
            cv2_json = json.load(f)
    else:
        return None

    return cv2_json


def is_cache_expired() -> bool:
    if exists(CACHE_DATE_PATH):
        with open(CACHE_DATE_PATH, "r") as f:
            timestamp = f.readline()

        now_timestamp = datetime.datetime.now().timestamp()

        # If true, a week has passed
        return int(now_timestamp) > int(timestamp)
    else:
        return True
        

def cache_circuits(cv2_json: dict) -> None:
    with open(CV2_JSON, 'w', encoding='utf-8') as f:
        json.dump(cv2_json, f, ensure_ascii=False, indent=4)

    # Date for next cache
    next_week = datetime.datetime.now() + datetime.timedelta(weeks=1)
    new_timestamp = str(int(next_week.timestamp()))

    with open(CACHE_DATE_PATH, 'w') as f:
        f.write(new_timestamp + f"\n\nThe circuits JSON will be updated on {next_week.date()}")


if __name__ == "__main__":
    ...
    #print(cv2_json)