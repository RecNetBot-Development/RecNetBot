from utility import load_cfg, respond
from discord.commands import slash_command, Option  # Importing the decorator that makes slash commands.
from base_commands.base_posts import base_posts

cfg = load_cfg()

@slash_command(
    debug_guilds=cfg['test_guild_ids'],
    name="sort",
    description="Sort a user's shared posts or feed."
)
async def sort(
    self, 
    ctx, 
    type: Option(str, choices=["photos", "feed"], required=True),
    username: Option(str, "Enter the username", required=True),
    sort: Option(str, "Sort options", choices=["Newest to Oldest", "Oldest to Newest", "Cheers: Highest to Lowest", "Cheers: Lowest to Highest", "Comments: Highest to Lowest", "Comments: Lowest to Highest"], required=True)
):
    await ctx.interaction.response.defer()
    view, embeds = await base_posts(self.bot.rec_net, ctx, type=type.capitalize(), username=username, sort=sort)
    await respond(ctx, embeds=embeds, view=view)
