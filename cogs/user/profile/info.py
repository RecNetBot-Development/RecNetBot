import discord
from discord.commands import slash_command, Option
from utils.converters import FetchAccount
from embeds import fetch_profile_embed
from resources import get_emoji
from exceptions import ConnectionNotFound
from recnetpy.dataclasses.account import Account

class ProfileView(discord.ui.View):
    def __init__(self, account: Account, ctx: discord.ApplicationContext):
        super().__init__()
        self.account = account
        self.ctx = ctx
        self.image_cog = self.ctx.bot.get_cog("Image")
        self.room_cog = self.ctx.bot.get_cog("Room")
        

    @discord.ui.button(label="Photos", style=discord.ButtonStyle.gray, emoji=get_emoji("image"))
    async def photos_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        cmd = discord.utils.get(self.image_cog.__cog_commands__, name='photos')
        await cmd(self.ctx, self.account)
        
        # Update the view with the disabled button
        button.disabled = True
        await interaction.response.edit_message(view=self)
        

    @discord.ui.button(label="Feed", style=discord.ButtonStyle.gray, emoji=get_emoji("image"))
    async def feed_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        cmd = discord.utils.get(self.image_cog.__cog_commands__, name='feed')
        await cmd(self.ctx, self.account)
        
        # Update the view with the disabled button
        button.disabled = True
        await interaction.response.edit_message(view=self)
        
    
    @discord.ui.button(label="Showcased Rooms", style=discord.ButtonStyle.gray, emoji=get_emoji("room"), row=2)
    async def showcased_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        cmd = discord.utils.get(self.room_cog.__cog_commands__, name='showcased')
        await cmd(self.ctx, self.account)
        
        # Update the view with the disabled button
        button.disabled = True
        await interaction.response.edit_message(view=self)
        

@slash_command(
    name="info",
    description="View a Rec Room profile with additional information.",
    
)
async def info(
    self,   
    ctx: discord.ApplicationContext,
    account: Option(FetchAccount, name="username", description="Enter RR username", default=None, required=False)
):
    await ctx.interaction.response.defer()
    
    if not account:  # Check for a linked RR account
        account = await self.bot.cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
    
    em = await fetch_profile_embed(account)
    view = ProfileView(account, ctx)
    await ctx.respond(
        embed=em,
        view=view
    )

        
