import discord
from discord.commands import slash_command
from embeds import get_default_embed
from resources import get_emoji, get_icon

class Menu(discord.ui.View):
    def __init__(self, server_link: str):
        super().__init__()

        kofi_page = "https://ko-fi.com/jegarde"
        patreon_page = "https://patreon.com/jegarde"

        buttons = [
            discord.ui.Button(label="Patreon", style=discord.ButtonStyle.url, url=patreon_page, emoji=get_emoji("patreon")),
            discord.ui.Button(label="Ko-fi", style=discord.ButtonStyle.url, url=kofi_page, emoji=get_emoji("kofi")),
            discord.ui.Button(label="Home Server", style=discord.ButtonStyle.url, url=server_link, emoji=get_emoji("discord_white"))
        ]
        for i in buttons:
            self.add_item(i)
        
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
    
    # Token emoji
    #token = self.bot.get_emoji(1120446788072120432)

    # Discord emoji
    #discord = self.bot.get_emoji(1120446959799500961)

    await ctx.respond(embed=em, view=Menu(server_link))

    
    

        

        
