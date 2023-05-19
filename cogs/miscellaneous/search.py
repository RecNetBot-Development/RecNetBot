import discord
from discord.ext import commands
from embeds import get_default_embed, fetch_profile_embed, room_embed, event_embed
from discord.commands import slash_command, Option
from discord.ext.pages import PaginatorButton
from embeds.invention_embed import invention_embed
from resources import get_emoji
from utils import profile_url, room_url, sanitize_text, event_url, invention_url, shorten
from utils.paginator import RNBPaginator, RNBPage
from recnetpy.dataclasses.account import Account
from recnetpy.dataclasses.event import Event
from recnetpy.dataclasses.room import Room
from recnetpy.dataclasses.invention import Invention

        
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
        

class SearchView(discord.ui.View):
    def __init__(self, bot: commands.Bot, query: str, search_type: str, lock: bool = False):
        super().__init__()
        self.bot = bot
        self.query = query
        self.results = {
            "Account": [],
            "Room": [],
            "Event": [],
            "Invention": []
        }
        self.search_type = search_type
        self.embed = None
        self.max_count = 10
        self.lock = lock


    async def initialize(self):
        await self.register_selection(self.search_type)
        self.create_embed()
        return self.embed
    

    def update_items(self):
        self.clear_items()
        if not self.lock: self.add_item(DropdownSearch(self))
        if self.results[self.search_type]:
            self.add_item(Browse(self))
            self.add_item(DropdownSelection(self))
        self.add_item(Delete(self))


    def create_embed(self) -> None:
        em = get_default_embed()
        formatted = map(lambda ele: ele["formatted"], self.results[self.search_type][:self.max_count])
        em.description = "\n".join(formatted)
        em.set_footer(text=f"Results: {len(self.results[self.search_type])}")
        if len(self.results[self.search_type]) > self.max_count: em.description += "\n..."  # Indicate that there's more truncated results
        em.description = f"Search results for `{self.query}`\nSearching for {self.search_type.lower()}s.\n\n" + sanitize_text(em.description)
        self.embed = em
        
    
    async def register_selection(self, select_type: str):
        self.search_type = select_type
        
        match self.search_type:
            case "Account":
                await self.fetch_accounts()
                
            case "Room":
                await self.fetch_rooms()
                
            case "Event":
                await self.fetch_events()
                
            case "Invention":
                await self.fetch_inventions()
                
        self.update_items()
        self.create_embed()
        
        
    async def fetch_accounts(self) -> None:
        if self.results["Account"]: return
        
        accounts = await self.bot.RecNet.accounts.search(self.query)
        
        results = []
        for i, ele in enumerate(accounts, start=1):
            if len(results) >= self.max_count:
                results.append({"dataclass": ele})
                continue
            
            level = await ele.get_level()
            formatted = f"[{ele.display_name}]({profile_url(ele.username)})\n{get_emoji('arrow')} {get_emoji('level')} {level.level} · @{ele.username}"
            item = {"name": f"{i}. {ele.username}", "formatted": formatted, "dataclass": ele}
            results.append(item)
        
        self.results["Account"] = results
        
    
    async def fetch_rooms(self) -> None:
        if self.results["Room"]: return
        
        rooms = await self.bot.RecNet.rooms.search(self.query, take=50)
        
        results = []
        for i, ele in enumerate(rooms, start=1):
            if len(results) >= self.max_count:
                results.append({"dataclass": ele})
                continue
            
            creator = await ele.get_creator_player()
            formatted = f"[^{ele.name}]({room_url(ele.name)})\n{get_emoji('arrow')} {get_emoji('cheer')} {ele.cheer_count:,} · @{creator.username}"
            item = {"name": f"{i}. {ele.name}", "formatted": formatted, "dataclass": ele}
            results.append(item)
        
        self.results["Room"] = results
        
        
    async def fetch_events(self) -> None:
        if self.results["Event"]: return
        
        events = await self.bot.RecNet.events.search(self.query, take=50)
        
        results = []
        for i, ele in enumerate(events, start=1):
            if len(results) >= self.max_count:
                results.append({"dataclass": ele})
                continue
            
            creator = await ele.get_creator_player()
            room = await ele.get_room(include=0)
            formatted = f"[{ele.name}]({event_url(ele.id)})\n{get_emoji('arrow')} {get_emoji('visitors')} {ele.attendee_count:,} · @{creator.username}"
            if room: formatted += f" at ^{room.name}"
            item = {"name": f"{i}. {ele.name}", "formatted": formatted, "dataclass": ele}
            results.append(item)
        
        self.results["Event"] = results
        
    
    async def fetch_inventions(self) -> None:
        if self.results["Invention"]: return
        
        inventions = await self.bot.RecNet.inventions.search(self.query)
        
        results = []
        for i, ele in enumerate(inventions, start=1):
            if len(results) >= self.max_count:
                results.append({"dataclass": ele})
                continue
            
            creator = await ele.get_creator_player()
            formatted = f"[{ele.name}]({invention_url(ele.id)})\n{get_emoji('arrow')} {get_emoji('cheer')} {ele.cheer_count:,} · @{creator.username}"
            item = {"name": f"{i}. {ele.name}", "formatted": formatted, "dataclass": ele}
            results.append(item)
        
        self.results["Invention"] = results
    

    async def refresh(self, interaction: discord.Interaction):
        await interaction.edit_original_response(embed=self.embed, view=self)
        


