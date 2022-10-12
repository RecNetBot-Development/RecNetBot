import discord
from discord import ApplicationContext
from discord.commands import user_command
from exceptions import ConnectionNotFound

@user_command(name="Showcased Rooms")
async def get_showcased_rooms(self, ctx: ApplicationContext, member: discord.Member):
    account = await self.bot.cm.get_linked_account(self.bot.RecNet, ctx.author.id)
    if not account: raise ConnectionNotFound
    
    # Run the showcased command with the RR username
    command = discord.utils.get(self.__cog_commands__, name='showcased')
    await command(ctx, account)