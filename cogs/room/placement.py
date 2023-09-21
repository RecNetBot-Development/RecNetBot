import discord
from utils.converters import FetchRoom
from discord.commands import slash_command, Option
from utils import room_url
from embeds import get_default_embed
from utils.rec_net_urls import img_url
from utils.autocompleters import room_searcher

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

    # Stop the command if no results were found
    if not results:
        em.description = f"Couldn't find ANY rooms based on your keywords or #tags! (`{filter}`)"
        return await ctx.respond(embed=em)
    
    em.set_thumbnail(url=img_url(room.image_name, crop_square=True))
    
    # Find the requested room from the results
    placement = 0
    for i, ele in enumerate(results, start=1):
        if ele.id == room.id:
            placement = i
            break
            
    # if no results were found
    if not placement:
        patched_room = await room.client.rooms.fetch(room.id, include=8)
        #tags = list(map(lambda tag: f"#{tag.tag}", patched_room.tags))
        tags = []
        pieces = [
            f"Couldn't find [^{room.name}]({room_url(room.name)}) from hot rooms filtered by `{filter or '-'}`.",
            f"The room scope is `{scope:,}`."
        ]
        if tags: pieces.insert(1, f"Room tags: `{', '.join(tags)}`",)
        em.description = "\n".join(pieces)
        return await ctx.respond(embed=em)
    
    # Room found!
    pieces = [
        f"Found [^{room.name}]({room_url(room.name)}) at **#{placement:,}**!",
        "*Ranked based on the platform independant hot room list!*"
    ]
    if filter: pieces.insert(1, f"Keywords and #tags: `{filter}`")  # Add filters if filters
    em.description = "\n".join(pieces)
    
    return await ctx.respond(embed=em)
    

    
    

        

        
