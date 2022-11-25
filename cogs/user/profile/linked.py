import discord
from discord import ApplicationContext
from discord.commands import slash_command, Option
from discord.ext.commands import cooldown, BucketType
from exceptions import AccountNotFound, ConnectionAlreadyDone
from embeds import get_default_embed, fetch_profile_embed
from utils import post_url, profile_url, unix_timestamp
from datetime import datetime, timedelta

# User can only run the command once every "per" seconds
@slash_command(
    name="linked",
    description="Check what Rec Room account is linked to your Discord."
)
async def linked(
    self, 
    ctx: ApplicationContext
):
    await ctx.interaction.response.defer(ephemeral=True)
    
    # Check if Discord user has already linked an account
    check_discord = self.bot.cm.get_discord_connection(ctx.author.id)
    if check_discord:
        user = await self.bot.RecNet.accounts.fetch(check_discord.rr_id)
        
        profile_em = await fetch_profile_embed(user)
        em = get_default_embed()
        group = discord.utils.get(self.__cog_commands__, name='profile')
        unlink_command = discord.utils.get(group.walk_commands(), name='unlink')
        em.description = f"You are linked to [@{user.username}]({profile_url(user.username)})."
        
        return await ctx.interaction.edit_original_response(
            embeds=[profile_em, em]
        )
    
    else:
        group = discord.utils.get(self.__cog_commands__, name='profile')
        unlink_command = discord.utils.get(group.walk_commands(), name='link')
        await ctx.interaction.edit_original_response(
            content=f"Your Discord account has no linked Rec Room account! Feel free to link one with {unlink_command.mention}"
        )     