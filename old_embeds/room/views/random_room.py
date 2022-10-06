import discord
from ..room_embed import room_embed
from utility.emojis import get_emoji
from random import randint

class RandomRoom(discord.ui.View):
    def __init__(self, ctx, rec_net):
        super().__init__(
            timeout=None
        )
        self.ctx = ctx  
        self.rec_net = rec_net
            
    async def start(self):
        embed = await self.find_room_and_return_embed()
        return self, embed 
    
    async def find_room_and_return_embed(self, interaction = None):
        random_id = randint(0, 1000)
        hot_rooms_resp = await self.rec_net.rec_net.rooms.rooms.hot.get(params={"skip": random_id, "take": 1}).fetch()
        room_id = hot_rooms_resp.data['Results'][0]['RoomId']
        room = await self.rec_net.room(id=room_id, info=["tags", "subrooms", "roles", "scores"], includes=["roles", "creator"])
        
        return room_embed(room, random_id+1)
    
    async def handle_message(self, interaction):
        embed = await self.find_room_and_return_embed(interaction)
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(emoji=get_emoji('random'), style=discord.ButtonStyle.primary, row=0, custom_id="persistent:random_room_ui_another")
    async def another(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.handle_message(interaction)