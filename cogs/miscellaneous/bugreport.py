import discord
from discord.ext import commands
from discord.commands import slash_command

class BugReportModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        self.bug_channel = kwargs.pop("log_channel")
        super().__init__(
            discord.ui.InputText(
                label="Command",
                placeholder="Tell us what command you used.",
                style=discord.InputTextStyle.short
            ),
            discord.ui.InputText(
                label="Short Summary",
                placeholder="Tell us a short summary of what happened.",
                style=discord.InputTextStyle.short
            ),
            discord.ui.InputText(
                label="Reproduction Steps",
                placeholder="Tell us how the bug is replicated.",
                style=discord.InputTextStyle.long,
            ),
            discord.ui.InputText(
                label="May we possibly contact you for more info?",
                placeholder="(yes/no)",
                style=discord.InputTextStyle.short,
            ),
            *args,
            **kwargs,
        )

    async def callback(self, interaction: discord.Interaction):
        em = discord.Embed(
            color=discord.Color.yellow()
        )
        
        # Fill in the fields
        for field in self.children:
            em.add_field(name=field.label, value=field.value, inline=False)
            
        em.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
        await self.bug_channel.send(f"A bug report was submitted by {interaction.user.mention} ({interaction.user})", embed=em)
        await interaction.response.send_message("Thank you so much for helping RecNetBot improve!", ephemeral=True)


@slash_command(
    name="bugreport",
    description="Report a bug you encountered outside of my server."
)
async def bugreport(self, ctx: discord.ApplicationContext):
    """A command for reporting a bug"""
    modal = BugReportModal(title="Send a bug report", log_channel=self.bot.log_channel)
    await ctx.send_modal(modal)     