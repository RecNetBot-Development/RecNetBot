from utility import load_cfg, respond
from discord.commands import slash_command, Option # Importing the decorator that makes slash commands.
from base_commands.base_profile import base_profile
from rec_net.exceptions import AccountNotFound, InvalidBioForPerspective
from embeds.account.profile.toxicity_embed import toxicity_embed
from googleapiclient.http import HttpError
import json

cfg = load_cfg()

@slash_command(
    debug_guilds=cfg['test_guild_ids'],
    name="toxicity",
    description="Check how toxic a player's bio is."
)
async def cringe(
    self, 
    ctx, 
    username: Option(str, "Enter user's username", required=True)
):
    await ctx.interaction.response.defer()
    
    # Fetch the user
    user = await self.bot.rec_net.account(name=username, includes=["bio"])
    if not user: raise AccountNotFound(username)

    bio = bio.replace("\r", "")

    # Get toxicity rating
    analyze_request = {
        'comment': { 'text': bio if bio else 'User has not written a bio!'},
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
        response = self.bot.discovery.comments().analyze(body=analyze_request).execute()
    except HttpError:
        raise InvalidBioForPerspective(username, bio)
        
    results_raw, results = response["attributeScores"], []
    
    # Sort toxicity ratings
    for key, value in results_raw.items():
        results.append((key, value['summaryScore']['value']))
    results.sort(reverse=True, key=lambda x: x[1]) 
   
    # Form response
    await respond(
        ctx,
        embed=toxicity_embed(user, results)
    )
