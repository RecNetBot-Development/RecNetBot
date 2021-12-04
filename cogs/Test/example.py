from scripts import load_cfg
from discord.commands import slash_command # Importing the decorator that makes slash commands.
from embeds import image_embed

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
    user = await self.bot.rec_net.account(account_id=id).get_user()
    await ctx.respond(f"Username from API: `{user.username}`")

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="username",
    description="Sends user's username from the API."
) # Create a slash command for the supplied guilds.
async def username(self, ctx, username: str):
    user = await self.bot.rec_net.account(username=username).get_user()
    await ctx.respond(f"Username from API: `{user.username}`")

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="platforms",
    description="Sends user's platforms."
)
async def platforms(self, ctx, username: str):
    user = await self.bot.rec_net.account(username=username).get_user()
    await ctx.respond(f"Platforms: `{user.platforms}`")

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="bio",
    description="Sends user's bio."
)
async def bio(self, ctx, username: str):
    user = await self.bot.rec_net.account(username=username, include_bio=True).get_user()
    await ctx.respond(f"Bio: ```{user.bio}```")

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="progression",
    description="Sends user's progression."
)
async def progression(self, ctx, username: str):
    user = await self.bot.rec_net.account(username=username, include_progression=True).get_user()
    await ctx.respond(f"lvl: `{user.progression.lvl}` xp: `{user.progression.xp}`")

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="subs",
    description="Sends user's subs."
)
async def subs(self, ctx, username: str):
    user = await self.bot.rec_net.account(username=username, include_subscriber_count=True).get_user()
    await ctx.respond(f"subs: `{user.subscriber_count}`")

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="bulk",
    description="bulk"
)
async def bulk(self, ctx, ids: str):
    user = await self.bot.rec_net.account(account_id=ids.split(":"), include_subscriber_count=True, include_progression=True, include_bio=True).get_user()

    msg = ""
    for account in user: msg += f"{account.username}: `{account.subscriber_count:,}`, `{account.bio}`, `{account.progression['lvl']}`\n"
    await ctx.respond(msg)

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="created",
    description="createdat"
)
async def createdat(self, ctx, username: str):
    user = await self.bot.rec_net.account(username=username).get_user()
    await ctx.respond(f"<t:{user.created_at}:f>")

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="image",
    description="images indeed"
)
async def image(self, ctx, username: str):
    user = await self.bot.rec_net.account(username=username, include_posts=True, include_feed=True).get_user()
    await ctx.respond(f"posts: {len(user.posts)}, feed: {len(user.feed)}")

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="latest",
    description="latest test command...!"
)
async def latest(self, ctx, username: str):
    user = await self.bot.rec_net.account(username=username, include_posts=True).get_user()
    embed = image_embed(ctx, user.posts[0])
    await ctx.respond(embed=embed)

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="oldest",
    description="oldest test command...!"
)
async def oldest(self, ctx, username: str):
    user = await self.bot.rec_net.account(username=username, include_feed=True).get_user()
    embed = image_embed(ctx, user.feed[-1])
    await ctx.send(embed=embed)