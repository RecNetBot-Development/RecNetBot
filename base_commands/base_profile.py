from embeds import profile_embed, Profile
from rec_net.exceptions import AccountNotFound

async def base_profile(rec_net, ctx, username, specified):
    options = {
        "posts": {
            "take": 2**16           
        }, 
        "feed": {
            "take": 2**16
        }
    }
    
    match specified:
        case "Profile":
            includes = ["bio", "progress", "subs"]
        case "Level":
            includes = ["progress"]
        case "Bio":
            includes = ["bio"]
        case _:
            includes = []
        
    user = await rec_net.account(name=username, includes=includes, options=options)
    if not user: raise AccountNotFound(username)
        
    embed = profile_embed(user, specified)
    view = Profile(ctx, user)
    return embed, view  # Embed, View