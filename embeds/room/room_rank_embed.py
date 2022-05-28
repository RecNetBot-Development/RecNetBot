from embeds.base.embed import DefaultEmbed as Embed
from utility.emojis import get_icon
from utility.rec_net_helpers import room_url

def format_room(room_tuple):
    return f"{room_tuple[0]}. [`^{room_tuple[1]['Name']}`]({room_url(room_tuple[1]['Name'])})"

def room_rank_embed(raw_rooms, tags, keywords):
    em = Embed(
        title=f"Rooms ranked based on keywords and tags",
        description = 
        f"Keywords `{keywords}`\n"
        f"Tags `{tags}`"
    )
    
    rooms = raw_rooms[:25]  # Condense list to 25 rooms
    enumerated_rooms = list(enumerate(rooms, start=1))
    ranked_rooms = list(map(format_room, enumerated_rooms))
    
    em.add_field(
        name="Ranked",
        value="\n".join(ranked_rooms)
    )
    
    return em