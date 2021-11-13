from rest import route_manager as route
from scripts import load_cfg, log
from embeds import image_embed, finalize_embed
from discord.commands import slash_command # Importing the decorator that makes slash commands.

cfg = load_cfg()
obj = route.APIRouteManager()

@slash_command(guild_ids=[cfg['test_guild_id']]) # Create a slash command for the supplied guilds.
async def image_test(self, ctx, post_id: int):
    log(ctx)

    post_data = await obj.api.images.v4(post_id).get().data

    # Test post
    em = await image_embed(post_data)  # Get embed
    await ctx.respond(embed=await finalize_embed(em, ctx.author))