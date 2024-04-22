import discord
from discord.commands import slash_command
from discord.ext.bridge import BridgeOption as Option
from utils.cv2 import get_chip, get_formatted_port, generate_svg, Chip
from utils.autocompleters import cv2_searcher
from embeds import get_default_embed
from resources import get_emoji
from io import BytesIO

class Menu(discord.ui.View):
    def __init__(self, chip: Chip):
        super().__init__()

        # Link button
        link_btn = discord.ui.Button(
            label="Chip",
            url=f"https://circuits.pages.dev/docs/documentation/chips/{chip.uuid}",
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
    chip_uuid: Option(str, name="chip", description="Enter chip name", required=True, autocomplete=cv2_searcher)
):
    await ctx.interaction.response.defer()

    # Get the chip
    chip = await get_chip(chip_uuid)

    # Embed skeleton
    em = get_default_embed()

    # Guard clause
    if not chip:
        em.description = f"Couldn't find the chip you were looking for!\n" \
                          "- Use the integrated search tool while typing a chip's name.\n" \
                          "- Make sure your Discord client isn't out of date for it to work."
        return await ctx.respond(embed=em)
    
    em.title = chip.name
    em.description = chip.description

    # Port template
    port_temp = "{port} {name} • `{type}`"

    # Inputs
    inputs = []
    for i in chip.inputs:
        input = get_formatted_port(i, port_temp)
        inputs.append(input)
    if not inputs:
        inputs.append("*None*")

    em.add_field(name="Inputs", inline=True, value=
        "\n".join(inputs)
    )

    # Outputs
    outputs = []
    for i in chip.outputs:
        output = get_formatted_port(i, port_temp)
        outputs.append(output)
    if not outputs:
        outputs.append("*None*")

    em.add_field(name="Outputs", inline=True, value=
       "\n".join(outputs)
    )

    # Chip properties
    true = get_emoji("correct")
    false = get_emoji("incorrect")

    # All the properties will be stored here
    properties = []

    # Role assignment property
    role_temp = "`{0}\u00a0Role\u00a0Assignment\u00a0Risk\u00a0`"
    properties.insert(
        0 if chip.is_role_risk else 1, 
        role_temp.format(true if chip.is_role_risk else false)
    )

    # Trolling property
    troll_temp = "`{0}\u00a0Trolling\u00a0Risk\u00a0`"
    properties.insert(
        0 if chip.is_trolling_risk else 1, 
        troll_temp.format(true if chip.is_trolling_risk else false)
    )

    # Beta property
    beta_temp = "`{0}\u00a0Beta\u00a0`"
    properties.insert(
        0 if chip.is_beta else 1, 
        beta_temp.format(true if chip.is_beta else false)
    )

    # Deprecation property
    deprecated_temp = "`{0}\u00a0Deprecated\u00a0`"
    properties.insert(
        0 if chip.is_deprecated else 1, 
        deprecated_temp.format(true if chip.is_deprecated else false)
    )
    
    # Rooms validity properties
    rooms1_temp = "`{0}\u00a0Rooms\u00a01\u00a0`"
    properties.insert(
        0 if chip.is_valid_rooms1 else 1, 
        rooms1_temp.format(true if chip.is_valid_rooms1 else false)
    )
    
    rooms2_temp = "`{0}\u00a0Rooms\u00a02\u00a0`"
    properties.insert(
        0 if chip.is_valid_rooms2 else 1, 
        rooms2_temp.format(true if chip.is_valid_rooms2 else false)
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

    # SVG image generation
    svg_image = generate_svg(chip.uuid, True)
    if svg_image is not None:
        image_file = discord.File(BytesIO(svg_image), filename="chip.png")

        em.set_image(url="attachment://chip.png")

    menu_view = Menu(chip=chip)
    if svg_image is not None:
        await ctx.respond(embed=em, view=menu_view, file=image_file)
    else:
        await ctx.respond(embed=em, view=menu_view)