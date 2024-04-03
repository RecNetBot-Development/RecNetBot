import discord
from discord import ApplicationContext
from discord.commands import slash_command, Option
from discord.ext.commands import cooldown, BucketType
from exceptions import AccountNotFound, ConnectionAlreadyDone
from embeds import get_default_embed, fetch_profile_embed
from utils import post_url, profile_url, unix_timestamp
from resources import get_emoji, get_icon
from datetime import datetime, timedelta
from utils.autocompleters import account_searcher
from database import ConnectionManager

BENEFITS = "- autofill the `username` slot in commands\n" \
           "- list your owned rooms in `room` slots so you don't have to type them out."

# For prompting the user whether or not to link the account
class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Link", style=discord.ButtonStyle.green)
    async def confirm_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.defer(invisible=True)
        self.value = True
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
    async def cancel_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.defer(invisible=True)
        self.value = False
        self.stop()


# For checking if the user has cheered the post
class Check(discord.ui.View):
    def __init__(self, post_id: int = 1):
        super().__init__(timeout=600)
        self.value = None
        
        # Add link to the verification post
        link_button = discord.ui.Button(
            label="Verification Post",
            style=discord.ButtonStyle.link, 
            url=post_url(post_id)
        )
        self.add_item(link_button)

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green)
    async def confirm_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.defer(invisible=True)
        self.value = True
        self.stop()

# User can only run the command once every "per" seconds
@slash_command(
    name="verify",
    description="Verify your Rec Room profile!"
)
@cooldown(rate=2, per=300, type=BucketType.user)
async def verify(
    self, 
    ctx: ApplicationContext, 
    username: Option(str, "Enter RR username", required=True, autocomplete=account_searcher)
):
    await ctx.interaction.response.defer(ephemeral=True)
    
    # Check if Discord user has already linked an account
    cm: ConnectionManager = self.bot.cm
    rr_id = await cm.get_discord_connection(ctx.author.id)
    if rr_id:
        user = await self.bot.RecNet.accounts.fetch(rr_id)
        
        profile_em = await fetch_profile_embed(user)
        em = get_default_embed()
        group = discord.utils.get(self.__cog_commands__, name='profile')
        unlink_command = discord.utils.get(group.walk_commands(), name='unlink')
        em.description = f"You are already linked to [@{user.username}]({profile_url(user.username)}). If you'd like, you can unlink the account with {unlink_command.mention}."
        
        return await ctx.interaction.edit_original_response(
            embeds=[profile_em, em]
        )
    
    # Check if RR account exists
    user = await self.bot.RecNet.accounts.get(username)
    if not user: raise AccountNotFound
    
    # Check if RR account is already linked
    check_rr = await cm.get_rec_room_connection(user.id)
    if check_rr: raise ConnectionAlreadyDone
    
    # Prompt the user
    profile_em = await fetch_profile_embed(user)
    prompt_em = get_default_embed()
    prompt_em.description = '\n'.join([
        f"Are you sure you want to link [@{user.username}]({profile_url(user.username)}) to your Discord?",
        "You can only link a Rec Room account that you own. Verification is required. It only takes less than a minute."
    ])
    prompt_em.add_field(name="Benefits", 
        value="Once linked, RecNetBot will:\n" + BENEFITS
    )
    view = Confirm()
    
    # Edit to verification phase
    await ctx.interaction.edit_original_response(
        embeds=[profile_em, prompt_em],
        view=view
    )
    
    await view.wait()
    if view.value is None:
        return await ctx.interaction.edit_original_response(content="Timed out! Try again later.", embeds=[], view=None)
    elif view.value is False:
        return await ctx.interaction.edit_original_response(content="Cancelled linking! You can try again later.", embeds=[], view=None)
        
    # Fetch cheers from verify post
    post = self.bot.verify_post
    cheer_list = await post.get_cheers(force=True)
            
    # Verification process
    cheered = user.id in cheer_list
    specify = "Uncheer from" if cheered else "Cheer"
    demonstration = "https://i.imgur.com/adYnPLi.gif" if cheered else "https://i.imgur.com/5VMBcJw.gif"
    
    # Send verification steps
    view = Check(post_id=post.id)
    
    # Get timeout date
    dt = datetime.now()
    td = timedelta(seconds=view.timeout)
    timeout_datetime = dt + td
    
    verify_em = get_default_embed()
    verify_em.title = "Verification Steps"
    verify_em.description = "\n".join(
        [
            f"1. {specify} [this RecNet post]({post_url(post.id)}) to verify that you own the account.",
            "2. Press the Verify button.",
            f"\nThis expires {unix_timestamp(int(timeout_datetime.timestamp()), 'R')}."
        ]
    )
    verify_em.set_footer(text=f"You can only press the verify button once.")
    verify_em.set_thumbnail(url=demonstration)
    await ctx.interaction.edit_original_response(embed=verify_em, view=view)
    
    await view.wait()
    if view.value is None:
        await cm.delete_connection(ctx.author.id)
        return await ctx.interaction.edit_original_response(content="Verification timed out! Try again later.", embeds=[], view=None)
    elif view.value is False:
        await cm.delete_connection(ctx.author.id)
        return await ctx.interaction.edit_original_response(content="Could not verify the account's ownership. Try again later.", embeds=[], view=None)
    
    # Check status
    cheer_list = await post.get_cheers(force=True)
    if cheered and user.id in cheer_list or not cheered and user.id not in cheer_list:    
        # Failed to verify
        await cm.delete_connection(ctx.author.id)
        return await ctx.interaction.edit_original_response(content="Could not verify the account's ownership. Try again later.", embeds=[], view=None)
        
    # One more security check
    if await cm.get_rec_room_connection(user.id):
        # If someone linked the account already
        await cm.delete_connection(ctx.author.id)
        return await ctx.interaction.edit_original_response(content="Someone else already linked this account!", embeds=[], view=None)
    
    # Verification done
    await cm.create_connection(ctx.author.id, user.id)
    em = get_default_embed()
    em.description = f"Your Discord is now linked to [@{user.username}]({profile_url(user.username)})! {get_emoji('helpful')}\n\n" \
                      "**RecNetBot will now**:\n" + BENEFITS
                      
    em.set_image(url=get_icon("user_command"))
    em.set_footer(text="You can also pull up yours or others' linked profiles and more through their Discord!")
    await ctx.interaction.edit_original_response(embeds=[profile_em, em], view=None)
    
    # Add on Rec Room
    # await self.bot.rr_bot.send_friend_request(account_id=user.id)
    