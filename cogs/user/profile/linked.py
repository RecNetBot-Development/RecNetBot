import discord
from discord import ApplicationContext
from discord.commands import slash_command, Option
from embeds import get_default_embed, fetch_profile_embed
from utils import profile_url
from database import ConnectionManager

# User can only run the command once every "per" seconds
@slash_command(
    name="linked",
    description="Check which Rec Room account is linked to a Discord account."
)
async def linked(
    self, 
    ctx: ApplicationContext,
    mention: Option(discord.User, description="Whose Discord account should be checked?", required=False)
):
    await ctx.interaction.response.defer(ephemeral=True)
    
    # Get the wanted Discord user
    discord_user = mention if mention else ctx.author

    # Check if Discord user has already linked an account
    cm: ConnectionManager = self.bot.cm
    check_discord = await cm.get_discord_connection(discord_user.id)
    if check_discord:
        user = await self.bot.RecNet.accounts.fetch(check_discord.rr_id)
        
        profile_em = await fetch_profile_embed(user)
        em = get_default_embed()
        group = discord.utils.get(self.__cog_commands__, name='profile')
        unlink_command = discord.utils.get(group.walk_commands(), name='unlink')

        if discord_user == ctx.author:
            em.description = f"Your Discord account linked to [@{user.username}]({profile_url(user.username)}). You may unlink with {unlink_command.mention} if you wish."
        else:
            em.description = f"{discord_user.mention} is linked to [@{user.username}]({profile_url(user.username)})."
                
        return await ctx.interaction.edit_original_response(
            embeds=[profile_em, em]
        )
    
    else:
        user_cog = self.bot.get_cog("User")
        cmd = discord.utils.get(user_cog.__cog_commands__, name='verify')

        if discord_user == ctx.author:
            await ctx.interaction.edit_original_response(
                content=f"Your Discord account has not been linked to a Rec Room account! Feel free to link one with {cmd.mention}"
            )     
        else:
            await ctx.interaction.edit_original_response(
                content=f"{discord_user.mention} has not been linked to a Rec Room account."
            )  