import discord
from discord.commands import slash_command
from discord.ext.bridge import BridgeOption as Option
from embeds import get_default_embed
from utils import room_url, img_url, BaseView, load_config
from resources import get_icon
from utils.autocompleters import room_searcher
from database import FeedManager, FeedTypes
from utils.converters import FetchRoom
from tasks import add_room

config = load_config(is_production=True)
def is_developer(discord_user_id) -> bool:
    return discord_user_id in config.get("developers")

class ChannelView(BaseView):
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
        await interaction.response.defer(ephemeral=True)
        
        # Make sure the correct user responds
        if not self.authority_check(interaction):
            await interaction.followup.send("You're not authorized!", ephemeral=True)
            return
        
        self.channel = select.values[0]
        self.interaction = interaction
        self.stop()

    @discord.ui.button(
        label="This Channel", style=discord.ButtonStyle.blurple
    )
    async def current_channel_button(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.defer(ephemeral=True)
        
        # Make sure the correct user responds
        if not self.authority_check(interaction):
            await interaction.followup.send("You're not authorized!", ephemeral=True)
            return
        
        self.channel = interaction.channel
        self.interaction = interaction
        self.stop()

    @discord.ui.button(
        label="Cancel", style=discord.ButtonStyle.red
    )
    async def cancel_button(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.defer(ephemeral=True)
        
        # Make sure the correct user responds
        if not self.authority_check(interaction):
            await interaction.followup.send("You're not authorized!", ephemeral=True)
            return
        
        self.cancelled = True
        self.interaction = interaction
        self.stop()

@slash_command(
    name="create",
    description="Create a webhook that continuously sends the latest photos taken in a specified room."
)
async def create(
    self, 
    ctx: discord.ApplicationContext, 
    room: Option(FetchRoom, name="room", description="Enter room name", required=True, autocomplete=room_searcher),
):
    await ctx.interaction.response.defer()

    # How many feeds can a user create
    max_feeds = 2

    # Support server link
    server_link = ctx.bot.config.get('server_link')

    # Forbid threads
    if type(ctx.interaction.channel) is discord.threads.Thread:
        await ctx.respond(
            "You can't create photo feeds in threads! [|=(]\n\n" \
            f"If this is a mistake, reach out to us [here](<{server_link}>)."
        )
        return

    # Make sure user is admin in server
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond(
            "Only server administrators can create photo feeds! [|=(]\n\n" \
            f"If this is a mistake, reach out to us [here](<{server_link}>)."
        )
        return

    #Make sure the bot can create webhooks
    if not ctx.app_permissions.manage_webhooks:
        await ctx.respond(
            f"Missing permission: `Manage Webhooks`. [|=(]\n" \
            f"Make sure there's no permission conflicts with roles and this channel allows webhooks.\n\n"
            f"I need this permission to create a webhook that sends the latest photos taken in [^{room.name}](<{room_url(room.name)}>).\n\n" \
            f"If you have trouble setting this up, reach out to us [here](<{server_link}>).\n\n" \
            f"[Permission](https://i.imgur.com/JesFZxb.png)"
        )
        return
    
    # Get feed database manager
    fcm: FeedManager = self.bot.fcm

    # /feed delete
    group = discord.utils.get(self.__cog_commands__, name='feed')
    destroy_cmd = discord.utils.get(group.walk_commands(), name='delete')

    # Check if the user has made more than 2 feeds
    feed_count = await fcm.get_feed_count_by_user(ctx.author.id)
    if feed_count >= max_feeds and not is_developer(ctx.author.id):
        await ctx.respond(
            f"You have reached the limit of {max_feeds} photo feeds. Please delete previous feeds.\n\n" \
            f"You can delete feeds using {destroy_cmd.mention}.\n\n" \
            f"This is an early access limitation. It is subject to change in the future. Reach out in [my test server](<{server_link}>) for any concerns."
        )
        return

    # Create the view containing our dropdown
    view = ChannelView()

    # Sending a message containing our View
    em = get_default_embed(
        title="Create Photo Feed",
        thumbnail=discord.EmbedMedia(url=get_icon("photo_add")),
        fields=[
            discord.EmbedField(
                name="Select Channel",
                value=f"Which channel should I create the photo feed webhook for [^{room.name}](<{room_url(room.name)}>) in?",
                inline=False
            ),
            discord.EmbedField(
                name="What Does This Do?",
                value="RecNetBot will treat the channel as a live feed of the room. Any new shared photos in the room will be sent in the channel. " \
                      "You can always disable the feature.",
                inline=False
            ),
            discord.EmbedField(
                name="Tip",
                value="If you can't find your desired channel, run this command in the channel and press the 'This Channel' button.",
                inline=False
            )
        ],
        footer=discord.EmbedFooter(text="Note: You can type the channel name into the dropdown menu."),
        image=discord.EmbedMedia(url=img_url(room.image_name, resolution=480))
    )

    await ctx.respond(embed=em, view=view)
    
    if feed_count == 0:
        await ctx.followup.send(
            "This is an early access feature! By testing this feature, you're helping us polish it.\n\n" \
            f"For now you can only create **{max_feeds}** photo feeds in total. You have `{max_feeds - feed_count}` feed slots left. You can always delete created feeds.\n\n"
            f"If you have any suggestions, issues or encounter any bugs, please please *please* let us know in [my test server](<{server_link}>)! " \
            "Your feedback is super-duper valuable to us. You'll also be kept up-to-date of any updates.\n\n" \
            "Please note that old feeds **MAY** be deleted once the feature leaves early access.\n\n" \
            "Thanks for trying this feature out! <3", 
            ephemeral=True
        )


    # Wait for response
    await view.wait()
    if view.cancelled:
        await view.interaction.delete_original_response()
        return
    elif view.channel == None:
        await view.interaction.delete_original_response()
        return 
    
    # Interaction from dropdown menu
    interaction = view.interaction

    # Chosen channel
    channel = view.channel

    # Returns existing feeds in channel and their RR ids
    rr_ids = await fcm.get_feed_rr_ids_in_channel(channel.id)

    # Don't let user create 2 same feeds in channel
    if room.id in rr_ids and not is_developer(ctx.author.id):
        await ctx.respond(f"You have already created a photo feed of ^{room.name} in {channel.mention}! [|=(]")
        return

    # See if I can create a webhook in the specified channel
    if hasattr(channel, "create_webhook"):
        try:
            # Attempt to create a webhook
            webhook = await channel.create_webhook(name=f"^{room.name} Webhook", reason="Tracks room photos. Created by RecNetBot.")
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
    
    # Tell update_feed() task to add new room
    add_room(room)

    # Inform user
    em = get_default_embed(
        title="Photo Feed",
        thumbnail=discord.EmbedMedia(url=img_url(room.image_name, resolution=180, crop_square=True)),
        fields=[
            discord.EmbedField(
                name="Success!",
                value=f"Subscribed {channel.mention} to the latest photos from [^{room.name}](<{room_url(room.name)}>)!",
                inline=False
            ),
            discord.EmbedField(
                name="Disable",
                value=f"Use {destroy_cmd.mention} to delete feeds.",
                inline=False
            ),
            discord.EmbedField(
                name="Captions",
                value="Photos with captions will be edited into the sent image. If you own the room, we recommend informing users about it in-game!",
                inline=False
            )
        ],
        image=discord.EmbedMedia(url="https://i.imgur.com/KypV0Do.png")
    )

    await interaction.edit_original_response(embed=em, view=None)

    # Feeds are handled in tasks/update_feeds.py

        
