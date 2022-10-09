import discord
from discord import ApplicationContext
from discord.commands import user_command
from exceptions import ConnectionNotFound

@user_command(name="Rec Room Profile")
async def get_rr_profile(self, ctx: ApplicationContext, member: discord.Member):
    account = await self.bot.cm.get_linked_account(self.bot.RecNet, ctx.author.id)
    if not account: raise ConnectionNotFound
    
    # Run the profile command with the RR username
    command = discord.utils.get(self.__cog_commands__, name='profile')
    await command(ctx, account)