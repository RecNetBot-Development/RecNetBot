from rest import Client, AccountNotFound
from scripts import load_cfg
from discord.commands import slash_command # Importing the decorator that makes slash commands.

cfg = load_cfg()

@slash_command() # Not passing in guild_ids creates a global slash command (might take an hour to register).
async def hi(self, ctx):
    await ctx.respond(f"Hi, this is a global slash command from a cog!")

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="accountid",
    description="Sends username from account id."
) # Create a slash command for the supplied guilds.
async def accountid(self, ctx, id: int):
    user = await self.rn.account(account_id=id).get_user()
    await ctx.respond(f"Username from API: `{user.username}`")

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="username",
    description="Sends user's username from the API."
) # Create a slash command for the supplied guilds.
async def username(self, ctx, username: str):
    user = await self.rn.account(username=username).get_user()
    await ctx.respond(f"Username from API: `{user.username}`")

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="platforms",
    description="Sends user's platforms."
)
async def platforms(self, ctx, username: str):
    user = await self.rn.account(username=username).get_user()
    await ctx.respond(f"Platforms: `{user.platform_names}`")

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="bio",
    description="Sends user's bio."
)
async def bio(self, ctx, username: str):
    user = await self.rn.account(username=username, include_bio=True).get_user()
    await ctx.respond(f"Bio: ```{user.bio}```")

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="progression",
    description="Sends user's progression."
)
async def progression(self, ctx, username: str):
    user = await self.rn.account(username=username, include_progression=True).get_user()
    await ctx.respond(f"lvl: `{user.progression['lvl']}` xp: `{user.progression['xp']}`")

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="subs",
    description="Sends user's subs."
)
async def subs(self, ctx, username: str):
    user = await self.rn.account(username=username, include_subscribers=True).get_user()
    await ctx.respond(f"subs: `{user.subscribers}`")
