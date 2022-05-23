from email.policy import default
import discord
from discord import Embed
from embeds.event.event_data_embed import event_data_embed
from embeds.room.room_data_embed import room_data_embed
from utility import load_cfg, respond, edit_message
from discord.commands import slash_command, Option  # Importing the decorator that makes slash commands.
from rec_net.exceptions import AccountNotFound, EventNotFound, ImageNotFound, RoomNotFound
from embeds import account_data_embed, image_data_embed

cfg = load_cfg()

class RawDataShowcase(discord.ui.View):
    def __init__(self, ctx, type, data, content):
        super().__init__(
            timeout=None
        )
        
        self.type = type
        self.content = content
        self.ctx = ctx
        self.user = ctx.user
        self.data = data[0] if isinstance(data, list) else data
        self.variation = 0
        
        self.embeds = {
            "account": account_data_embed,
            "image": image_data_embed,
            "event": event_data_embed,
            "room": room_data_embed
        }
        
    @discord.ui.button(label="Toggle Variations", style=discord.ButtonStyle.primary, row=0, custom_id="persistent:data_toggle_explanations")
    async def toggle(self, button, interaction):
        self.change_variation()
        await edit_message(self.ctx, interaction, embed=self.make_embed(), content=self.content)
        
    async def _respond(self):
        await respond(self.ctx, view=self, embed=self.make_embed(), content=self.content)
        
    async def interaction_check(self, interaction):
        return self.user == interaction.user
    
    def make_embed(self):
        match self.variation:
            case 0:
                return self.embeds[self.type](self.data, False)
            case 1:
                return self.embeds[self.type](self.data, True)
            case 2:
                embed = Embed(
                    description=f"```json\n{self.data}```"
                )
                return embed
                
    
    def change_variation(self):
        if self.variation >= 2: self.variation = 0
        else: self.variation += 1
            
    
@slash_command(
    debug_guilds=cfg['test_guild_ids'],
    name="data",
    description="Get raw data from the API."
)
async def data(
    self, 
    ctx, 
    type: Option(str, "Enter what type of data you want", choices=["account", "room", "event", "image"], required=True),
    name: Option(str, "Enter the unique name or id", required=True),
    is_id: Option(bool, "Is the name argument an id or not? If unspecified, it will be assumed. Images are always id's.", required=False)
):
    await ctx.interaction.response.defer()
    
    if name.isdigit() and is_id == None:
        is_id = True
    
    match type:
        case "account":
            host = "https://accounts.rec.net"
            endpoint = f"/account?username={name}"
            request = self.bot.rec_net.rec_net.accounts.account(name).get() if is_id else self.bot.rec_net.rec_net.accounts.account().get({"username": name})
            exception = AccountNotFound(name)
        case "room":
            host = "https://rooms.rec.net"  
            endpoint = f"/rooms/{name}" if is_id else f"/rooms?name={name}"
            request = self.bot.rec_net.rec_net.rooms.rooms(name).get() if is_id else self.bot.rec_net.rec_net.rooms.rooms().get({"name": name})
            exception = RoomNotFound(name)
        case "image":
            host = "https://api.rec.net"
            endpoint = f"/api/images/v4/{name}"
            request = self.bot.rec_net.rec_net.api.images.v4(name).get()
            exception = ImageNotFound(name)
        case "event":
            host = "https://api.rec.net"
            endpoint = f"/api/playerevents/v1/{name}" if is_id else f"/api/playerevents/v1/search?query={name}&take=1"
            request = self.bot.rec_net.rec_net.api.playerevents.v1(name).get() if is_id else self.bot.rec_net.rec_net.api.playerevents.v1.search().get({"query": name, "take": 1})
            exception = EventNotFound(name)

    resp = await request.fetch()
    if not resp.success or not resp.data: raise exception

    view = RawDataShowcase(ctx, type, resp.data, host + endpoint)
    await view._respond()