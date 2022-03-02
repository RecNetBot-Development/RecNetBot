from utility import load_cfg
from discord.commands import slash_command, Option  # Importing the decorator that makes slash commands.
from rec_net.exceptions import Error
from embeds import json_embed

cfg = load_cfg()

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="postdata",
    description="Get raw post data from the API."
)
async def postdata(
    self, 
    ctx,
    post: Option(str, "Enter the post's id", required=True)
):
    await ctx.interaction.response.defer()
    parsed_post_id = int(post)
    post_resp = await self.bot.rec_net.rec_net.api.images.v4(parsed_post_id).get().fetch()

    await ctx.respond(
        content = f"https://api.rec.net/api/images/v4/{parsed_post_id}",
        embed=json_embed(ctx, post_resp.data)
    )