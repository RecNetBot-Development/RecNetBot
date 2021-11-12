import discord
from scripts import date_to_unix
from scripts import Emoji  # RNB Emojis

"""Makes an embed for a single room"""
async def room_embed(room_data: dict, icons: bool = True, explanations: bool = True):
    # Unpack required data
    try:
        name, room_id, creator, img_name, description, cheers, favorites, visitors, visits, unix_date, tags, subrooms, max_players, rro = room_data['Name'], room_data['RoomId'], room_data['CreatorAccountId'], room_data['ImageName'], room_data['Description'], room_data['Stats']['CheerCount'], room_data['Stats']['FavoriteCount'], room_data['Stats']['VisitorCount'], room_data['Stats']['VisitCount'], date_to_unix(room_data['CreatedAt']), room_data['Tags'], room_data['SubRooms'], room_data['MaxPlayers'], room_data['IsRRO']
        accessibility = [
            {"mode": "`Screen`", "supported": room_data['SupportsScreens'], "icon": Emoji.screen},
            {"mode": "`Walk`", "supported": room_data['SupportsWalkVR'], "icon": Emoji.walk},
            {"mode": "`Teleport`", "supported": room_data['SupportsTeleportVR'], "icon": Emoji.teleport},
            {"mode": "`Quest 1`", "supported": room_data['SupportsVRLow'], "icon": Emoji.quest1},
            {"mode": "`Quest 2`", "supported": room_data['SupportsQuest2'], "icon": Emoji.quest2},
            {"mode": "`Mobile`", "supported": room_data['SupportsMobile'], "icon": Emoji.mobile},
            {"mode": "`Juniors`", "supported": room_data['SupportsJuniors'], "icon": Emoji.junior}
        ]

    except TypeError:  # Missing required data
        return

    # Tags
    tag_list = []
    for tag in tags:  # Appends all tags in a list so it can be joined easily
        tag_list.append(tag['Tag'])
        
    # Subrooms
    subroom_list = []
    for subroom in subrooms:  # Appends all subrooms in a list so it can be joined easily
        subroom_list.append(subroom['Name'])

    # Supported
    supported_list, unsupported_list = [], []
    for mode in accessibility:  # Goes through all accessibility options
        mode_name = f"{mode['icon'] if icons else mode['mode']} {mode['mode'] if icons and explanations else ''}"

        if mode['supported']:
            supported_list.append(mode_name)
            continue
        unsupported_list.append(mode_name)

    # Information of the post that'll be included in the embed
    desc = f"""
**Description**
```{description}```
**Information**
{Emoji.date if icons else 'Created At:'} <t:{unix_date}:f> {'*(CREATED AT)*' if explanations else ''}
{Emoji.tag if icons else 'Tags:'} `#{", #".join(tag_list)}` {'*(TAGS)*' if explanations else ''}
{Emoji.door if icons else 'Subrooms:'} `{", ".join(subroom_list)}` {'*(SUBROOMS)*' if explanations else ''}
{Emoji.visitors if icons else 'Max Players:'} `{max_players}` {'*(MAX PLAYERS)*' if explanations else ''}

**Accessibility**
{Emoji.correct + " | " if icons else 'Supported:'} {', '.join(supported_list)} {'*(SUPPORTED)*' if explanations else ''}
{Emoji.incorrect + " | " if icons else 'Not supported:'} {', '.join(unsupported_list)} {'*(UNSUPPORTED)*' if explanations else ''}

**Statistics**
{Emoji.cheer if icons else 'Cheers:'} `{cheers:,}` {'*(CHEERS)*' if explanations else ''}
{Emoji.favorite if icons else 'Favorites:'} `{favorites:,}` {'*(FAVORITES)*' if explanations else ''}
{Emoji.visitors if icons else 'Visitors:'} `{visitors:,}` {'*(VISITORS)*' if explanations else ''}
{Emoji.visitor if icons else 'Visits:'} `{visitors:,}` {'*(VISITS)*' if explanations else ''}
    """

    # Define embed
    em = discord.Embed(
        title = f"^{name} {'(RRO)' if rro else ''}",
        description = desc,
        url=f"https://rec.net/room/{name}"
    )

    # Add the room thumbnail
    em.set_image(url="https://img.rec.net/" + img_name)

    return em  # Return the embed.