import requests  # For testing purposes
from scripts import load_cfg
from embeds import image_embed, finalize_embed
from discord.commands import slash_command # Importing the decorator that makes slash commands.

cfg = load_cfg()

@slash_command(guild_ids=[cfg['test_guild_id']]) # Create a slash command for the supplied guilds.
async def image_test(self, ctx, post_id: int):
    async def get_post_data(post_id):  # Temporary for testing purposes
        url = f"https://api.rec.net/api/images/v4/{post_id}"
        r = requests.get(url)
        if r.ok:
            return r.json()
        return {}

    post_data = await get_post_data(post_id)

    # Test post
    em = await image_embed(post_data)  # Get embed
    await ctx.respond(embed=await finalize_embed(em, ctx.author))