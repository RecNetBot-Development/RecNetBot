import discord
from discord.ext import commands
from embeds import get_default_embed
from discord.commands import slash_command, Option
from discord.ext.pages import PaginatorButton
from resources import get_emoji
from utils import profile_url, room_url, sanitize_text
from utils.paginator import RNBPaginator, RNBPage

        
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
    def __init__(self, bot: commands.Bot, query: str, search_type: str):
        super().__init__()
        self.bot = bot
        self.add_item(Dropdown(self))
        self.add_item(Browse(self))
        
        self.query = query
        self.results = {
            "Account": [],
            "Room": []
        }
        self.search_type = search_type
        self.embed = None


    async def initialize(self):
        await self.register_selection(self.search_type)
        self.create_embed()
        return self.embed


    def create_embed(self) -> None:
        em = get_default_embed()
        formatted = map(lambda ele: ele["formatted"], self.results[self.search_type][:10])
        em.description = "\n".join(formatted)
        em.set_footer(text=f"Results: {len(self.results[self.search_type])}")
        if len(self.results[self.search_type]) > 10: em.description += "\n..."  # Indicate that there's more truncated results
        em.description = f"Search results for `{self.query}`\n\n" + sanitize_text(em.description)
        self.embed = em
        
    
    async def register_selection(self, select_type: str):
        self.search_type = select_type
        
        match self.search_type:
            case "Account":
                await self.fetch_accounts()
                
            case "Room":
                await self.fetch_rooms()
                
        self.create_embed()
        
        
    async def fetch_accounts(self) -> None:
        if self.results["Account"]: return
        
        accounts = await self.bot.RecNet.accounts.search(self.query)
        
        results = []
        for ele in accounts:
            level = await ele.get_level()
            formatted = f"[{ele.display_name}]({profile_url(ele.username)})\n{get_emoji('arrow')} {get_emoji('level')} {level.level} @{ele.username}"
            item = {"name": ele.username, "formatted": formatted, "dataclass": ele}
            results.append(item)
        
        self.results["Account"] = results
        
    
    async def fetch_rooms(self) -> None:
        if self.results["Room"]: return
        
        rooms = await self.bot.RecNet.rooms.search(self.query)
        
        results = []
        for ele in rooms:
            creator = await ele.get_creator_account()
            formatted = f"[^{ele.name}]({room_url(ele.name)})\n{get_emoji('arrow')} @{creator.username}"
            item = {"name": ele.name, "formatted": formatted, "dataclass": ele}
            results.append(item)
        
        self.results["Room"] = results
    

    async def refresh(self, interaction: discord.Interaction):
        await interaction.edit_original_response(embed=self.embed, view=self)
        


class Dropdown(discord.ui.Select["SearchView"]):
    def __init__(self, view: SearchView):
        self.search_view = view
        self.bot = self.search_view.bot
        
        options = [
            discord.SelectOption(
                label="Account"
            ),
            discord.SelectOption(
                label="Room"
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
        

class Browse(discord.ui.Button["SearchView"]):
    def __init__(self, view: SearchView):
        self.search_view = view
        
        super().__init__(
            style=discord.ButtonStyle.secondary, label="Browse", row=1
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        pages = list(map(lambda ele: RNBPage(ele["dataclass"]), self.search_view.results[self.search_view.search_type]))
        paginator = RNBPaginator(pages=pages, trigger_on_display=True, show_indicator=False, author_check=True)
        paginator.add_button(Send())
        await paginator.respond(interaction, ephemeral=True)


@slash_command(
    name="search",
    description="Search for accounts, rooms, events or inventions!"
)
async def search(
    self,   
    ctx: discord.ApplicationContext,
    query: Option(str, name="query", description="Search term", required=True),
    search_type: Option(str, choices=["Account", "Room"], name="type", description="What are you looking for?", required=False, default="Account")
):
    await ctx.interaction.response.defer(invisible=True)
    
    view = SearchView(self.bot, query, search_type)
    em = await view.initialize()
    await ctx.respond(view=view, embed=em)
    #await ctx.interaction.response.send_message(view=view, embed=em, ephemeral=True)
    
    
    
    
    
    
    