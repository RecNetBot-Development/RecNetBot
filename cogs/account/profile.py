from scripts import load_cfg, img_url
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
    username: Option(str, "Enter user's username", required=True),
    specified: Option(str, "Choose specific information", choices=["Profile", "Profile Picture", "Banner", "Platforms"], required=False, default="Profile")
):
    match specified:
        case "Profile Picture":  # Raw PFP
            user = await self.bot.rec_net.account(name=username)
            return await ctx.respond(img_url(user.profile_image), view=Profile(user))
        case "Banner":  # Raw banner
            user = await self.bot.rec_net.account(name=username)
            return await ctx.respond(img_url(user.banner_image), view=Profile(user))
        case "Platforms": # Just the platforms
            user = await self.bot.rec_net.account(name=username)
            return await ctx.respond(embed=profile_embed(ctx, user, "platforms"), view=Profile(user))
        case _:  # Full profile as default
            user = await self.bot.rec_net.account(name=username, includes=["bio", "progress", "subs"])
            return await ctx.respond(embed=profile_embed(ctx, user), view=Profile(user))
    