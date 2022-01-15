from scripts import load_cfg
from discord.commands import slash_command, Option # Importing the decorator that makes slash commands.
from embeds import profile_embed, Profile

cfg = load_cfg()

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="profile",
    description="View a user's profile."
)
async def profile(
    self, 
    ctx, 
    username: Option(str, "Enter user's username", required=True)
):
    user = await self.bot.rec_net.account(name=username, includes=["bio", "progress", "subs"])
    await ctx.respond(embed=profile_embed(ctx, user), view=Profile(user))