from utils.cv2.fetch_circuits import fetch_circuits
from typing import List, Union
import discord
from discord import OptionChoice
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

async def cv2_searcher(ctx: discord.AutocompleteContext) -> List[OptionChoice]:
    """
    Returns a list of CV2 chips
    """
    chips = await fetch_circuits()

    options: List[OptionChoice] = []
    starts_with_query: List[OptionChoice] = []
    similar_names: List[OptionChoice] = []
    direct_hit: Union[OptionChoice, None] = None
    query = ctx.value.lower()
    for i in chips.values():
        chip_name = i.name.lower()

        # Prioritize exact matches
        if chip_name == query:
            direct_hit = OptionChoice(i.name, i.uuid)
            continue

        # Secondly matches that start with the query
        if chip_name.startswith(query):
            starts_with_query.append(OptionChoice(i.name, i.uuid))
            continue

        # Lastly similar names
        if similar(query, chip_name) > 0.5:
            similar_names.append(OptionChoice(i.name, i.uuid))

    # Append to full list
    if starts_with_query:
        options += sorted(starts_with_query, key=lambda x: x.to_dict()["name"], reverse=False)

    if similar_names:
        options += sorted(similar_names, key=lambda x: x.to_dict()["name"], reverse=False)

    # Push direct hit first
    if direct_hit:
        options.insert(0, direct_hit)

    return options