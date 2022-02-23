from utility import load_cfg
from discord.commands import slash_command, Option  # Importing the decorator that makes slash commands.
from base_commands.base_posts import base_posts

cfg = load_cfg()

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="posts",
    description="The base command for advanced RecNet post filtering and sorting."
)
async def posts(
    self, 
    ctx, 
    type: Option(str, choices=["Photos", "Feed"], required=True),
    username: Option(str, "Enter the username", required=False),
    sort: Option(str, "Sort options", choices=["Newest to Oldest", "Oldest to Newest", "Cheers: Highest to Lowest", "Cheers: Lowest to Highest", "Comments: Highest to Lowest", "Comments: Lowest to Highest"], required=False, default="Newest to Oldest"),
    in_rooms: Option(str, "Only show posts taken in specific room(s)", required=False, default=""),
    not_in_rooms: Option(str, "Only show posts not taken in specific room(s)", required=False, default=""),
    with_users: Option(str, "Only show posts with specific user(s) tagged", required=False, default=""),
    without_users: Option(str, "Only show posts without specific user(s) tagged", required=False, default=""),
    during_event: Option(int, "Only show posts taken during an event", required=False, default="", min_value=0),
    exclude_events: Option(str, "Only show posts not taken during specific events", required=False, default=""),
    minimum_cheers: Option(int, "Only show posts with more or equal cheers", required=False, default=0, min_value=0),
    minimum_comments: Option(int, "Only show posts with more or equal comments", required=False, default=0, min_value=0),
    raw: Option(bool, "Send raw images", required=False, default=False)
):
    await ctx.interaction.response.defer()
    view, embeds = await base_posts(self.bot.rec_net, ctx, type=type, username=username, sort=sort, in_rooms=in_rooms, not_in_rooms=not_in_rooms, with_users=with_users, without_users=without_users, during_event=during_event, exclude_events=exclude_events, minimum_cheers=minimum_cheers, minimum_comments=minimum_comments, raw=raw)
    await ctx.respond(embeds=embeds, view=view)
