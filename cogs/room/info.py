import discord
from utils.converters import FetchRoom
from embeds import get_default_embed
from resources import get_emoji, get_icon
from utils import unix_timestamp, room_url, img_url
from utils.formatters import format_accessibilities, format_roles, format_warnings
from discord.commands import slash_command, Option
from recnetpy.dataclasses.room import Room

@slash_command(
    name="room",
    description="View a Rec Room room's information and statistics."
)
async def info(
    self, 
    ctx: discord.ApplicationContext, 
    room: Option(FetchRoom, name="name", description="Enter RR room", required=True)
):
    await ctx.interaction.response.defer()
    
    await ctx.respond(embed=room_embed(room))
    

def room_embed(room: Room) -> discord.Embed:
    """
    Makes an embed for a single room
    """
    # Sub rooms
    subroom_list = [subroom.name for subroom in room.subrooms[:10]] if room.subrooms else ["None!"]
    if len(room.subrooms) > 10:
        subroom_list.append("...")

    latest_updated_subroom = None
    for subroom in room.subrooms:
        if not latest_updated_subroom or latest_updated_subroom.data_saved_at < subroom.data_saved_at:
            latest_updated_subroom = subroom
        
    # Supported
    supported_list, unsupported_list = format_accessibilities(room)
    supported = ', '.join(supported_list) if supported_list else None
    unsupported = ', '.join(unsupported_list) if unsupported_list else None
            
    # Roles
    role_pieces = format_roles(room.roles)
    roles = "\n".join(role_pieces) if role_pieces else None
    
    # Warnings
    warnings = format_warnings(room.warnings)
    custom_warning = f"```{room.custom_warning}```"
    
    # Tags
    tags = list(map(lambda ele: ele.tag, room.tags)) if room.tags else ["..."]
    
    # Room hot placement
    #placement = 0
    #if hot_rooms: 
    #    if isinstance(hot_rooms, dict):
    #        placement = f"{next((i for (i, _room) in enumerate(hot_rooms) if _room['RoomId'] == room.id), 0):,}"
    #    elif isinstance(hot_rooms, int):
    #        placement = f"{hot_rooms:,}"
            
    # Room engagement
    score = round((sum([i.score for i in room.scores]) / len(room.scores)) * 100) if room.scores else 0

    details = [
        f"{get_emoji('date')} {unix_timestamp(room.created_at)} — Created At",
        f"{get_emoji('tag')} `{', '.join(tags)}` ({len(room.tags)}) — Tags",
        f"{get_emoji('subrooms')} `{', '.join(subroom_list)}` ({len(room.subrooms)}) — Subrooms",
        f"{get_emoji('limit')} `{room.max_players}` — Player Limit",
        f"{get_emoji('update')} In `{latest_updated_subroom.name}` at {unix_timestamp(latest_updated_subroom.data_saved_at if latest_updated_subroom.data_saved_at else room.created_at)} — Latest Update",
    ]

    # Voice moderation check
    if room.voice_moderated: details.insert(-1, f"{get_emoji('toxmod')} Voice Moderation enabled!")
    
    statistics = [
        f"{get_emoji('cheer')} `{room.cheer_count:,}` — Cheers",
        f"{get_emoji('favorite')} `{room.favorite_count:,}` — Favorites",
        f"{get_emoji('visitors')} `{room.visitor_count:,}` — Visitors",
        f"{get_emoji('visitor')} `{room.visit_count:,}` — Visits",
        #f"{get_emoji('hot')} `#{placement if placement else '>1,000'}` — Hot Placement",
        f"{get_emoji('engagement')} `{score}%` — Engagement"
    ]
    
    # Define embed
    em = get_default_embed()
    em.title = f"^{room.name}"
    em.description = f"```{room.description}```"
    em.url = room_url(room.name)
    
    if details: em.add_field(name="Details", value="\n".join(details), inline=False)
    if supported: em.add_field(name="Supported Modes", value=supported, inline=False)
    if unsupported: em.add_field(name="Unsupported Modes", value=unsupported, inline=False)
    if warnings: em.add_field(name="Warnings", value=" ".join(warnings), inline=False)
    if room.custom_warning: em.add_field(name="Custom Warning", value=custom_warning, inline=False)
    if roles: em.add_field(name="Roles", value=roles, inline=False)
    if statistics: em.add_field(name="Statistics", value="\n".join(statistics), inline=False)

    # Set the room's thumbnail as image
    em.set_image(url=img_url(room.image_name))
    
    # Show if UGC or RRO
    thumbnail_url = get_icon("rro") if room.is_rro else get_icon("ugc")
    em.set_thumbnail(url=thumbnail_url)
    
    return em
    
    

        

        
