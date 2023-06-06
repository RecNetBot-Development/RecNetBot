import discord

def get_rarity_color(rarity = 1):
    """ Returns the Discord color for each rarity """

    match rarity:
        case 5:
            color = discord.Color.orange()
        case 4:
            color = discord.Color.purple()
        case 3:
            color = discord.Color.blue()
        case 2:
            color = discord.Color.green()
        case _:
            color = discord.Color.dark_gray()

    return color