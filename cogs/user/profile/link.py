import discord
from discord import ApplicationContext
from discord.commands import slash_command, Option
from discord.ext.commands import cooldown, BucketType
from exceptions import AccountNotFound, ConnectionAlreadyDone
from embeds import get_default_embed, fetch_profile_embed
from utils import post_url, profile_url

# For prompting the user whether or not to link the account
class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
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
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green)
    async def confirm_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.defer(invisible=True)
        self.value = True
        self.stop()

# User can only run the command once every "per" seconds
@slash_command(
    name="link",
    description="Link your Rec Room profile to your Discord!"
)
@cooldown(rate=1, per=60, type=BucketType.user)
async def link(
    self, 
    ctx: ApplicationContext, 
    username: Option(str, "Enter RR username", required=True)
):
    await ctx.interaction.response.defer(ephemeral=True)
    
    # Check if Discord user has already linked an account
    check_discord = self.bot.cm.get_discord_connection(ctx.author.id)
    if check_discord:
        user = await self.bot.RecNet.accounts.fetch(check_discord.rr_id)
        
        profile_em = await fetch_profile_embed(user)
        prompt_em = get_default_embed()
        prompt_em.description = "Are you sure you want to **UNLINK** your current Rec Room account?\nThis is irreversible and will get rid of all your saved data."
        view = Confirm()
        
        await ctx.interaction.edit_original_response(
            embeds=[profile_em, prompt_em],
            view=view,
            ephemeral=True
        )
        
        await view.wait()
        if view.value is None:
            em = get_default_embed()
            em.description = "Prompt timed out!"
            return await ctx.interaction.edit_original_response(embed=em, view=None)
        elif view.value is False:
            em = get_default_embed()
            em.description = "Cancelled unlinking!"
            return await ctx.interaction.edit_original_response(embed=em, view=None)
        
        # Delete connection
        self.bot.cm.delete_connection(ctx.author.id)
    
    # Check if RR account exists
    user = await self.bot.RecNet.accounts.get(username)
    if not user: raise AccountNotFound
    
    # Check if RR account is already linked
    check_rr = self.bot.cm.get_rec_room_connection(user.id)
    if check_rr: raise ConnectionAlreadyDone
    
    # Prompt the user
    profile_em = await fetch_profile_embed(user)
    prompt_em = get_default_embed()
    prompt_em.description = '\n'.join([
        f"Are you sure you want to **LINK** [@{user.username}]({profile_url(user.username)}) to your Discord?",
        "You can only link a Rec Room account that you own."
    ])
    view = Confirm()
    await ctx.interaction.edit_original_response(
        embeds=[profile_em, prompt_em],
        view=view
    )
    
    await view.wait()
    if view.value is None:
        em = get_default_embed()
        em.description = "Prompt timed out!"
        return await ctx.interaction.edit_original_response(embed=em, view=None)
    elif view.value is False:
        em = get_default_embed()
        em.description = "Cancelled linking!"
        return await ctx.interaction.edit_original_response(embed=em, view=None)
        
    # Fetch cheers from verify post
    post = self.bot.verify_post
    cheer_list = await post.get_cheers(force=True)
            
    # Verification process
    cheered = user.id in cheer_list
    specify = "Uncheer from" if cheered else "Cheer"
    demonstration = "https://i.imgur.com/adYnPLi.gif" if cheered else "https://i.imgur.com/5VMBcJw.gif"
    
    view = Check()
    verify_em = get_default_embed()
    verify_em.description = "\n".join(
        [
            f"{specify} this [this post]({post_url(post.id)}) to verify that you own the account.",
            "You can only check the verification once."
        ]
    )
    verify_em.set_thumbnail(url=demonstration)
    await ctx.interaction.edit_original_response(embed=verify_em, view=view)
    
    await view.wait()
    if view.value is None:
        em = get_default_embed()
        em.description = "Verification timed out! Try again later."
        self.bot.cm.delete_connection(ctx.author.id)
        return await ctx.interaction.edit_original_response(embed=em, view=None)
    elif view.value is False:
        em = get_default_embed()
        em.description = "Could not verify the account's ownership. Try again later."
        self.bot.cm.delete_connection(ctx.author.id)
        return await ctx.interaction.edit_original_response(embed=em, view=None)
    
    # Check status
    cheer_list = await post.get_cheers(force=True)
    if cheered and user.id in cheer_list or not cheered and user.id not in cheer_list:    
        # Failed to verify
        em = get_default_embed()
        em.description = "Could not verify the account's ownership. Try again later."
        self.bot.cm.delete_connection(ctx.author.id)
        return await ctx.interaction.edit_original_response(embed=em, view=None)
        
    # One more security check
    if self.bot.cm.get_rec_room_connection(user.id):
        # If someone linked the account already
        em = get_default_embed()
        em.description = "Someone else already linked this account!"
        self.bot.cm.delete_connection(ctx.author.id)
        return await ctx.interaction.edit_original_response(embed=em, view=None)
    
    # Verification done
    self.bot.cm.create_connection(ctx.author.id, user.id)
    em = get_default_embed()
    em.description = f"Your Discord is now linked to [@{user.username}]({profile_url(user.username)})!"
    await ctx.interaction.edit_original_response(embeds=[profile_em, em], view=None)
    