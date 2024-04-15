import discord
from discord.commands import slash_command
from discord.ext.bridge import BridgeOption as Option
from embeds import get_default_embed
from utils import room_url, img_url
from utils.autocompleters import room_searcher
from database import FeedManager, FeedTypes
from utils.converters import FetchRoom

class ChannelView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.interaction: discord.Interaction = None
        self.channel: discord.TextChannel = None
        self.cancelled = False

    @discord.ui.channel_select(
        placeholder="Channel", min_values=1, max_values=1, channel_types=[
            discord.ChannelType.text
        ]
    )
    async def channel_select_dropdown(
        self, select: discord.ui.Select, interaction: discord.Interaction
    ) -> None:
        await interaction.response.defer()
        self.channel = select.values[0]
        self.interaction = interaction
        self.stop()

    @discord.ui.button(
        label="This Channel", style=discord.ButtonStyle.blurple
    )
    async def current_channel_button(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.defer()
        self.channel = interaction.channel
        self.interaction = interaction
        self.stop()

    @discord.ui.button(
        label="Cancel", style=discord.ButtonStyle.red
    )
    async def cancel_button(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.defer()
        self.cancelled = True
        self.interaction = interaction
        self.stop()

@slash_command(
    name="subscribe",
    description="Get room images"
)
async def subscribe(
    self, 
    ctx: discord.ApplicationContext, 
    room: Option(FetchRoom, name="name", description="Enter RR room", required=True, autocomplete=room_searcher),
):
    await ctx.interaction.response.defer()

    #Make sure the bot can create webhooks
    if not ctx.app_permissions.manage_webhooks:
        await ctx.respond("Missing permissions! `Manage Webhooks`")
        return

    # Create the view containing our dropdown
    view = ChannelView()

    # Sending a message containing our View
    em = get_default_embed(
        title="Select Channel",
        description=
            f"Which channel should I send the latest images of [^{room.name}](<{room_url(room.name)}>) to?" \
            "\n\nIf you can't find your desired channel, run this command in the channel and press the 'This Channel' button.",
        footer=discord.EmbedFooter(text="Note: You can type the channel name into the dropdown menu."),
        image=discord.EmbedMedia(url=img_url(room.image_name, resolution=480))
    )
    await ctx.respond("Select channel", embed=em, view=view)

    await view.wait()
    if view.cancelled:
        await view.interaction.delete_original_message()
        return
    elif view.channel == None:
        await view.interaction.delete_original_message()
        return 
    
    # Interaction from dropdown menu
    interaction = view.interaction

    # Chosen channel
    channel = view.channel

    # Create webhook and feed
    fcm: FeedManager = self.bot.fcm

    # See if I can create a webhook in the specified channel
    if hasattr(channel, "create_webhook"):
        try:
            # Attempt to create a webhook
            webhook = await channel.create_webhook(name=f"^{room.name} Webhook", reason="Tracks room pictures. Created by RecNetBot.")
        except discord.errors.Forbidden:
            # Lacking permissions in channel
            await interaction.edit_original_response(content=f"I don't have permission to create a webhook in {channel.mention}! Please update the channel permissions.", embed=None, view=None)
            return
    else:
        # Channel doesn't support creating webhooks!
        await interaction.edit_original_response(content=f"{channel.mention} is not supported! I must be able to create a webhook there. Try a regular channel.", embed=None, view=None)
        return
    
    # Save feed into database
    await fcm.create_feed(ctx.author.id, ctx.guild_id, webhook.id, channel.id, FeedTypes.IMAGE, room.id)

    # Inform user
    await interaction.edit_original_response(
        content=f"Subscribed {channel.mention} to the latest photos from [^{room.name}](<{room_url(room.name)}>)\n\n" \
                f"In order to unsubscribe, please delete the `{webhook.name}` webhook from the channel's integrations!", 
        view=None, embed=None
    )

    # Feeds are handled in tasks/update_feeds.py

    
    

        

        
