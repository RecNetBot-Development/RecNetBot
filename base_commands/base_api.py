import discord
from utility import respond, edit_message
from rec_net.exceptions import AccountNotFound, EventNotFound, ImageNotFound, RoomNotFound
from embeds import account_data_embed, image_data_embed, room_data_embed, event_data_embed
from embeds.base.embed import DefaultEmbed as Embed

class RawDataShowcase(discord.ui.View):
    def __init__(self, type, data, content):
        super().__init__(
            timeout=None
        )
        
        self.type = type
        self.content = content
        self.user = None
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
        await edit_message(interaction, embed=self.make_embed(), content=self.content)
        
    async def _respond(self, ctx):
        self.user = ctx.user
        await respond(ctx, view=self, embed=self.make_embed(), content=self.content)
        
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
        case "account":
            host = "https://accounts.rec.net"
            endpoint = f"/account?username={name}"
            request = rec_net.accounts.account(name).get() if is_id else rec_net.accounts.account().get({"username": name})
            exception = AccountNotFound(name)
        case "room":
            host = "https://rooms.rec.net"  
            endpoint = f"/rooms/{name}" if is_id else f"/rooms?name={name}"
            request = rec_net.rooms.rooms(name).get() if is_id else rec_net.rooms.rooms().get({"name": name})
            exception = RoomNotFound(name)
        case "image":
            host = "https://api.rec.net"
            endpoint = f"/api/images/v4/{name}"
            request = rec_net.api.images.v4(name).get()
            exception = ImageNotFound(name)
        case "event":
            host = "https://api.rec.net"
            endpoint = f"/api/playerevents/v1/{name}" if is_id else f"/api/playerevents/v1/search?query={name}&take=1"
            request = rec_net.api.playerevents.v1(name).get() if is_id else rec_net.api.playerevents.v1.search().get({"query": name, "take": 1})
            exception = EventNotFound(name)

    resp = await request.fetch()
    if not resp.success or not resp.data: raise exception

    view = RawDataShowcase(type, resp.data, host + endpoint)
    await view._respond(ctx)