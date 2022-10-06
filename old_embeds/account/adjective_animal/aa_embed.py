from embeds.base.embed import DefaultEmbed as Embed

def adjective_animal_embed(name):
    # Define embed
    em = Embed(
        title="Your Animal Adjective name",
        description = f"""
`{name}`
*Generated from the official adjectives and nouns!*
        """
    )
    return em