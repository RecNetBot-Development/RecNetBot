import discord
from discord.interactions import Interaction
from utils.converters import FetchRoom
from utils import room_url, profile_url, shorten
from discord.commands import slash_command, Option
from embeds import room_embed
from bot import RecNetBot
from recnetpy.dataclasses.room import Room
from exceptions import RoomNotFound
from utils.autocompleters import room_searcher

class RoleBtn(discord.ui.Button):
    def __init__(self, command):
        super().__init__(
            label="View Roles",
            style=discord.ButtonStyle.primary
        )

        self.command = command

    async def callback(self, interaction: discord.Interaction):
        # Run /roles

        # Make sure it's the author using the component
        if not self.view.authority_check(interaction):
            return await interaction.response.send_message("You're not authorized!", ephemeral=True)

        ctx = await self.view.bot.get_application_context(interaction)
        await self.command(ctx, self.view.room)


class PlacementBtn(discord.ui.Button):
    def __init__(self, command):
        super().__init__(
            label="View Placement",
            style=discord.ButtonStyle.primary
        )

        self.command = command

    async def callback(self, interaction: discord.Interaction):
        # Run /placement

        # Make sure it's the author using the component
        if not self.view.authority_check(interaction):
            return await interaction.response.send_message("You're not authorized!", ephemeral=True)

        ctx = await self.view.bot.get_application_context(interaction)
        await self.command(ctx, self.view.room, None)


class RefreshBtn(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Refresh",
            style=discord.ButtonStyle.primary
        )

    async def callback(self, interaction: discord.Interaction):
        # Make sure it's the author using the component
        if not self.view.authority_check(interaction):
            return await interaction.response.send_message("You're not authorized!", ephemeral=True)

        # Refresh the room
        await self.view.fetch_room()
        
        # Create embed and respond
        if self.view.room:
            await self.view.update(interaction)
        else:
            await self.view.error(interaction)


class RoomView(discord.ui.View):
    def __init__(self, room: Room, bot: RecNetBot, only_stats: bool = False, commands: dict = {}):
        super().__init__()
        
        self.commands = commands
        self.room = room
        self.bot = bot
        self.author_id = 0
        self.only_stats = only_stats

        # Component timeout
        self.timeout = 600
        self.disable_on_timeout = True

        # Link buttons
        buttons = [
            RefreshBtn(),
            RoleBtn(commands["roles"]),
            PlacementBtn(commands["placement"]),
            discord.ui.Button(
                label=shorten(f"^{self.room.name}", 80),
                url=room_url(self.room.name),
                style=discord.ButtonStyle.link,
                row=1
            ),
            discord.ui.Button(
                label=f"@{self.room.creator_account.username}",
                url=profile_url(self.room.creator_account.username),
                style=discord.ButtonStyle.link,
                row=1
            )
        ]

        for i in buttons:
            self.add_item(i)

    async def on_timeout(self):
        # Method override to exempt link buttons from being disabled on timeout.
        if not self.disable_on_timeout: return
        for item in self.children:
            if isinstance(item, discord.ui.Button) and item.style == discord.ButtonStyle.link:
                continue
            item.disabled = True

    def get_embed(self):
        """
        Gets the embed and refreshes cache
        """
        
        cached_stats = self.bot.rcm.get_cached_stats(self.author_id, self.room.id)
        self.bot.rcm.cache_stats(self.author_id, self.room.id, self.room)

        embed = room_embed(self.room, cached_stats, self.only_stats)
        return embed
    
    async def fetch_room(self):
        """
        Fetches the room again for new statistics
        """
        room = await self.bot.RecNet.rooms.fetch(self.room.id, 78)
        if room: 
            self.room = room
        else:
            self.room = None
        
    async def respond(self, ctx: discord.ApplicationContext):
        self.author_id = ctx.author.id

        embed = self.get_embed()
        await ctx.respond(embed=embed, view=self)
        
    async def update(self, interaction: discord.Interaction):
        embed = self.get_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    def authority_check(self, interaction: discord.Interaction):
        return interaction.user.id == interaction.message.interaction.user.id
    
    async def error(self, interaction: discord.Interaction):
        """
        If the room doesn't exist anymore
        """
        await interaction.response.send_message("I couldn't find the room anymore! It either got privated, or I malfunctioned.", ephemeral=True)
        
@slash_command(
    name="info",
    description="View a room's information and statistics."
)
async def info(
    self, 
    ctx: discord.ApplicationContext, 
    room: Option(FetchRoom, name="name", description="Enter RR room", required=True, autocomplete=room_searcher),
    only_stats: Option(bool, name="only_stats", description="Whether or not to only display statistics and leave out details", required=False, default=False)
):
    await ctx.interaction.response.defer()
    
    await room.get_creator_player()
    
    # Get button commands
    commands = {
        "roles": None,
        "placement": None
    }
    for i in self.__cog_commands__:
        if i.name in commands:
            commands[i.name] = i

    view = RoomView(room, self.bot, only_stats, commands)
    await view.respond(ctx)

    
    

        

        
