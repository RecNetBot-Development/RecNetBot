from dataclasses import dataclass
import discord
from discord.ext import commands
from embeds import get_default_embed
from resources import get_emoji
from typing import List, Optional
from recnetpy.dataclasses.event import Event
from recnetpy.dataclasses.event_response import EventInteraction
from utils.converters import FetchEvent
from utils import chunks, profile_url, event_url, img_url
from discord.commands import slash_command, Option
from utils.paginator import RNBPaginator, RNBPage


class AttendeeView(discord.ui.View):
    def __init__(self, bot: commands.Bot, context: discord.ApplicationContext, event: Event):
        super().__init__()
        self.bot = bot
        self.ctx = context
        self.embeds = []
        self.paginator = None
        self.event = event
        self.responses = event.responses
        
        # Sort responses by the account's display_name
        self.responses.sort(key=lambda response: response.player.display_name)
        
        self.add_item(Dropdown(self))
        
    def initialize(self) -> discord.Embed:
        """
        Generates the first embed
        """
        
        self.register_selections(-1)
        return self.embeds
        
        
    def register_selections(self, selections: List[int]):
        """
        Takes in selected roles and creates embeds
        """
        
        if selections == -1:
            responsees = self.responses
        else:
            responsees = list(filter(lambda responsee: responsee.type in selections, self.responses))
            
            
        self.embeds = self.create_embeds(responsees)
        
    def create_embeds(self, responses: Optional[List[EventInteraction]]) -> discord.Embed:
        """
        Creates role page embeds
        """
        em = get_default_embed()
        em.title = f"{self.event.name}'s responses"
        em.url = event_url(self.event.id)
        
        image_name = self.event.image_name
        if image_name:
            em.set_thumbnail(image_name)
        
        if not responses:
            em.description = "No players found!"
            return [RNBPage(embeds=[em])]
            
        responsee_chunks, embeds = chunks(responses, 15), []
        for chunk in responsee_chunks:
            em, pieces = get_default_embed(), []
            em.title = f"{self.event.name}'s responses"
            em.url = event_url(self.event.id)
            if image_name:
                em.set_thumbnail(image_name)
            for responsee in chunk:
                pieces.append(
                    f"[{responsee.player.username}]({profile_url(responsee.player.username)}) • {responsee.type}"
                )
            
            em.description = "\n".join(pieces)
            embeds.append(RNBPage(embeds=[em]))
        
        return embeds
        
        
    async def refresh(self, interaction: discord.Interaction):
        #await interaction.response.edit_message(embed=self.embed, view=self)
        await interaction.response.defer(invisible=True)
        await self.paginator.update(pages=self.embeds, custom_view=self)
        
        
class Dropdown(discord.ui.Select):
    def __init__(self, view):
        self.attendee_view = view
        self.bot = self.attendee_view.bot
        self.responses = self.attendee_view.responses
        
        # Create selection options with cogs
        
        options = [
            discord.SelectOption(
                label=f"All ({len(self.responses)})"
            )
        ]
        
        # If attendees
        attendees = len(list(filter(lambda response: response.type == "Attending", self.responses)))
        if attendees:
            options.append(
                discord.SelectOption(
                    label=f"Attending ({attendees})"
                )
            )
        
        # If interested
        interested = len(list(filter(lambda response: response.type == "May Attend", self.responses)))
        if interested:
            options.append(
                discord.SelectOption(
                    label=f"Interested ({interested})"
                )
            )
        
        # If not attending
        not_attending = len(list(filter(lambda response: response.type == "Not Attending", self.responses)))
        if not_attending:
            options.append(
                discord.SelectOption(
                    label=f"Not Attending ({not_attending})"
                )
            )

        # If invited
        invited = len(list(filter(lambda response: response.type == "Pending", self.responses)))
        if invited:
            options.append(
                discord.SelectOption(
                    label=f"Invited ({invited})"
                )
            )

        super().__init__(
            placeholder="Select Responses",
            min_values=1,
            max_values=len(options),
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        """
        Returns chosen categories back to the view
        """
        
        response_types = {
            "Attending": "Attending",
            "Interested": "May Attend",
            "Not Attending": "Not Attending",
            "Invited": "Pending"
        }
        responses = list(map(lambda response: response_types.get(response.split(" (")[0], -1), self.values))
             
        # If all selected, make it the primary selection
        if -1 in responses:
            responses = -1
        
        self.attendee_view.register_selections(responses)
        await self.attendee_view.refresh(interaction)

@slash_command(
    name="responses",
    description="See who have responsed to an event."
)
async def responses(
    self, 
    ctx: discord.ApplicationContext, 
    event: Option(FetchEvent, name="event", description="Enter a RecNet link or id", required=True)
):
    await event.resolve_responders()
    view = AttendeeView(self.bot, context=ctx, event=event)
    embeds = view.initialize()
    paginator = RNBPaginator(pages=embeds, custom_view=view, show_indicator=False, show_disabled=True, trigger_on_display=True)
    view.paginator = paginator
    await paginator.respond(ctx.interaction)