import discord
from utils.converters import FetchRoom
from utils import room_url, profile_url
from discord.commands import slash_command, Option
from embeds import room_embed
from bot import RecNetBot
from recnetpy.dataclasses.room import Room
from exceptions import RoomNotFound
from utils.autocompleters import room_searcher

class RoomView(discord.ui.View):
    def __init__(self, room: Room, bot: RecNetBot, author_id: int, only_stats: bool = False, commands: dict = {}):
        super().__init__()
        
        self.commands = commands
        self.room = room
        self.bot = bot
        self.author_id = author_id
        self.only_stats = only_stats

        # Link buttons
        buttons = [
            discord.ui.Button(
                label=f"^{self.room.name}",
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
            
        
    async def respond(self, ctx):
        embed = self.get_embed()
        await ctx.respond(embed=embed, view=self)
        
    @discord.ui.button(label="Refresh", style=discord.ButtonStyle.primary)
    async def refresh(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Refresh the room
        await self.fetch_room()
        
        # Create embed and respond
        if self.room:
            embed = self.get_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.send_message("I couldn't find the room anymore! It either got privated, or I malfunctioned.", ephemeral=True)

    @discord.ui.button(label="View Roles", style=discord.ButtonStyle.primary)
    async def roles(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Run /roles

        # Make sure it's the author using the component
        if interaction.user.id != interaction.message.interaction.user.id:
            return await interaction.response.send_message("You're not authorized!", ephemeral=True)

        ctx = await self.bot.get_application_context(interaction)
        await self.commands["roles"](ctx, self.room)

    @discord.ui.button(label="View Placement", style=discord.ButtonStyle.primary)
    async def placement(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Run /placement

        # Make sure it's the author using the component
        if interaction.user.id != interaction.message.interaction.user.id:
            return await interaction.response.send_message("You're not authorized!", ephemeral=True)

        ctx = await self.bot.get_application_context(interaction)
        await self.commands["placement"](ctx, self.room, None)
        

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

    view = RoomView(room, self.bot, ctx.author.id, only_stats, commands)
    await view.respond(ctx)

    
    

        

        
