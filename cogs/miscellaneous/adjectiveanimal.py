from utility import load_cfg, respond
from discord.commands import slash_command # Importing the decorator that makes slash commands.
from embeds import AdjectiveAnimal

cfg = load_cfg()

@slash_command(
    debug_guilds=cfg['test_guild_ids'],
    name="adjectiveanimal",
    description="Generate a random Adjective Animal username based on the official adjectives and nouns!"
)
async def adjectiveanimal(
    self, 
    ctx
):
    await ctx.interaction.response.defer()
    view, embed = AdjectiveAnimal(ctx).start()
    await respond(ctx, embed=embed, view=view)
    