from embeds.base.embed import DefaultEmbed as Embed
from embeds.headers.profile_header import profile_header
        
"""Makes an embed for a toxicity check"""
def toxicity_embed(user, toxicity_ratings):
    em = profile_header(user, Embed())
    
    em.title = f"{user.display_name}'s toxicity"
    em.description = f"```{user.bio}```" if user.bio else "User hasn't written a bio!"

    # Don't include toxicity if no bio
    if not user.bio: return em
    
    conclusion = ""
    for type, value in toxicity_ratings:
        conclusion += f"{round(value * 100)}% `{type.replace('_', ' ').capitalize()}`\n"
    
    em.add_field(
        name="Toxicity Ratings",
        value=conclusion
    )
    
    em.set_footer(text="This is powered by Perspective API. Results shouldn't be taken seriously.")
    
    return em