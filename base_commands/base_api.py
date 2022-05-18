import discord
from discord import Embed
from utility import respond, edit_message
from rec_net.exceptions import AccountNotFound, EventNotFound, ImageNotFound, RoomNotFound
from embeds import account_data_embed, image_data_embed, json_embed

class RawDataShowcase(discord.ui.View):
    def __init__(self, ctx, type, data, content):
        super().__init__(
            timeout=None
        )
        
        self.type = type
        self.content = content
        self.ctx = ctx
        self.user = ctx.user
        self.data = data
        self.variation = 0
        
        self.embeds = {
            "Account": account_data_embed,
            "Image": image_data_embed,
            "Event": json_embed,
            "Room": json_embed
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
            
async def base_api(
    rec_net, 
    ctx, 
    type,
    name,
    is_id
):
    await ctx.interaction.response.defer()
    
    if name.isdigit() and is_id == None:
        is_id = True
    
    match type:
        case "Account":
            host = "https://accounts.rec.net"
            endpoint = f"/account?username={name}"
            request = rec_net.accounts.account(name).get() if is_id else rec_net.accounts.account().get({"username": name})
            exception = AccountNotFound(name)
        case "Room":
            host = "https://rooms.rec.net"  
            endpoint = f"/rooms/{name}" if is_id else f"/rooms?name={name}"
            request = rec_net.rooms.rooms(name).get() if is_id else rec_net.rooms.rooms().get({"name": name})
            exception = RoomNotFound(name)
        case "Image":
            host = "https://api.rec.net"
            endpoint = f"/api/images/v4/{name}"
            request = rec_net.api.images.v4(name).get()
            exception = ImageNotFound(name)
        case "Event":
            host = "https://api.rec.net"
            endpoint = f"/api/playerevents/v1/{name}" if is_id else f"/api/playerevents/v1/search?query={name}&take=1"
            request = rec_net.api.playerevents.v1(name).get() if is_id else rec_net.api.playerevents.v1.search().get({"query": name, "take": 1})
            exception = EventNotFound(name)

    resp = await request.fetch()
    if not resp.success or not resp.data: raise exception

    view = RawDataShowcase(ctx, type, resp.data, host + endpoint)
    await view._respond()