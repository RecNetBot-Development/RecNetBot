from embeds.base.embed import DefaultEmbed as Embed

def data_embed(formatting, data, explanations=False):
    em = Embed(
        description=""
    )
    for key, value in data.items():
        if explanations:
            data_format = formatting.get(key, {
                "name": key,
                "value": "```{value}```",
                "info": "Unknown, new property!",
                "inline": False
            })
            
            em.description += f"""
**{data_format['name']}**
{data_format['info']}\n{data_format['value'].format(value=value)}\r
            """

        else:
            em.add_field(
                name=key, 
                value=f"""```{value}```\n""",
                inline=False
            )
    return em