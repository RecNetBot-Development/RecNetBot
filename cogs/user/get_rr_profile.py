import discord
from discord import ApplicationContext
from discord.commands import user_command
from utils import get_linked_account
from exceptions import ConnectionNotFound, AccountNotFound

@user_command(name="Rec Room Profile")
async def get_rr_profile(self, ctx: ApplicationContext, member: discord.Member):
    account = await get_linked_account(self.bot.cm, self.bot.RecNet, ctx.author.id)
    
    # Run the profile command with the RR username
    command = discord.utils.get(self.__cog_commands__, name='profile')
    await command(ctx, account)