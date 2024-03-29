import discord
from discord import ApplicationContext
from discord.commands import slash_command
from discord.ext.commands import cooldown, BucketType
from embeds import get_default_embed, fetch_profile_embed

# For prompting the user whether or not to link the account
class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Unlink", style=discord.ButtonStyle.red)
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
    name="unlink",
    description="Unlink your Rec Room account from your Discord."
)
@cooldown(rate=1, per=300, type=BucketType.user)
async def unlink(
    self, 
    ctx: ApplicationContext
):
    await ctx.interaction.response.defer(ephemeral=True)
    
    # Check if Discord user has already linked an account
    check_discord = self.bot.cm.get_discord_connection(ctx.author.id)
    if check_discord:
        user = await self.bot.RecNet.accounts.fetch(check_discord.rr_id)
        
        profile_em = await fetch_profile_embed(user)
        prompt_em = get_default_embed()
        prompt_em.description = "Are you sure you want to **UNLINK** your current Rec Room account?\nThis is irreversible and you will have to verify the account again if you wish to link it again."
        view = Confirm()
        
        await ctx.interaction.edit_original_response(
            embeds=[profile_em, prompt_em],
            view=view
        )
        
        await view.wait()
        if view.value is None:
            return await ctx.interaction.edit_original_response(content="Prompt timed out!", embeds=[], view=None)
        elif view.value is False:
            return await ctx.interaction.edit_original_response(content="Cancelled unlinking!", embeds=[], view=None)
        
        # Delete connection
        self.bot.cm.delete_connection(ctx.author.id)
        
        await ctx.interaction.edit_original_response(
            content="Unlinking complete, your Discord account isn't linked to the Rec Room account anymore!",
            embeds=[],
            view=None
        )        
    else:
        group = discord.utils.get(self.__cog_commands__, name='profile')
        unlink_command = discord.utils.get(group.walk_commands(), name='link')
        await ctx.interaction.edit_original_response(
            content=f"Your Discord account isn't linked to a Rec Room account in the first place! Feel free to link one with {unlink_command.mention}"
        )        