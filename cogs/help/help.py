import discord
from datetime import datetime
from resources import get_emoji
from embeds import get_default_embed
from discord.commands import slash_command, SlashCommand
from discord.ext.commands import Context

class DetailsView(discord.ui.View):
    def __init__(self, invite_link: str = None, server_link: str = None, help_command: SlashCommand = None, context: Context = None):
        super().__init__()
        self.help_cmd = help_command
        self.ctx = context
        buttons = []

        # Component timeout
        self.timeout = 180
        self.disable_on_timeout = True
        
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
                label="Join Server",
                url=server_link,
                style=discord.ButtonStyle.link
            )
            buttons.append(server_btn)
        
        # add buttons
        for item in buttons:
            self.add_item(item)
    
    @discord.ui.button(label="View Commands", style=discord.ButtonStyle.primary)
    async def view_cmds(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        # Make sure it's the author using the component
        if interaction.user.id != interaction.message.interaction.user.id:
            return await interaction.response.send_message("You're not authorized!", ephemeral=True)
        
        await interaction.response.defer()
        await self.help_cmd(self.ctx)

@slash_command(
    name="help",
    description="Get help with navigating RecNetBot!"
)
async def help(self, ctx: discord.ApplicationContext):
    await ctx.interaction.response.defer()
    
    cfg = self.bot.config
    
    em = get_default_embed()
    em.title = "RecNetBot"
    em.description = f"Your sidekick of all things RecNet! {get_emoji('rr')}"
    em.set_footer(text="RecNetBot is NOT affiliated with Rec Room Inc.")
    
    # Fetch commands to display
    cogs = self.bot.cogs.values()

    # The displayed commands in the meant order
    cmds = {
        "User": {
            "info": {"mention": None, "description": "View someone's profile"},
            "xp": {"mention": None, "description": "View a player's level & XP progress with details", "updated": True},
            "link": {"mention": None, "description": "Link your Rec Room profile", "hidden": True}  # Keep it here for later
        },
        "Room": {
            "info": {"mention": None, "description": "New properties, included room save description to updates", "updated": True} 
        },
        "Image": {
            "photos": {"mention": None, "description": "Browse someone's shared photos"}
        },
        "Random": {
            "image": {"mention": None, "description": "Pull up random images out of context"}
        },
        "Invention": {
            "search": {"mention": None, "description": "Search inventions"}
        },
        "Help": {
            "commands": {"mention": None, "description": "View the rest of the commands...", "command": None}
        },
        "Circuits V2": {
            "chip": {"mention": None, "description": "Lookup a CV2 chip and view its ports and properties", "updated": True}
        }
        #"Miscellaneous": {
        #    "changelog": {"hidden": True}  # Fetch for later
        #}
    }
    
    # Find the wanted commands cuz 'get_command' doesn't work. At least this is a single iteration to find all the commands.
    for cog in cogs:
        for cmd in cog.walk_commands():
            if cog.qualified_name in cmds:
                if cmd.name in cmds[cog.qualified_name]:
                    cmds[cog.qualified_name][cmd.name]["mention"] = cmd.mention
                    
                    # for the help command
                    if "command" in cmds[cog.qualified_name][cmd.name]:
                        cmds[cog.qualified_name][cmd.name]["command"] = cmd
                    
    # Gather the commands in the meant order
    beginner_guide = ""
    new_updated = ""
    for cog in cmds.values():
        for cmd in cog.values():
            if "hidden" in cmd: continue
            cmd_text = f"{cmd['mention']} • {cmd['description']}\n"

            if "updated" in cmd:
                new_updated += cmd_text
            else:
                beginner_guide += cmd_text
    
    # Getting started segment
    em.add_field(name="Getting Started", value=beginner_guide)

    # New or updates commands
    em.add_field(name="New & updated", inline=False, value=new_updated)
    
    # Account linking info if not linked
    check_discord = self.bot.cm.get_discord_connection(ctx.author.id)
    if not check_discord:
        linking = "You can link your Rec Room account through me!\n" \
                "Once linked, I will autofill `username` slots in commands.\n" \
                f"To get started, use {cmds['User']['link']['mention']} {get_emoji('helpful')}"
        em.add_field(name="Account Linking", value=linking, inline=False)

    # Information segment
    info = f"{get_emoji('stats')} I am in `{len(self.bot.guilds):,}` servers and counting!\n" \
           f"{get_emoji('helpful')} `{self.bot.cm.get_connection_count():,}` people have linked their Rec Room account!"
    
    # Update segment
    #resp = await get_changelog(self.bot)
    #if not resp.get("error"):
    #    last_updated = resp.get('created_timestamp', 0)
    #
    #    info += f"\n{get_emoji('update')} I was last updated <t:{last_updated}:R>. Join [my server]({cfg['server_link']}) to read the change logs!"

    # Add github link if in cfg
    if 'github_link' in cfg:
        info += f"\n{get_emoji('github')} I am open source! Check out my [GitHub organization]({cfg['github_link']})." 
    
    # Add the segment
    em.add_field(name="Information", value=info, inline=False)

    # Get link buttons + commands
    view = DetailsView(
        invite_link=cfg.get('invite_link', None),
        server_link=cfg.get('server_link', None),
        help_command=cmds["Help"]["commands"]["command"], # yes. confusing.
        context=ctx
    )
    await ctx.respond(embed=em, view=view)