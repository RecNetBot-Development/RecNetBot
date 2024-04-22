import discord
from discord.commands import slash_command
from discord.ext.bridge import BridgeOption as Option
from utils.converters import FetchAccount
from utils.autocompleters import account_searcher
from utils import profile_url
from embeds import fetch_profile_embed
from exceptions import ConnectionNotFound
from recnetpy.dataclasses.account import Account
from utils import BaseView
from database import ConnectionManager

class UserBtn(discord.ui.Button):
    def __init__(self, title: str, command):
        super().__init__(
            label=title,
            style=discord.ButtonStyle.primary
        )

        self.command = command

    async def callback(self, interaction: discord.Interaction):
        # Make sure it's the author using the component
        if not self.view.authority_check(interaction):
            return await interaction.response.send_message("You're not authorized!", ephemeral=True)

        ctx = await interaction.client.get_application_context(interaction)
        await self.command(ctx, self.view.account)


class ProfileView(BaseView):
    def __init__(self, account: Account, commands: dict):
        super().__init__()

        # Component timeout
        self.timeout = 600
        self.disable_on_timeout = True

        # The account in question
        self.account = account

        # Commands for buttons
        self.commands = commands

        # Link buttons
        buttons = [
            UserBtn("Level Progression", self.commands["User"]["xp"]) if account.level.level < 50 else None,
            UserBtn("Photos", self.commands["Image"]["photos"]),
            UserBtn("Profile Picture", self.commands["User"]["pfp"]),
            UserBtn("Banner", self.commands["User"]["banner"]) if account.banner_image else None,
            discord.ui.Button(
                label=f"@{self.account.username}",
                url=profile_url(self.account.username),
                style=discord.ButtonStyle.link,
                row=1
            )
        ]

        for i in buttons:
            # Ignore NoneTypes
            if i: self.add_item(i)


@slash_command(
    name="info",
    description="View a player's profile.",
    
)
async def info(
    self,   
    ctx: discord.ApplicationContext,
    account: Option(
        FetchAccount, 
        name="username", 
        description="Enter RR username", 
        default=None, 
        required=False, 
        autocomplete=account_searcher
    )
):
    await ctx.interaction.response.defer()
    
    link_discord = None
    cm: ConnectionManager = self.bot.cm
    if not account:  # Check for a linked RR account
        account = await cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
        link_discord = str(ctx.author)
    else:
        link_discord = await cm.get_rec_room_connection(account.id)
    
    # Fetch the profile embed
    em = await fetch_profile_embed(account)
    
    # Add linked Discord user to footer if exists
    if link_discord:
        if isinstance(link_discord, str):
            em.set_footer(text=f"Linked to {link_discord}")
        else:  # must be an int
            user = await self.bot.fetch_user(link_discord)
            if user:
                em.set_footer(text=f"Linked to @{user}")
    else:
        em.set_footer(text="Not linked to a Discord account.")
    
    # Get button commands
    commands = {
        "User": {
            "xp": None,
            "banner": None,
            "pfp": None
        },
        "Image": {
            "photos": None
        }  
    }

    # Get the amount of commands needed so we can stop the following iteration
    command_count = 0
    for i in commands:
        command_count += len(commands.keys())

    # Fetch commands to display
    cogs = self.bot.cogs.values()

    # Find the wanted commands
    found_commands = 0
    for cog in cogs:
        for cmd in cog.walk_commands():
            # We found them all!
            if found_commands >= command_count: break

            if cog.qualified_name in commands:
                if cmd.name in commands[cog.qualified_name]:
                    commands[cog.qualified_name][cmd.name] = cmd
                    found_commands += 1

    await ctx.respond(
        embed=em,
        view=ProfileView(account=account, commands=commands)
    )

        
