import discord
import random
from discord.commands import slash_command
from embeds import get_default_embed
from resources import get_emoji, get_icon

class Menu(discord.ui.View):
    def __init__(self, server_link: str, emoji1, emoji2):
        super().__init__()

        tip_page = "https://ko-fi.com/jegarde"

        btn = discord.ui.Button(label="Proceed", style=discord.ButtonStyle.url, url=tip_page, emoji=emoji1)
        btn2 = discord.ui.Button(label="Home Server", style=discord.ButtonStyle.url, url=server_link, emoji=emoji2)
        self.add_item(btn)
        self.add_item(btn2)
        
@slash_command(
    name="tip",
    description="In case you're feeling cheerful and would like to say thank you for RecNetBot"
)
async def tip(
    self, 
    ctx: discord.ApplicationContext
):
    server_link = self.bot.config['server_link']

    em = get_default_embed()
    em.title = "Tip Jar"
    em.set_thumbnail(url=get_icon("heart"))
    em.description = \
        f"{get_emoji('cheer_host')} Cheers! Feel free to tip if you're feeling extra cheerful and would like to say thank you for RecNetBot.\n\n" \
        f"{get_emoji('helpful')} By tipping, you support the free nature of RecNetBot and its development.\n\n" \
        f"{get_emoji('discord')} You will also automatically receive an exclusive role in [my home server]({server_link})!"
        
    em.set_footer(text="Tips are processed in Ko-fi", icon_url=get_icon("kofi"))
    
    # Token emoji
    token = self.bot.get_emoji(1120446788072120432)

    # Discord emoji
    discord = self.bot.get_emoji(1120446959799500961)

    await ctx.respond(embed=em, view=Menu(server_link, token, discord))

    
    

        

        
