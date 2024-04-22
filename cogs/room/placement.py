import discord
import recnetpy
import recnetpy.dataclasses
from utils.converters import FetchRoom
from discord.commands import slash_command
from discord.ext.bridge import BridgeOption as Option
from resources import get_icon, get_emoji
from embeds import get_default_embed
from utils.rec_net_urls import img_url, profile_url
from utils.autocompleters import room_searcher
from utils import BaseView, room_url, shorten

class RoomView(BaseView):
    def __init__(self, room: recnetpy.dataclasses.Room):
        super().__init__()

        self.room = room

        # Link buttons
        buttons = [
            discord.ui.Button(
                label=shorten(f"^{self.room.name}", 80),
                url=room_url(self.room.name),
                style=discord.ButtonStyle.link
            ),
            discord.ui.Button(
                label=f"@{self.room.creator_account.username}",
                url=profile_url(self.room.creator_account.username),
                style=discord.ButtonStyle.link
            )
        ]

        for i in buttons:
            self.add_item(i)

@slash_command(
    name="placement",
    description="View a room's placement in the hot page."
)
async def placement(
    self, 
    ctx: discord.ApplicationContext, 
    room: Option(FetchRoom, name="name", description="Enter RR room", required=True, autocomplete=room_searcher),
    filter: Option(str, name="filter", description="Enter keywords or #tags. Example: pvp #contest", required=False)
):
    await ctx.interaction.response.defer()
    em = get_default_embed()
    em.title = "Hot Placement"
    scope = 10_000  # How many rooms to fetch
    
    if filter:
        results = await self.bot.RecNet.rooms.search(filter, take=scope)
    else:
        results = await self.bot.RecNet.rooms.hot(take=scope)
    result_count = len(results)

    # Stop the command if no results were found
    if not results:
        em.description = f"Couldn't find ANY rooms based on your keywords or #tags! (`{filter}`)"
        em.set_thumbnail(url=get_icon("rectnet"))
        return await ctx.respond(embed=em)
    
    # Room thumbnail
    em.set_thumbnail(url=img_url(room.image_name, crop_square=True))
    
    # Find the requested room from the results
    placement = 0
    for i, ele in enumerate(results, start=1):
        if ele.id == room.id:
            placement = i
            break
            
    # Fetch room creator
    await room.get_creator_player()

    # Links to room and creator
    view = RoomView(room)

    # Get tags
    RecNet: recnetpy.Client = self.bot.RecNet
    room_with_tags = await RecNet.rooms.fetch(room.id, 8)
    room.tags = room_with_tags.tags

    # Add filters
    em.add_field(name="Filters", value=filter or "None!", inline=False)

    # If room doesn't have filter tags, flag it
    no_matching_tags = True

    # Format tags as a field in embed
    if room.tags:
        tags_str = []
        split_filter = filter.split(" ") if filter else []
        for i in room.tags:
            # Highlight tags that appear in filters
            if f"#{i.tag}" in split_filter:
                tags_str.append(f"**#{i.tag}**")
                no_matching_tags = False
            else:
                tags_str.append(f"#{i.tag}")
        em.add_field(name="Room Tags", value=", ".join(tags_str), inline=False)

    # if no results were found
    if not placement:
        if filter:
            em.description = f"Couldn't find [^{room.name}]({room_url(room.name)}) from filtered hot rooms!"
            if no_matching_tags:
                em.description += f"\n{get_emoji('warning')} This is because your filters conflict with your room."
        else:
            em.description = f"Couldn't find [^{room.name}]({room_url(room.name)}) from hot rooms!\n{get_emoji('tip')} You could try specifying room tags or keywords in filter."

        em.set_footer(text=f"The room scope is {result_count:,}.")

    else:
        # Room found! Create embed
        em.description = f"Found [^{room.name}]({room_url(room.name)}) at **#{placement:,}**! 🔥"
        em.set_footer(text=f"Ranked based on {result_count:,} platform independent hot rooms!")
    

    return await ctx.respond(embed=em, view=view)
    

    
    

        

        
