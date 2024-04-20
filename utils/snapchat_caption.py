from PIL import Image, ImageDraw, ImageFont
import re
import io
import discord
import re

def snapchat_caption(image_bytes: bytes, text: str, filename: str = None):
    """Edits a Snapchat caption on top of an image.

    Returns:
        tuple[discord.File | PIL.Image]: Returns a discord.File and Pillow image object
    """
    im = Image.open(image_bytes).convert("RGBA")
    if not text: return im

    # max text length
    max_text_length = 175
    text = text[:max_text_length]

    # add line break every 80th char
    text = re.sub("(.{35})", "\\1\n", text, 0, re.DOTALL)
    text = text.rstrip() # strip trailing newline

    # make a blank image for the text box, initialized to transparent text box color
    box = Image.new("RGBA", im.size, (0, 0, 0, 0))

    # scale the caption based on resolution
    size_chart = {
        480: (35, 200),
        720: (45, 350),
        1080: (55, 400),
        1440: (60, 500)
    }

    # draw text box
    sizing = size_chart.get(im.height, (40, 350))
    height = sizing[1]
    min_size = sizing[0]
    box_size = min_size + 35 * text.count("\n")
    draw = ImageDraw.Draw(box)
    draw.rectangle((0, (im.height+height)/2-box_size, im.width, (im.height+height)/2+box_size-5), fill=(0, 0, 0, 128))

    # get font
    fnt = ImageFont.truetype("utils/fonts/HelveticaNeueRoman.otf", min_size)

    # draw text
    draw.multiline_text((box.width/2, (box.height+height)/2), text, font=fnt, fill=(255, 255, 255, 255), anchor="mm", align="center", spacing=32)

    # merge images
    out = Image.alpha_composite(im, box)

    # Get bytes
    img_byte_arr = io.BytesIO()
    out.save(img_byte_arr, format='PNG', compress_type=3)
    img_byte_arr.seek(0)
    return (discord.File(fp=img_byte_arr, filename=f"{filename}.png"), out)