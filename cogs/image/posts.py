from dataclasses import dataclass
from scripts import load_cfg, handle_filters
from discord.commands import slash_command, Option  # Importing the decorator that makes slash commands.
from embeds import ImageUI, loading_embed

cfg = load_cfg()

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="posts",
    description="View a user's RecNet posts."
)
async def posts(
    self, 
    ctx, 
    username: Option(str, "Enter user's username", required=True),
    sort: Option(str, "Choose specific information", choices=["Newest to Oldest", "Oldest to Newest", "Cheers: Highest to Lowest", "Cheers: Lowest to Highest", "Comments: Highest to Lowest", "Comments: Lowest to Highest"], required=False, default="Newest to Oldest"),
    raw: Option(bool, "Send raw images", required=False, default=False),
    in_rooms: Option(str, "Only show posts taken in specific room(s)", required=False, default=""),
    not_in_rooms: Option(str, "Only show posts not taken in specific room(s)", required=False, default=""),
    with_users: Option(str, "Only show posts with specific user(s) tagged", required=False, default=""),
    without_users: Option(str, "Only show posts without specific user(s) tagged", required=False, default=""),
    during_event: Option(int, "Only show posts taken during an event", required=False, default="", min_value=0),
    exclude_events: Option(str, "Only show posts not taken during specific events", required=False, default=""),
    minimum_cheers: Option(int, "Only show posts with more or equal cheers", required=False, default=0, min_value=0),
    minimum_comments: Option(int, "Only show posts with more or equal comments", required=False, default=0, min_value=0)
):
    interaction = await ctx.respond(embed=loading_embed(ctx))
    post_options = {
        "take": 2**16           
    }
    user = await self.bot.rec_net.account(name=username, includes=["posts"], options={"posts": post_options})

    post_filter = {}
    if in_rooms: post_filter["rooms"] = Filter("In room(s)", in_rooms)
    if not_in_rooms: post_filter["not_rooms"] = Filter("Not in room(s)", not_in_rooms)
    if with_users: post_filter["with_users"] = Filter("User(s) tagged", with_users)
    if without_users: post_filter["without_users"] = Filter("User(s) not tagged", without_users)
    if during_event: post_filter["during_event"] = Filter("During event", during_event, False)
    if exclude_events: post_filter["exclude_events"] = Filter("Not during event(s)", exclude_events)
    if minimum_cheers: post_filter["minimum_cheers"] = Filter("Minimum cheers", minimum_cheers, False)
    if minimum_comments: post_filter["minimum_comments"] = Filter("Minimum comments", minimum_comments, False)
    
    await ImageUI(ctx, user.posts, raw=raw, post_filter=post_filter, interaction=interaction, sort=sort).start()

class Filter:
    def __init__(self, name, filter, handle=True):
        self.name = name
        handled_filters = handle_filters(filter) if handle else filter
        self.filter = handled_filters

        

    

