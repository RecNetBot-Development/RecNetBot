import discord
from discord.commands import slash_command, Option
from embeds import fetch_image_embed
from utils.converters import FetchImage

@slash_command(
    name="image",
    description="View a Rec Room room's information and statistics."
)
async def image(
    self, 
    ctx: discord.ApplicationContext, 
    image: Option(FetchImage, name="id", description="Enter RR post id", required=True),
):
    await ctx.interaction.response.defer()

    em = await fetch_image_embed(image)
    await ctx.respond(embed=em)

    
    

        

        
