import discord
import asyncpg
import matplotlib.pyplot as plt
import os
from utils import unix_timestamp, room_url
from utils.converters import FetchRoom
from discord.commands import slash_command
from discord.ext.bridge import BridgeOption as Option
from embeds import room_embed
from discord.ext import tasks
from recnetpy.dataclasses.room import Room
from bot import RecNetBot
from discord.ext.commands import Context
from datetime import datetime, timedelta

class TrackView(discord.ui.View):
    def __init__(self, room: Room, author, bot: RecNetBot):
        super().__init__()
        
        self.room = room  # The room to track
        self.author = author  # The user who ran the command
        self.bot = bot  # RecNetBot
        self.interaction_msg: discord.InteractionMessage = None
        self.graph_path = f"temporary/graphs/graph-{self.author.id}.png"  # Where the graphs are stored at
        self.minimum_loops = 5  # How many loops it takes to generate graphs
        self.next_graph_datetime = None  # When the next graph will be generated
        self.msg = None
        
        self.old_stats = {
            "visits": room.visit_count,
            "visitors": room.visitor_count,
            "cheers": room.cheer_count
        }
        
        self.stats = {
            "visits": [room.visit_count],
            "visitors": [room.visitor_count],
            "cheers": [room.cheer_count],
            "minutes": [0]
        }

    def get_embed(self):
        cached_stats = self.bot.rcm.get_cached_stats(self.author.id, self.room.id)
        self.bot.rcm.cache_stats(self.author.id, self.room.id, self.room)
        
        em = room_embed(self.room, cached_stats, True)
        em.set_footer(text=f"Initiated by {self.author}")
        
        return em
    
    async def start(self, ctx: Context):
        """
        Initial response and initialization
        """
        
        # Delete an existing graph
        if os.path.exists(self.graph_path): 
            os.remove(self.graph_path)
        
        self.track_room.add_exception_type(asyncpg.PostgresConnectionError)
        self.track_room.start(ctx, self.bot, self.room)
        
    def make_graph(self, room: Room):
        """
        Makes the graph
        """
        self.stats["minutes"].append(
            int(self.stats["minutes"][-1] + self.track_room.minutes)
        )
        
        # Get stats
        self.stats["visits"].append(room.visit_count - sum(self.stats["visits"]))
        self.stats["visitors"].append(room.visitor_count - sum(self.stats["visitors"]))
        self.stats["cheers"].append(room.cheer_count - sum(self.stats["cheers"]))
        
        # Do every 'self.minimum_loops' times
        if self.track_room.current_loop % self.minimum_loops == 0 and self.track_room.current_loop != 0:
            # Change the style
            plt.style.use('ggplot')
            
            plt.plot(self.stats["minutes"][2:], self.stats["visits"][2:], label="Visits", 
                linestyle='dashed', linewidth = 3, marker='o', markersize=12
            )
            plt.plot(self.stats["minutes"][2:], self.stats["visitors"][2:], label="Visitors", 
                linestyle='dashed', linewidth = 3, marker='o', markersize=12
            )
            plt.plot(self.stats["minutes"][2:], self.stats["cheers"][2:], label="Cheers", 
                linestyle='dashed', linewidth = 3, marker='o', markersize=12
            )
            
            # show a legend on the plot
            plt.legend()
            
            plt.title(f'^{room.name} Statistics')
            plt.xlabel('Minutes')
            plt.ylabel('Amount')
            
            print(self.stats)
            
            plt.savefig(self.graph_path)
            
            plt.clf()
        
        
    @tasks.loop(minutes=1)
    async def track_room(self, ctx, bot: RecNetBot, room: Room):
        # Fetch new statistics
        room = await bot.RecNet.rooms.fetch(room.id, 64)
        
        # Make graph
        self.make_graph(room)
        
        # Make embed
        embed = self.get_embed()
        
        # Next update indicator
        dt = datetime.now()
        td = timedelta(minutes=self.track_room.minutes)
        update_datetime = dt + td
        update_text = f"Next update {unix_timestamp(int(update_datetime.timestamp()), 'R')}"
        
        # Only let the graph button be sent if a graph exists
        graph_button = discord.utils.get(self.children, label='Graph')
        graph_button.disabled = not os.path.exists(self.graph_path)
        
        # Add indicator on when a new graph will be generated
        if self.track_room.current_loop % self.minimum_loops == 0:
            td = timedelta(minutes=self.track_room.minutes * self.minimum_loops)
            graph_datetime = dt + td
            self.next_graph_datetime = graph_datetime
                
        if self.next_graph_datetime:
            update_text += f"\nNew graph {unix_timestamp(int(self.next_graph_datetime.timestamp()), 'R')}"
        
        # Respond or edit
        if self.msg:
            await self.msg.edit(content=update_text, embed=embed, view=self)
        else:
            self.msg = await ctx.send(content=update_text, embed=embed, view=self)
        
    @track_room.before_loop
    async def before_tracking(self):
        await self.bot.wait_until_ready()
   
    @discord.ui.button(label="Graph", style=discord.ButtonStyle.primary)
    async def show_graph(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        Sends the latest graph
        """
        if os.path.exists(self.graph_path): 
            # Sends the graph
            await interaction.response.send_message(file=discord.File(self.graph_path), ephemeral=True)
            
            # Deletes it
            os.remove(self.graph_path)
        else:
            await interaction.response.send_message(content="A graph hasn't been generated yet!", ephemeral=True)
        
        # Disable the button to prevent trying to send a non-existent graph
        button.disabled = True  
        
        # Edit the embed to disable the button
        await self.msg.edit(view=self)
    
    @discord.ui.button(label="Stop", style=discord.ButtonStyle.danger)
    async def stop(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        Stops tracking the room
        """
        self.track_room.stop()
         
        # Indicate that it was successful
        await interaction.response.send_message("Stopped tracking the room!", ephemeral=True)
        
        # Disable the button
        #button.disabled = True
        
        # Edit the embed to disable the buttons
        await self.msg.edit(content="", view=None)


@slash_command(
    name="track",
    description="Automatically update and track room statistics."
)
async def track(
    self, 
    ctx: discord.ApplicationContext, 
    room: Option(FetchRoom, name="name", description="Enter RR room", required=True)
):
    await ctx.interaction.response.send_message(content=f"Started tracking [^RecCenter](<{room_url(room.name)}>)", ephemeral=True)
    view = TrackView(room=room, author=ctx.author, bot=self.bot)
    await view.start(ctx)




