import discord
from utils.converters import FetchRoom
from discord.commands import slash_command, Option
from embeds import room_embed
from bot import RecNetBot
from recnetpy.dataclasses.room import Room
from exceptions import RoomNotFound

class RoomView(discord.ui.View):
    def __init__(self, room: Room, bot: RecNetBot, author_id: int, only_stats: bool = False):
        super().__init__()
        
        self.room = room
        self.bot = bot
        self.author_id = author_id
        self.only_stats = only_stats
        
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
        
    @discord.ui.button(label="Refresh")
    async def refresh(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Refresh the room
        await self.fetch_room()
        
        # Create embed and respond
        if self.room:
            embed = self.get_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.send_message("I couldn't find the room anymore! It either got privated, or I malfunctioned.", ephemeral=True)


@slash_command(
    name="info",
    description="View a room's information and statistics."
)
async def info(
    self, 
    ctx: discord.ApplicationContext, 
    room: Option(FetchRoom, name="name", description="Enter RR room", required=True),
    only_stats: Option(bool, name="only_stats", description="Whether or not to only display statistics and leave out details", required=False, default=False)
):
    await ctx.interaction.response.defer()
    
    view = RoomView(room, self.bot, ctx.author.id, only_stats)
    await view.respond(ctx)

    
    

        

        
