import discord
from discord import ApplicationContext
from discord.commands import slash_command, Option
from utils.converters import FetchAccount
from embeds import get_default_embed
from utils import sanitize_bio, img_url
from recnetpy.dataclasses.account import Account
from googleapiclient.http import HttpError
from exceptions import ConnectionNotFound
from utils.autocompleters import account_searcher

@slash_command(
    name="toxicity",
    description="See how toxic an AI sees a player's bio!"
)
async def toxicity(
    self, 
    ctx: ApplicationContext, 
    account: Option(FetchAccount, name="username", description="Enter RR username", default=None, required=False, autocomplete=account_searcher)
):
    await ctx.interaction.response.defer()
    
    if not account:  # Check for a linked RR account
        account = await self.bot.cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
    
    bio = await account.get_bio()
    if not bio:
        em = get_default_embed()
        em.description = "This account doesn't have a bio!"
        return await ctx.respond(embed=em)
    
    # Get toxicity rating
    analyze_request = {
        'comment': {'text': sanitize_bio(bio)},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {}
        }
    }
    
    try:
        response = self.bot.perspective.comments().analyze(body=analyze_request).execute()
        results_raw, results = response["attributeScores"], []
        for key, value in results_raw.items():
            results.append((key, value['summaryScore']['value']))
    except HttpError:
        results = DEFAULT_RESULTS
    
    # Sort toxicity ratings
    results.sort(reverse=True, key=lambda x: x[1]) 
   
    # Form response
    await ctx.respond(
        embed=toxicity_embed(account, results)
    )
    
    
def toxicity_embed(account: Account, toxicity_ratings: dict) -> discord.Embed:
    em = get_default_embed()
    
    em.title = f"{account.display_name}'s toxicity"
    em.description = f"```{sanitize_bio(account.bio)}```"
    
    conclusion = ""
    for type, value in toxicity_ratings:
        conclusion += f"{round(value * 100)}% `{type.replace('_', ' ').capitalize()}`\n"
    
    em.add_field(
        name="Toxicity Ratings",
        value=conclusion
    )
    
    em.set_thumbnail(url=img_url(account.profile_image, crop_square=True))
    
    em.set_footer(text="This is powered by Perspective API. Results shouldn't be taken seriously.")
    
    return em
    
    
DEFAULT_RESULTS = [
    ('TOXICITY', 0),
    ('SEVERE_TOXICITY', 0),
    ('IDENTITY_ATTACK', 0),
    ('INSULT', 0),
    ('PROFANITY', 0),
    ('THREAT', 0)
]