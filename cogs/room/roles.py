from dataclasses import dataclass
import discord
from discord.ext import commands
from embeds import get_default_embed
from resources import get_emoji
from typing import List, Optional
from recnetpy.dataclasses.room import Room
from recnetpy.dataclasses.role import Role
from utils.converters import FetchRoom
from utils import chunks, profile_url
from discord.commands import slash_command, Option
from utils.paginator import RNBPaginator, RNBPage
from utils.rec_net_urls import img_url, room_url


class RoleView(discord.ui.View):
    def __init__(self, bot: commands.Bot, context: discord.ApplicationContext, room: Room):
        super().__init__()
        self.bot = bot
        self.ctx = context
        self.embeds = []
        self.paginator = None
        self.room = room
        self.roles = room.roles
        
        # Sort roles by the account's display_name
        self.roles.sort(key=lambda role: role.account.display_name)
        
        self.add_item(Dropdown(self))
        
    def initialize(self) -> discord.Embed:
        """
        Generates the first embed
        """
        
        self.register_selections(-1)
        return self.embeds
        
        
    def register_selections(self, selections: List[int]):
        """
        Takes in selected roles and creates embeds
        """
        
        if selections == -1:
            roles = self.roles
        else:
            roles = list(filter(lambda role: role.id in selections, self.roles))
            
            
        self.embeds = self.create_embeds(roles)
        
    def create_embeds(self, roles: Optional[List[Role]]) -> discord.Embed:
        """
        Creates role page embeds
        """
        em = get_default_embed()
        em.url = room_url(self.room.name)
        em.set_thumbnail(url=img_url(self.room.image_name, crop_square=True))
        em.title = f"^{self.room.name}'s privileged users"
        
        if not roles:
            em.description = "No players found!"
            return [RNBPage(embeds=[em])]
            
        role_chunks, embeds = chunks(roles, 15), []
        for chunk in role_chunks:
            em, pieces = get_default_embed(), []
            em.title = f"^{self.room.name}'s privileged users"
            em.url = room_url(self.room.name)
            em.set_thumbnail(url=img_url(self.room.image_name, crop_square=True))
            for role in chunk:
                pieces.append(
                    #f"[{role.account.display_name}]({profile_url(role.account.username)})\n{get_emoji('arrow')}{role.role}"
                    f"[{role.account.display_name}]({profile_url(role.account.username)}) • {role.name}"
                )
            
            em.description = "\n".join(pieces)
            embeds.append(RNBPage(embeds=[em]))
        
        return embeds
        
        
    async def refresh(self, interaction: discord.Interaction):
        #await interaction.response.edit_message(embed=self.embed, view=self)
        await interaction.response.defer(invisible=True)
        await self.paginator.update(pages=self.embeds, custom_view=self)
        
        
class Dropdown(discord.ui.Select):
    def __init__(self, view):
        self.role_view = view
        self.bot = self.role_view.bot
        self.roles = self.role_view.roles
        
        # Create selection options with cogs
        
        options = [
            discord.SelectOption(
                label=f"All ({len(self.roles)})"
            ),
            discord.SelectOption(
                label="Creator",
                emoji=get_emoji('role_owner')
            )
        ]
        
        # If co-owners
        co_owners = len(list(filter(lambda role: role.id == 30, self.roles)))
        if co_owners:
            options.append(
                discord.SelectOption(
                    label=f"Co-Owner ({co_owners})",
                    emoji=get_emoji('role_owner')
                )
            )
        
        # If temp co-owners
        temp_co_owners = len(list(filter(lambda role: role.id == 31, self.roles)))
        if temp_co_owners:
            options.append(
                discord.SelectOption(
                    label=f"Temporary Co-Owner ({temp_co_owners})",
                    emoji=get_emoji('role_owner')
                )
            )
        
        # If moderators
        mods = len(list(filter(lambda role: role.id == 20, self.roles)))
        if mods:
            options.append(
                discord.SelectOption(
                    label=f"Moderator ({mods})",
                    emoji=get_emoji('role_mod')
                )
            )

        # If hosts
        hosts = len(list(filter(lambda role: role.id == 10, self.roles)))
        if hosts:
            options.append(
                discord.SelectOption(
                    label=f"Host ({hosts})",
                    emoji=get_emoji('role_host')
                )
            )

        super().__init__(
            placeholder="Select Roles",
            min_values=1,
            max_values=len(options),
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        """
        Returns chosen categories back to the view
        """
        
        role_ids = {
            "Creator": 255,
            "Temporary Co-Owner": 31,
            "Co-Owner": 30,
            "Moderator": 20,
            "Host": 10
        }
        roles = list(map(lambda role: role_ids.get(role.split(" (")[0], -1), self.values))
             
        # If all selected, make it the primary selection
        if -1 in roles:
            roles = -1
        
        self.role_view.register_selections(roles)
        await self.role_view.refresh(interaction)

@slash_command(
    name="roles",
    description="View a room's co-owners, moderators and hosts."
)
async def roles(
    self, 
    ctx: discord.ApplicationContext,
    room: Option(FetchRoom, name="name", description="Enter RR room", required=True)
):
    await room.resolve_role_owners()
    view = RoleView(self.bot, context=ctx, room=room)
    embeds = view.initialize()
    paginator = RNBPaginator(pages=embeds, custom_view=view, show_indicator=False, show_disabled=True, trigger_on_display=True)
    view.paginator = paginator
    await paginator.respond(ctx.interaction)