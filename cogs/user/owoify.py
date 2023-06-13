import discord
from discord.commands import slash_command, Option
from utils.converters import FetchAccount
from embeds import fetch_profile_embed
from exceptions import ConnectionNotFound
from owoify import owoify
from owoify.owoify import Owoness
from utils.autocompleters import account_searcher


@slash_command(
    name="owoify",
    description="View a pwayew's pwofiwe.",
    
)
async def _owoify(
    self,   
    ctx: discord.ApplicationContext,
    account: Option(FetchAccount, name="usewnyame", description="Entew RR u-u-usewnyame", default=None, required=False, autocomplete=account_searcher)
):
    await ctx.interaction.response.defer()
    
    if not account:  # Check for a linked RR account
        account = await self.bot.cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound
    
    em = await fetch_profile_embed(account)
    await ctx.respond(
        embed=owoify_profile_embed(em)
    )
    
    
OWOIFIED = {
    "Level": "Wevew hehe",
    "Subscribers": "Subscwibews",
    "Junior account!": "OwO Junyiow account!",
    "Mature account!": "Matuwe a-account! UwU",
    "Joined": "J-Joinyed",
    "Steam": "Stweam~ :3",
    "Meta": "M-Meta murr~",
    "PlayStation": "PwayStation- (▰˘v˘▰)",
    "Xbox": "Xbowx (*≧▽≦)",
    "iOS": "i-iOS *giggles*",
    "Android": "Andwoid- ɾ⚈▿⚈ɹ",
    "Standalone": "Standawonye hehe",
    "LGBTQIA": "WGBTQIA UwU",
    "Transgender": "Twansgendew (ﾉ´ з `)ノ",
    "Bisexual": "Bwisexuaw OwO",
    "Lesbian": "Wesbian >:3",
    "Pansexual": "Phansexuaw hehe",
    "Asexual": "Asexuaw UwU",
    "Intersex": "Intewsex *gwomps*",
    "Genderqueer": "Gendewqueew OwO",
    "Nonbinary": "Nyonbinyawy Wyonbinyawy (ᗒᗨᗕ)",
    "Aromantic": "Awomantic >3<"
}

def owoify_profile_embed(embed: discord.Embed) -> discord.Embed:
    # Display name
    embed.title = owoify(embed.title, Owoness.Uvu)
    
    # Embed's description
    for og, owo in OWOIFIED.items():  
        embed.description = embed.description.replace(og, owo)

    # Bio
    if "```" in embed.description:  # Check if the bio exists in the embed
        bio = embed.description.split("```")[1]
        embed.description = embed.description.replace(bio, owoify(bio, Owoness.Uvu))
    
    return embed