import discord
from discord.ext import commands
from discord.commands import slash_command

class BugReportModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        self.bug_channel = kwargs.pop("bug_report_channel")
        super().__init__(
            discord.ui.InputText(
                label="Short Summary",
                placeholder="Tell us a short summary of what happened.",
            ),
            discord.ui.InputText(
                label="Reproduction Steps",
                value="Tell us how the bug is replicated.",
                style=discord.InputTextStyle.long,
            ),
            *args,
            **kwargs,
        )

    async def callback(self, interaction: discord.Interaction):
        em = discord.Embed(
            fields=[
                discord.EmbedField(
                    name="Short Summary", value=self.children[0].value, inline=False
                ),
                discord.EmbedField(
                    name="Reproduction Steps", value=self.children[1].value, inline=False
                ),
            ],
            color=discord.Color.orange(),
        )
        await self.bug_channel.send(embed=em)
        await interaction.response.send_message("Thank you for your bug report!", ephemeral=True)


@slash_command(
    name="bugreport",
    description="Report a bug you encountered outside of my server."
)
async def bugreport(self, ctx: discord.ApplicationContext):
    """A command for reporting a bug"""
    modal = BugReportModal(title="Send a bug report", bug_report_channel=self.bot.bug_channel)
    await ctx.send_modal(modal)     