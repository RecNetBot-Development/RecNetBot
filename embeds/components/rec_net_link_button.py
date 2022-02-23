import discord

class RecNetLinkButton(discord.ui.Button):
    def __init__(self, type, content, row=0):
        super().__init__(
            style=discord.ButtonStyle.link, 
            label="RecNet", 
            url=f"https://rec.net/{type}/{content}",
            row=row
        )
        
        

       

        

    