import discord
from discord import ApplicationContext
from exceptions import ConnectionNotFound
from discord.ext import commands
from embeds import get_default_embed, room_embed
from discord.ext.pages import PaginatorButton
from resources import get_emoji
from utils import profile_url, room_url, sanitize_text, img_url
from utils.paginator import RNBPaginator, RNBPage
from recnetpy.dataclasses.room import Room
from recnetpy.dataclasses.account import Account
from typing import List
from discord.commands import slash_command, Option
from utils.converters import FetchAccount

        
class Send(PaginatorButton):
    def __init__(self):
        super().__init__(label="Send to Chat", row=1, button_type="send")
        self.sent_pages = []
        
    async def callback(self, interaction: discord.Interaction):
        if self.paginator.current_page in self.sent_pages:  # Don't allow for it to be spammed
            await interaction.response.send_message("You have already sent that!", ephemeral=True)
        
        page = self.paginator.pages[
            self.paginator.current_page
        ]
        page_content = self.paginator.get_page_content(page)
        if page_content.embeds:
            page_content.embeds[-1].remove_footer()  # Clear out indicator
        
        self.sent_pages.append(self.paginator.current_page)  # Disable sending it
        
        await interaction.response.send_message(content=page_content.content, embeds=page_content.embeds, files=page_content.files)
        

class ShowcaseView(discord.ui.View):
    def __init__(self, bot: commands.Bot, showcased_rooms: List[Room], account: Account):
        super().__init__()
        self.bot = bot
        self.raw_rooms = showcased_rooms
        self.showcased = []
        self.account = account


    async def initialize(self) -> discord.Embed:
        self.showcased = await self.register_rooms(self.raw_rooms)
        self.update_items()
        return self.create_embed()
    
    
    def update_items(self) -> None:
        self.clear_items()
        self.add_item(Browse(self))
        self.add_item(DropdownSelection(self))
        self.add_item(Delete(self))


    def create_embed(self) -> discord.Embed:
        em = get_default_embed()
        em.title = f"{self.account.display_name}'s Showcased Rooms"
        em.url = profile_url(self.account.username)
        em.set_thumbnail(url=img_url(self.account.profile_image, crop_square=True))
        formatted = map(lambda ele: ele["formatted"], self.showcased)
        em.description = sanitize_text("\n".join(formatted))
        return em
        
    
    async def register_rooms(self, rooms: List[Room]) -> List[dict]:
        results = []
        for i, ele in enumerate(rooms, start=1):
            formatted = f"[^{ele.name}]({room_url(ele.name)})\n{get_emoji('arrow')} {get_emoji('cheer')} {ele.cheer_count}"
            item = {"name": f"{i}. {ele.name}", "formatted": formatted, "dataclass": ele}
            results.append(item)
        
        return results
        
        
class DropdownSelection(discord.ui.Select["ShowcaseView"]):
    def __init__(self, view: ShowcaseView):
        self.search_view = view
        self.bot = self.search_view.bot
        self.showcased = self.search_view.showcased
        self.sent = [] 
            
        options = []
        for ele in self.showcased:
            option = discord.SelectOption(
                label=ele["name"]
            )
            options.append(option)
            
        super().__init__(
            placeholder="View result",
            min_values=1,
            max_values=len(self.showcased),
            options=options,
            row=1
        )

    async def callback(self, interaction: discord.Interaction):
        embeds = []
        for ele in self.values:
            # Find the result with the name property
            item = next((item for item in self.showcased if item['name'] == ele), None)["dataclass"]
            if item in self.sent: continue  # Spam prevention
            self.sent.append(item)  # Spam prevention
            
            room = await item.client.rooms.fetch(item.id, 78)
            
            cached_stats = self.bot.rcm.get_cached_stats(interaction.user.id, room.id)
            self.bot.rcm.cache_stats(interaction.user.id, room.id, room)
            
            embeds.append(room_embed(room, cached_stats))
        
        if not embeds:
            return await interaction.response.send_message("You can't send the same results more than once to prevent spam.", ephemeral=True)
        
        await interaction.response.send_message(embeds=embeds)
        

class Browse(discord.ui.Button["ShowcaseView"]):
    def __init__(self, view: ShowcaseView):
        self.search_view = view
        
        super().__init__(
            style=discord.ButtonStyle.secondary, label="Browse", row=2
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        pages = list(map(lambda ele: RNBPage(ele["dataclass"]), self.search_view.showcased))
        paginator = RNBPaginator(pages=pages, trigger_on_display=True, show_indicator=False, author_check=True)
        paginator.add_button(Send())
        await paginator.respond(interaction, ephemeral=True)
        
        
class Delete(discord.ui.Button["ShowcaseView"]):
    def __init__(self, view: ShowcaseView):
        self.search_view = view
        
        super().__init__(
            style=discord.ButtonStyle.danger, label="Delete", row=2
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.delete_original_response()
        

@slash_command(
    name="showcased",
    description="View a player's showcased rooms on their profile."
)
async def showcased(
    self, 
    ctx: ApplicationContext, 
    account: Option(FetchAccount, name="username", description="Enter RR username", default=None, required=False)
):
    if not account:  # Check for a linked RR account
        account = await self.bot.cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
    
    showcased = await account.get_showcased_rooms()
    if not showcased:
        em = get_default_embed()
        em.description = "This Rec Room account doesn't have any showcased rooms!"
        return await ctx.respond(embed=em)
    
    view = ShowcaseView(self.bot, showcased, account)
    em = await view.initialize()
    await ctx.respond(view=view, embed=em)
    