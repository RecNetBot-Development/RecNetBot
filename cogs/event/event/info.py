import discord
from discord.commands import slash_command, Option
from utils import event_url
from utils.converters import FetchEvent
from embeds import fetch_event_embed
from recnetpy.dataclasses import Event

class EventView(discord.ui.View):
    def __init__(self, event: Event, commands: dict):
        super().__init__()

        self.event = event
        self.command = commands
        self.timeout = 600
        self.disable_on_timeout = True

        # Link button
        btn = discord.ui.Button(
            label="Event URL",
            url=event_url(self.event.id),
            style=discord.ButtonStyle.url
        )
        self.add_item(btn)

    @discord.ui.button(label="Attendees", style=discord.ButtonStyle.primary)
    async def responses(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Make sure it's the author using the component
        if interaction.user.id != interaction.message.interaction.user.id:
            return await interaction.followup.send("You're not authorized!", ephemeral=True)

        ctx = await interaction.client.get_application_context(interaction)
        await self.command(ctx, self.event)

        # Disable button to prevent spam
        button.disabled = True

        await interaction.edit_original_response(view=self)

@slash_command(
    name="info",
    description="View an event's details."
)
async def info(
    self, 
    ctx: discord.ApplicationContext, 
    event: Option(FetchEvent, name="event", description="Enter a RecNet link or ID", required=True)
):
    await ctx.interaction.response.defer()

    # Fetch commands to display
    cogs = self.bot.cogs.values()

    event_cog = discord.utils.get(cogs, qualified_name="Event")
    responses_cmd = discord.utils.get(event_cog.walk_commands(), name="responses")

    em = await fetch_event_embed(event)
    view = EventView(event, responses_cmd)
    await ctx.respond(embed=em, view=view)
