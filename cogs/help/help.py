import discord
import datetime
from resources import get_emoji
from embeds import get_default_embed
from discord.commands import slash_command, SlashCommand
from discord.ext.commands import Context
from utils import BaseView

class DetailsView(BaseView):
    def __init__(self, invite_link: str = None, server_link: str = None, help_command: SlashCommand = None, tip_jar: SlashCommand = None, context: Context = None):
        super().__init__()
        self.help_cmd = help_command
        self.tip_jar = tip_jar
        self.ctx = context
        buttons = []

        # Component timeout
        self.timeout = 600
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
    async def btn_view_cmds(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        # Make sure it's the author using the component
        if not self.authority_check(interaction):
            return await interaction.response.send_message("You're not authorized!", ephemeral=True)
        
        await interaction.response.defer()
        await self.help_cmd(self.ctx)
    
    @discord.ui.button(label="Tip Jar", style=discord.ButtonStyle.green)
    async def btn_tip_jar(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.defer()
        await self.tip_jar(self.ctx)

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
            "info": {"mention": None, "beginner": True, "description": "Check someone's Rec Room profile"},
            "xp": {"mention": None, "description": "View a player's level & XP progress with details"},
            "verify": {"mention": None, "description": "Verify your Rec Room profile", "hidden": True}  # Keep it here for later
        },
        "Room": {
            "info": {"mention": None, "beginner": True, "description": "View room info that cannot be seen otherwise"} 
        },
        "Image": {
            "photos": {"mention": None, "beginner": True, "description": "Browse someone's RecNet photos"}
        },
        "Circuits V2": {
            "chip": {"mention": None, "description": "Lookup a CV2 chip and view its ports and properties", "beginner": True}
        },
        "Random": {
            "image": {"mention": None, "beginner": True, "description": "Find random images from the depths of RecNet", "updated": True}
        },
        #"Invention": {
        #    "search": {"mention": None, "beginner": True, "description": "Search Rec Room inventions"}
        #},
        "Help": {
            "commands": {"mention": None, "beginner": True, "description": "Browse the rest of the commands...", "command": None}
        },
        "Miscellaneous": {
            "tip": {"mention": None, "command": None}  # Fetch for later
        }
    }

    # Get ran commands from the past month
    month_ago = datetime.datetime.now() - datetime.timedelta(days=30)
    logs = self.bot.lcm.get_ran_commands_after_timestamp(int(month_ago.timestamp()))

    total_ran, total_users, command_ran = 0, 0, {}
    for user, data in logs.items():
        total_users += 1
        total_ran += data["total_usage"]

        # Calculate how many times each command has been ran
        for cmd, usage in data["specific"].items():
            if cmd in command_ran:
                command_ran[cmd] += len(usage)
            else:
                command_ran[cmd] = len(usage)

    # Sort them by usage and get the top 5
    usage_sort = {k: v for k, v in sorted(command_ran.items(), key=lambda item: item[1], reverse=True)}
    leaderboard = []
    limit, i = 5, 0
    for cmd, usage in usage_sort.items():
        if i >= limit: break
        if cmd.startswith("other:"): continue
        leaderboard.append(f"`{cmd}`")
        i += 1

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
    beginner_guide, new_updated = [], []
    for cog in cmds.values():
        for cmd in cog.values():
            if cmd.get("hidden", False): continue

            if cmd.get("updated", False):
                new_updated.append(cmd['mention'])

            if cmd.get("beginner", False):
                beginner_guide.append(f"{cmd['mention']} • {cmd['description']}") 
    
    # Getting started segment
    em.add_field(name="Getting Started", inline=False, value="\n".join(beginner_guide) if beginner_guide else "How empty...")

    # Trending segment
    em.add_field(name="Trending Commands", inline=False, value=" ".join(leaderboard) if leaderboard else "How empty...")

    # New or updates commands
    em.add_field(name="New & Updated", inline=False, value=" ".join(new_updated) if new_updated else "How empty...")
    
    # Account linking info if not linked
    check_discord = self.bot.cm.get_discord_connection(ctx.author.id)
    if not check_discord:
        linking = "You can verify your Rec Room account!\n" \
                "Once verified, I will autofill `username` slots and list your owned rooms in `room` slots.\n" \
                f"To get started, use {cmds['User']['verify']['mention']} {get_emoji('helpful')}"
        em.add_field(name="Account Linking", value=linking, inline=False)

    # Information segment
    info = f"{get_emoji('stats')} I am in `{len(self.bot.guilds):,}` servers and counting!\n" \
           f"{get_emoji('helpful')} `{self.bot.cm.get_connection_count():,}` people have linked their Rec Room account!\n" \
           f"{get_emoji('token')} {cmds['Miscellaneous']['tip']['mention']} if you would like to thank for RecNetBot!"
    
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
        tip_jar=cmds['Miscellaneous']['tip']["command"],
        context=ctx
    )
    await ctx.respond(embed=em, view=view)