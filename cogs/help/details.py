import discord
import time
from resources import get_emoji
from embeds import get_default_embed
from discord.commands import slash_command

class DetailsView(discord.ui.View):
    def __init__(self, invite_link: str = None, server_link: str = None):
        super().__init__()
        buttons = []
        
        # Invite bot button
        if invite_link:
            invite_btn = discord.ui.Button(
                label="Invite Bot",
                url=invite_link,
                style=discord.ButtonStyle.link
            )
            buttons.append(invite_btn)
        
        # Join discord button
        if server_link:
            server_btn = discord.ui.Button(
                label="Join Discord",
                url=server_link,
                style=discord.ButtonStyle.link
            )
            buttons.append(server_btn)
        
        # add buttons
        for item in buttons:
            self.add_item(item)

@slash_command(
    name="details",
    description="View details about RecNetBot!"
)
async def details(self, ctx: discord.ApplicationContext):
    await ctx.interaction.response.defer()
    
    cfg = self.bot.config
    
    em = get_default_embed()
    em.title = "RecNetBot"
    em.description = ""
    
    em.set_footer(text="RecNetBot is NOT affiliated with Rec Room Inc.")
    
    info_parts = [f"{get_emoji('stats')} I am in `{len(self.bot.guilds):,}` servers so far!"]
    if 'github_link' in cfg:
        info_parts.append(
            f"{get_emoji('github')} I am open source! Check out my [GitHub repository]({cfg['github_link']})."
        )

    em.add_field(name="Information", value="\n".join(info_parts))
    
    view = DetailsView(
        invite_link=cfg.get('invite_link', None),
        server_link=cfg.get('server_link', None)
    )
    await ctx.respond(embed=em, view=view)