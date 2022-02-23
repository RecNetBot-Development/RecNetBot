from utility import load_cfg, img_url
from discord.commands import slash_command, Option # Importing the decorator that makes slash commands.
from embeds import profile_embed, Profile

async def base_profile(rec_net, ctx, username, specified):
    options = {
        "posts": {
            "take": 2**16           
        }, 
        "feed": {
            "take": 2**16
        }
    }
    #includes = ["posts", "feed"]
    includes = []
    
    match specified:
        case "Profile Picture":  # Raw PFP
            user = await rec_net.account(name=username, includes=includes, options=options)
            embed = None
            content = img_url(user.profile_image)
            view = Profile(ctx, user)
        case "Banner":  # Raw banner
            user = await rec_net.account(name=username, includes=includes, options=options)
            embed = None
            content = img_url(user.banner_image) if user.banner_image else "https://cdn.rec.net/static/banners/default_player.png"  # If user doesn't have a banner, supply the default one
            view = Profile(ctx, user)
        case "Platforms": # Just the platforms
            user = await rec_net.account(name=username, includes=includes, options=options)
            embed = profile_embed(ctx, user, "platforms")
            content = None
            view = Profile(ctx, user)
        case "Bio":
            user = await rec_net.account(name=username, includes=["bio"] + includes, options=options)
            embed = profile_embed(ctx, user, "bio")
            content = None
            view = Profile(ctx, user)
        case "Junior":
            user = await rec_net.account(name=username, includes=includes, options=options)
            embed = profile_embed(ctx, user, "junior")
            content = None
            view = Profile(ctx, user)
        case "Level":
            user = await rec_net.account(name=username, includes=includes + ["progress"], options=options)
            embed = profile_embed(ctx, user, "level")
            content = None
            view = Profile(ctx, user)
        case _:  # Full profile as default
            user = await rec_net.account(name=username, includes=["bio", "progress", "subs"] + includes, options=options)
            embed = profile_embed(ctx, user)
            content = None
            view = Profile(ctx, user)
        
    return embed, content, view