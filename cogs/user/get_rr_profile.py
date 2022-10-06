import discord
from discord import ApplicationContext
from discord.commands import user_command
from exceptions import ConnectionNotFound, AccountNotFound

@user_command(name="Rec Room Profile")
async def get_rr_profile(self, ctx: ApplicationContext, member: discord.Member):
    connections = self.bot.cm.get_discord_connection(ctx.author.id)
    if not connections: raise ConnectionNotFound
    user = await self.bot.RecNet.accounts.fetch(connections.rr_id)
    if not user: raise AccountNotFound
    
    # Run the profile command with the RR username
    command = discord.utils.get(self.__cog_commands__, name='profile')
    await command(ctx, user.username)