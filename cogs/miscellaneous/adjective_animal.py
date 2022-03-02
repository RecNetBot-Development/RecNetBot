from utility import load_cfg
from discord.commands import slash_command # Importing the decorator that makes slash commands.
from embeds import AdjectiveAnimal

cfg = load_cfg()

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="adjectiveanimal",
    description="Generate a random Adjective Animal username based on the official adjectives and nouns!"
)
async def adjectiveanimal(
    self, 
    ctx
):
    await ctx.interaction.response.defer()
    view, embed = AdjectiveAnimal(ctx).start()
    await ctx.respond(embed=embed, view=view)
    