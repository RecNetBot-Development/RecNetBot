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
    try:
        user = await self.rn.account(account_id=id).get_account_by_id()
    except AccountNotFound:
        return await ctx.respond(f"Couldn't find account with the id `{id}`")
    await ctx.respond(user.username)

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="username",
    description="Sends user's username from the API."
) # Create a slash command for the supplied guilds.
async def username(self, ctx, username: str):
    try:
        user = await self.rn.account(username=username).get_account_by_username()
    except AccountNotFound:
        return await ctx.respond(f"Couldn't find `@{username}`")
    await ctx.respond(user.username)

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="platforms",
    description="Sends user's platforms."
)
async def platforms(self, ctx, username: str):
    try:
        user = await self.rn.account(username=username).get_account_by_username()
    except AccountNotFound:
        return await ctx.respond(f"Couldn't find `@{username}`")

    await ctx.respond(user.platform_names)

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="bio",
    description="Sends user's bio."
)
async def bio(self, ctx, username: str):
    try:
        user = await self.rn.account(username=username, include_bio=True).get_account_by_username()
    except AccountNotFound:
        return await ctx.respond(f"Couldn't find `@{username}`")

    await ctx.respond(user.bio)
