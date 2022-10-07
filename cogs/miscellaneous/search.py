import discord
from discord.ext import commands
from embeds import get_default_embed
from discord.commands import slash_command, Option
from resources import get_emoji
from utils import profile_url, room_url

class SearchView(discord.ui.View):
    def __init__(self, bot: commands.Bot, query: str, search_type: str):
        super().__init__()
        self.bot = bot
        self.add_item(Dropdown(self))
        
        self.query = query
        self.results = []
        self.search_type = search_type
        self.embed = None


    async def initialize(self):
        await self.register_selection(self.search_type)
        self.create_embed()
        return self.embed


    def create_embed(self) -> None:
        em = get_default_embed()
        formatted = map(lambda ele: ele["formatted"], self.results)
        em.description = f"Search results for `{self.query}`\n\n" + "\n".join(formatted)
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
        accounts = await self.bot.RecNet.accounts.search(self.query)
        
        results = []
        for ele in accounts:
            if len(results) >= 10: break
            
            level = await ele.get_level()
            formatted = f"[{ele.display_name}]({profile_url(ele.username)})\n{get_emoji('arrow')} {get_emoji('level')} {level.level} @{ele.username}"
            item = {"name": ele.username, "formatted": formatted}
            results.append(item)
        
        self.results = results
        
    
    async def fetch_rooms(self) -> None:
        rooms = await self.bot.RecNet.rooms.search(self.query)
        
        results = []
        for ele in rooms:
            if len(results) >= 10: break
            
            creator = await ele.get_creator_account()
            formatted = f"[^{ele.name}]({room_url(ele.name)})\n{get_emoji('arrow')} @{creator.username}"
            item = {"name": ele.name, "formatted": formatted}
            results.append(item)
        
        self.results = results
    

    async def refresh(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=self.embed, view=self)
        


class Dropdown(discord.ui.Select):
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
        )

    async def callback(self, interaction: discord.Interaction):
        await self.search_view.register_selection(self.values[0])
        await self.search_view.refresh(interaction)
        


@slash_command(
    name="search",
    description="Search for all things RecNet!"
)
async def search(
    self,   
    ctx: discord.ApplicationContext,
    query: Option(str, name="query", description="Search term", required=True),
    search_type: Option(str, choices=["Account", "Room"], name="type", description="What are you looking for?", required=False, default="Account")
):
    await ctx.interaction.response.defer()
    
    view = SearchView(self.bot, query, search_type)
    em = await view.initialize()
    await ctx.respond(view=view, embed=em)
    
    
    
    
    
    
    
    