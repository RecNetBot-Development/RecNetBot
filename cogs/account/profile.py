from scripts import load_cfg, img_url
from discord.commands import slash_command, Option, SlashCommandGroup # Importing the decorator that makes slash commands.
from embeds import profile_embed, Profile

cfg = load_cfg()

cmd_profile = SlashCommandGroup("account", "profile commands", guild_ids=[cfg['test_guild_id']])
extra_profile = cmd_profile.create_subgroup(
    "profile_extra", "bruh"
)

@cmd_profile.command(
    guild_ids=[cfg['test_guild_id']],
    name="profile",
    description="View a user's profile."
)
async def profile(
    self, 
    ctx, 
    username: Option(str, "Enter user's username", required=True)
):
    print(type(extra_profile))
    user = await self.bot.rec_net.account(name=username, includes=["bio", "progress", "subs"])
    await ctx.respond(embed=profile_embed(ctx, user), view=Profile(user))

@extra_profile.command(
    guild_ids=[cfg['test_guild_id']],
    name="pfp",
    description="View a user's profile picture."
)
async def pfp(
    self, 
    ctx, 
    username: Option(str, "Enter user's username", required=True)
):
    print(type(extra_profile))
    user = await self.bot.rec_net.account(name=username)
    await ctx.respond(img_url(user.profile_image), view=Profile(user))

