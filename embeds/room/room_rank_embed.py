from embeds.base.embed import DefaultEmbed as Embed
from utility.emojis import get_emoji, get_icon
from utility.rec_net_helpers import room_url

def format_room(room_tuple, ranking_method):
    placement, room_data = room_tuple[0], room_tuple[1]
    default = f"{placement}. `^{room_data['Name']}`"
    
    match ranking_method:
        case "Cheers":
            return default + f" {get_emoji('cheer')} `{room_data['Stats']['CheerCount']:,}`"
        case "Favorites":
            return default + f" {get_emoji('favorite')} `{room_data['Stats']['FavoriteCount']:,}`"
        case "Visits":
            return default + f" {get_emoji('visitor')} `{room_data['Stats']['VisitCount']:,}`"
        case "Visitors":
            return default + f" {get_emoji('visitors')} `{room_data['Stats']['VisitorCount']:,}`"
        case _:
            return default

def room_rank_embed(raw_rooms, tags, keywords, ranking_method="Popularity"):
    em = Embed(
        title=f"Rooms ranked based on keywords and tags",
        description = 
        f"Rooms are initially sorted by RecNet's popularity sort and then re-sorted by your liking.\n"
        f"Keywords `{keywords}`\n"
        f"Tags `{tags}`\n"
        f"Ranking Method `{ranking_method}`"
    )
    
    rooms = raw_rooms[:15]  # Condense list to 15 rooms
    enumerated_rooms = list(enumerate(rooms, start=1))
    ranked_rooms = list(map(lambda room: format_room(room, ranking_method), enumerated_rooms))
    
    ranked_rooms[0] = ranked_rooms[0].replace("1.", get_emoji("first_place"))
    if len(ranked_rooms) >= 2: ranked_rooms[1] = ranked_rooms[1].replace("2.", get_emoji("second_place"))
    if len(ranked_rooms) >= 3: ranked_rooms[2] = ranked_rooms[2].replace("3.", get_emoji("third_place"))
    
    em.add_field(
        name="Ranking",
        value="\n".join(ranked_rooms)
    )
    
    em.set_thumbnail(url=get_icon("room"))
    
    return em