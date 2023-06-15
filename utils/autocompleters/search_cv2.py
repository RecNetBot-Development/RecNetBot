from utils.cv2.fetch_circuits import fetch_circuits
from typing import List
import discord
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

async def cv2_searcher(ctx: discord.AutocompleteContext) -> List[str]:
    """
    Returns a list of CV2 chips
    """
    chips = await fetch_circuits()

    names = []
    starts_with_query = []
    similar_names = []
    direct_hit = ""
    for i in chips:
        chip_name = i.name.lower()
        query = ctx.value.lower()

        # Prioritize exact matches
        if chip_name == query:
            direct_hit = i.name
            continue

        # Secondly matches that start with the query
        if chip_name.startswith(query):
            starts_with_query.append(i.name)
            continue

        # Lastly similar names
        if similar(query, chip_name) > 0.5:
            similar_names.append(i.name)

    # Append to full list
    if starts_with_query:
        names += sorted(starts_with_query, reverse=False)

    if similar_names:
        names += sorted(similar_names, reverse=False)

    # Push direct hit first
    if direct_hit:
        names.insert(0, direct_hit)

    return names