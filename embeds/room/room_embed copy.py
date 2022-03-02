from discord import Embed
from embeds.finalize_embed import finalize_embed
from utility import Emoji, unix_timestamp, img_url

"""Makes an embed for a single room"""
def room_embed(ctx, room):
    accessibility = [
        {"mode": "`Screen`", "supported": 'screen' in room.supported_platforms, "icon": Emoji.screen},
        {"mode": "`Walk`", "supported": 'walk' in room.supported_platforms, "icon": Emoji.walk},
        {"mode": "`Teleport`", "supported": 'teleport' in room.supported_platforms, "icon": Emoji.teleport},
        {"mode": "`Quest 1`", "supported": 'vr low' in room.supported_platforms, "icon": Emoji.quest1},
        {"mode": "`Quest 2`", "supported": 'quest 2' in room.supported_platforms, "icon": Emoji.quest2},
        {"mode": "`Mobile`", "supported": 'mobile' in room.supported_platforms, "icon": Emoji.mobile},
        {"mode": "`Juniors`", "supported": 'juniors' in room.supported_platforms, "icon": Emoji.junior}
    ]

    # Sub rooms
    subroom_list = [subroom.name for subroom in room.sub_rooms] if room.sub_rooms else ["None!"]

    # Supported
    supported_list, unsupported_list = [], []
    for mode in accessibility:  # Goes through all accessibility options
        mode_name = f"{mode['icon']} {mode['mode']}"

        if mode['supported']:
            supported_list.append(mode_name)
            continue
        unsupported_list.append(mode_name)
    
    # Define embed
    em = Embed(
        title = f"^{room.name} {'(RRO)' if room.is_rro else ''}",
        description = f"```{room.description}```",
        url=f"https://rec.net/room/{room.name}"
    )
    
    information = f"""
{Emoji.date} Created At {unix_timestamp(room.created_at)}
{Emoji.tag} Tags `{', '.join(room.tags)}` ({len(room.tags)})
{Emoji.door} Subrooms `{", ".join(subroom_list)}` ({len(subroom_list)})
{Emoji.visitors} Player Limit `{room.max_players}`
    """

    accessibility = f"""
{(Emoji.correct + ' Allowed ' + ', '.join(supported_list)) if supported_list else ''}
{(Emoji.incorrect + ' Not Allowed ' + ', '.join(unsupported_list)) if unsupported_list else ''}
    """
    
    statistics = f"""
{Emoji.cheer} Cheers `{room.cheer_count:,}`
{Emoji.favorite} Favorites `{room.favorite_count:,}`
{Emoji.visitors} Visitors `{room.visitor_count:,}`
{Emoji.visitor} Visits `{room.visit_count:,}`
    """
    
    em.add_field(name="Information", value=information, inline=False)
    em.add_field(name="Accessibility", value=accessibility, inline=False)
    em.add_field(name="Statistics", value=statistics, inline=False)

    # Add the room thumbnail
    em.set_image(url=img_url(room.image_name))

    em = finalize_embed(ctx, em)
    return em  # Return the embed.