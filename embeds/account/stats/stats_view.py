import discord
from embeds.image.stats_embed import stats_embed as img_stats_embed
#from utility.discord_helpers.send import respond as __respond

class NavigationButton(discord.ui.Button):
    def __init__(self, button_type, view):
        super.__init__()
        self.button_type = button_type
        self.view = view
        
        match button_type:
            case "image":
                self.label = "Image"
                
    async def callback(self, interaction):
        self.view.page = self.button_type
        await self.view.change_page(interaction=interaction)

class StatsView(discord.ui.View):
    def __init__(self, rec_net, username):
        super().__init__()
        
        self.rec_net = rec_net
        self.username = username
        
        self.cached_users = {}
        
        self.pages = {
            "image": img_stats_embed
        }
        
        self.page = self.pages['image']
        
    async def change_page(self, interaction):
        user = await self.fetch_user()
        embed = self.create_embed(user)
        await interaction.response.edit_message(embed=embed, view=self)
        
    async def fetch_user(self):
        if self.page in self.cached_users: return self.cached_users[self.page]
        
        match self.page:
            case "image":
                options = {
                    "posts": {
                        "take": 2**16
                    },
                    "feed_options": {
                        "take": 2**16
                    }
                }
                includes = ["posts", "feed"]
                
        user = await self.rec_net.account(name=self.username, includes=includes, options=options)    
        self.cached_users[self.page] = user
        
        return user
    
    def create_embed(self, user):
        return self.pages[self.page](..., user)
        
    async def respond(self, ctx):
        user = await self.fetch_user()
        embed = self.create_embed(user)
        #await __respond(ctx, embed=embed, view=self)