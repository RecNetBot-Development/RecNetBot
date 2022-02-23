from discord import Embed
from embeds.finalize_embed import finalize_embed

formatting = {
    "accountId": {
        "name": "Account Id",
        "value": "```{value}```",
        "info": "Account's unique id. Based on total accounts created.",
        "inline": False
    },
    "username": {
        "name": "Username",
        "value": "```{value}```",
        "info": "Account's @ username",
        "inline": False
    },
    "displayName": {
        "name": "Display Name",
        "value": "```{value}```",
        "info": "Account's display name",
        "inline": False
    },
    "profileImage": {
        "name": "Profile Image Name",
        "value": "```{value}```",
        "info": "Account's profile picture's name",
        "inline": False
    },
    "bannerImage": {
        "name": "Banner Image Name",
        "value": "```{value}```",
        "info": "Account's banner picture's name",
        "inline": False
    },
    "isJunior": {
        "name": "Junior Status",
        "value": "```{value}```",
        "info": "Account's junior status",
        "inline": False
    },
    "platforms": {
        "name": "Platform Bit Mask",
        "value": "```{value}```",
        "info": "Account's platform bit mask",
        "inline": False
    },
    "personalPronouns": {
        "name": "Pronoun Bit Mask",
        "value": "```{value}```",
        "info": "Account's pronoun bit mask",
        "inline": False
    },
    "identityFlags": {
        "name": "Identity Bit Mask",
        "value": "```{value}```",
        "info": "Account's sexual identity bit mask",
        "inline": False
    },
    "createdAt": {
        "name": "Creation Date",
        "value": "```{value}```",
        "info": "Account's creation date",
        "inline": False
    }
}

def account_data_embed(ctx, account_data: dict):
    em = Embed()
    for key in account_data:
        data_format = formatting.get(key, {
            "name": key,
            "value": "```{value}```",
            "info": "Unknown, new property!",
            "inline": False
        })
        em.add_field(
            name=data_format['name'], 
            value=f"{data_format['info']}\n{data_format['value'].format(value=account_data[key])}",
            inline=data_format['inline']
        )
    em = finalize_embed(ctx, em)
    return em