class DropdownSearch(discord.ui.Select["SearchView"]):
    def __init__(self, view: SearchView):
        self.search_view = view
        self.bot = self.search_view.bot
        
        options = [
            discord.SelectOption(
                label="Account",
                emoji=get_emoji('user')
            ),
            discord.SelectOption(
                label="Room",
                emoji=get_emoji('room')
            ),
            discord.SelectOption(
                label="Event",
                emoji=get_emoji('event')
            ),
            discord.SelectOption(
                label="Invention",
                emoji=get_emoji('light')
            )
        ]
        super().__init__(
            placeholder="Choose what you're searching for",
            min_values=1,
            max_values=1,
            options=options,
            row=0
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(invisible=True)
        await self.search_view.register_selection(self.values[0])
        await self.search_view.refresh(interaction)
        
        
class DropdownSelection(discord.ui.Select["SearchView"]):
    def __init__(self, view: SearchView):
        self.search_view = view
        self.bot = self.search_view.bot
        self.results = self.search_view.results[self.search_view.search_type][:self.search_view.max_count]
        self.sent = [] 
            
        options = []
        for ele in self.results:
            option = discord.SelectOption(
                label=shorten(ele["name"])
            )
            options.append(option)
            
        while len(options) < 5:
            option = discord.SelectOption(
                label="." * len(options)
            )
            options.append(option)
            
        super().__init__(
            placeholder="View result",
            min_values=1,
            max_values=int(self.search_view.max_count / 2),
            options=options,
            row=1
        )

    async def callback(self, interaction: discord.Interaction):
        embeds = []
        placeholder_flag = False
        for ele in self.values:
            # Placeholder check
            if ele.startswith("."): 
                placeholder_flag = True
                continue
            
            # Find the result with the name property
            item = next((item for item in self.results if item['name'] == ele), None)["dataclass"]
            if item in self.sent: continue  # Spam prevention
            self.sent.append(item)  # Spam prevention
            
            if isinstance(item, Account):
                embeds.append(await fetch_profile_embed(item))
                
            elif isinstance(item, Room):
                room = await item.client.rooms.fetch(item.id, 78)
                
                cached_stats = self.bot.rcm.get_cached_stats(interaction.user.id, room.id)
                self.bot.rcm.cache_stats(interaction.user.id, room.id, room)
                
                embeds.append(room_embed(room, cached_stats))
                
            elif isinstance(item, Event):
                embeds.append(event_embed(item))
                
            elif isinstance(item, Invention):
                cached_stats = self.bot.icm.get_cached_stats(interaction.user.id, item.id)
                self.bot.icm.cache_stats(interaction.user.id, item.id, item)
                
                embeds.append(invention_embed(item, cached_stats))
        
        if not embeds:
            if placeholder_flag:
                return await interaction.response.send_message("You selected a placeholder because Discord requires at least 5 selection options.", ephemeral=True)
            else:
                return await interaction.response.send_message("You can't send the same results more than once to prevent spam.", ephemeral=True)
        
        await interaction.response.send_message(embeds=embeds)
        

class Browse(discord.ui.Button["SearchView"]):
    def __init__(self, view: SearchView):
        self.search_view = view
        
        super().__init__(
            style=discord.ButtonStyle.secondary, label="Browse", row=2
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        pages = list(map(lambda ele: RNBPage(ele["dataclass"]), self.search_view.results[self.search_view.search_type]))
        paginator = RNBPaginator(pages=pages, trigger_on_display=True, show_indicator=False, author_check=True)
        paginator.add_button(Send())
        await paginator.respond(interaction, ephemeral=True)
        
        
class Delete(discord.ui.Button["SearchView"]):
    def __init__(self, view: SearchView):
        self.search_view = view
        
        super().__init__(
            style=discord.ButtonStyle.danger, label="Delete", row=2
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.delete_original_response()


@slash_command(
    name="search",
    description="Search for accounts, rooms, events or inventions!"
)
async def search(
    self,   
    ctx: discord.ApplicationContext,
    query: Option(str, name="query", description="Search term", required=True),
    search_type: Option(str, choices=["Account", "Room", "Event", "Invention"], name="type", description="What are you looking for?", required=False, default="Account")
):
    await ctx.interaction.response.defer(invisible=True)
    
    view = SearchView(self.bot, query, search_type)
    em = await view.initialize()
    await ctx.respond(view=view, embed=em)
    #await ctx.interaction.response.send_message(view=view, embed=em, ephemeral=True)
    
    
    
    
    
    
    