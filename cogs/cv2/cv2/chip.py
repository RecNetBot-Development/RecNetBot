import discord
from discord.commands import slash_command, Option
from utils.cv2 import get_chip, Chip
from utils.autocompleters import cv2_searcher
from embeds import get_default_embed
from resources import get_emoji

class Menu(discord.ui.View):
    def __init__(self, chip: Chip):
        super().__init__()

        # Patch name
        chip_name = chip.name.lower().replace(" ", "-")

        # Link button
        link_btn = discord.ui.Button(
            label="Chip",
            url=f"https://www.recroomcircuits.com/chip/{chip_name}",
            style=discord.ButtonStyle.link
        )
        self.add_item(link_btn)


@slash_command(
    name="chip",
    description="Lookup a CV2 chip and view its ports and properties."
)
async def chip(
    self, 
    ctx: discord.ApplicationContext, 
    chip_name: Option(str, name="chip", description="Enter chip name", required=True, autocomplete=cv2_searcher)
):
    await ctx.interaction.response.defer()

    # Get the chip
    chip = await get_chip(chip_name)

    # Embed skeleton
    em = get_default_embed()

    # Guard clause
    if not chip:
        em.description = f"Couldn't find `{chip_name}`!\n" \
                          "- Use the integrated search tool while typing a chip's name.\n" \
                          "- Make sure your Discord client isn't out of date for it to work."
        return await ctx.respond(embed=em)
    
    em.title = chip.name
    em.description = chip.description

    # Port template
    port = "`{name}` • ({type})"

    # Inputs
    inputs = []
    for i in chip.inputs:
        input = port.format(name=i.name, type=i.type)
        inputs.append(input)

    em.add_field(name="Inputs", inline=True, value=
        "\n".join(inputs)
    )

    # Outputs
    outputs = []
    for i in chip.outputs:
        output = port.format(name=i.name, type=i.type)
        outputs.append(output)

    em.add_field(name="Outputs", inline=True, value=
       "\n".join(outputs)
    )

    # Chip properties
    true = get_emoji("correct")
    false = get_emoji("incorrect")

    # All the properties will be stored here
    properties = []

    # Role assignment property
    role_temp = "`{0} Role Assignment Risk `"
    properties.insert(
        0 if chip.is_role_risk else 1, 
        role_temp.format(true if chip.is_role_risk else false)
    )

    # Trolling property
    troll_temp = "`{0} Trolling Risk `"
    properties.insert(
        0 if chip.is_trolling_risk else 1, 
        troll_temp.format(true if chip.is_trolling_risk else false)
    )

    # Beta property
    beta_temp = "`{0} Beta `"
    properties.insert(
        0 if chip.is_beta else 1, 
        beta_temp.format(true if chip.is_beta else false)
    )

    # Deprecation property
    deprecated_temp = "`{0} Deprecated `"
    properties.insert(
        0 if chip.is_deprecated else 1, 
        deprecated_temp.format(true if chip.is_deprecated else false)
    )
    
    # Add them all together
    em.add_field(name="Properties", inline=False, value=
        " ".join(properties)
    )

    # Filter paths
    filters = [f"`{'/'.join(filter.path)}`" for filter in chip.filters]
    em.add_field(name="Path" if len(filters) <= 1 else "Paths", inline=False, value=
        "\n".join(filters)
    )

    # UUID
    em.set_footer(text=f"UUID: {chip.uuid}")

    #menu_view = Menu(chip=chip)
    #await ctx.respond(embed=em, view=menu_view)
    await ctx.respond(embed=em)