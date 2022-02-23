from .finalize_embed import finalize_embed
from discord import Embed

def filter_embed(ctx, filters, sort, original_length, new_length):
    # Define embed
    filter_desc = f"Sorted by `{sort}`\n"
    for filter in filters:
        filter_name = filters[filter].name
        value = filters[filter].readable_filter
        value_type = type(value)
        if value_type is str:
            value = value.capitalize()
        elif value_type is int:
            value = value
        elif value_type is list:
            value =  ', '.join(map(str, value))

        filter_desc += f"{filter_name} `{value}`\n"

    filter_desc += f"\nPost difference after filtering `{original_length:,}` -> `{new_length:,}`"
    em = Embed(
        title="Post Filters",
        description = filter_desc
    )
    em = finalize_embed(ctx, em)
    return em