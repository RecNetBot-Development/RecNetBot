from utility import load_cfg
from discord.commands import slash_command, Option # Importing the decorator that makes slash commands.
from utility.discord_helpers.helpers import respond
from embeds.error_embed import error_embed
from embeds.room.views.rank import Rank

cfg = load_cfg()

def separate_tags(_filter):
        return "#" in _filter
    
def separate_keywords(_filter):
    return "#" not in _filter

@slash_command(
    debug_guilds=cfg['test_guild_ids'],
    name="rank",
    description="Check room ranking based on keywords and #tags!"
)
async def rank(
    self, 
    ctx,
    specify: Option(str, "Enter any #tags or keywords to filter results (separate by space)", required=False),
    room_count: Option(int, "Specify how many rooms should be included in ranking.", required=False, default=10, min_value=3, max_value=15)
):
    if specify:
        room_resp = await self.bot.rec_net.rec_net.rooms.rooms.search.get(params={"query": specify, "take": room_count}).fetch()
    else:
        room_resp = await self.bot.rec_net.rec_net.rooms.rooms.hot.get(params={"take": room_count}).fetch()
        
    rooms = room_resp.data['Results']
    
    tags, keywords = None, None
    if specify: 
        split_filters = specify.split(",")
        tags = ' '.join(list(filter(separate_tags, split_filters)))
        keywords = ' '.join(list(filter(separate_keywords, split_filters)))
        
        tags = tags if tags else 'None!'
        keywords = keywords if keywords else 'None!'
    
    if not rooms: 
        return await respond(
            ctx, 
            embed=error_embed(
                error=None,
                custom_text=f"No room found with specified keywords and #tags!\nTags: `{tags}`\nKeywords: `{keywords}`"
            )
        )
    
    rank_view = Rank(self.bot.rec_net, rooms, tags, keywords)
    await rank_view.respond(ctx)