import discord
from discord.commands import slash_command, Option
from utils.converters import FetchAccount
from embeds import fetch_profile_embed
from resources import get_emoji
from exceptions import ConnectionNotFound
from database import BookmarkTypes
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
        
        
    @discord.ui.button(label="Bookmark", style=discord.ButtonStyle.gray, row=2)
    async def showcased_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        # Update the view with the disabled button
        button.disabled = True
        button.label = "Bookmarked!"
        await interaction.response.edit_message(view=self)
        
        self.ctx.bot.bcm.create_bookmark(self.ctx.author.id, BookmarkTypes.ACCOUNTS, self.account.id)

@slash_command(
    name="info",
    description="View a player's profile.",
    
)
async def info(
    self,   
    ctx: discord.ApplicationContext,
    account: Option(FetchAccount, name="username", description="Enter RR username", default=None, required=False)
):
    await ctx.interaction.response.defer()
    
    link_discord = None
    if not account:  # Check for a linked RR account
        account = await self.bot.cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
        link_discord = str(ctx.author)
    else:
        link_discord = self.bot.cm.get_rec_room_connection(account.id)
    
    # Fetch the profile embed
    em = await fetch_profile_embed(account)
    
    # Add linked Discord user to footer if exists
    if link_discord:
        if isinstance(link_discord, str):
            em.set_footer(text=f"Linked to {link_discord}")
        else:
            user = await self.bot.fetch_user(link_discord.discord_id)
            if user:
                em.set_footer(text=f"Linked to {user}")
    else:
        em.set_footer(text="Not linked to a Discord account.")
    
    await ctx.respond(
        embed=em,
        #view=view
    )

        
