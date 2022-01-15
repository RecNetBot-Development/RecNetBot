from os import link
import discord
from rec_net.managers.account import User

class RecNetLinkButton(discord.ui.Button):
    def __init__(self, type: str, content: str):
        super().__init__(
            style=discord.ButtonStyle.link, 
            label="RecNet", 
            url=f"https://rec.net/{type}/{content}"
        )
        
        

       

        

    