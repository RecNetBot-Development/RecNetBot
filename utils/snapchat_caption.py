from PIL import Image, ImageDraw, ImageFont
import re
import io
import discord
import time
import httpx
from typing import Tuple

def snapchat_caption(image_bytes: bytes, text: str, filename: str = None):
    # open target image
    im = Image.open(image_bytes).convert("RGBA")
    if not text: return im

    # add line break every 80th char
    text = re.sub("(.{80})", "\\1\n", text, 0, re.DOTALL)
    text = text.rstrip() # strip trailing newline

    # make a blank image for the text box, initialized to transparent text box color
    box = Image.new("RGBA", im.size, (0, 0, 0, 0))

    size_chart = {
        480: (40, 200),
        720: (50, 350),
        1080: (60, 400),
        1440: (65, 500)
    }

    # draw text box
    #height = 350
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
    out.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    #return discord.File(fp=img_byte_arr, filename=f"f{filename if filename else 'output'}.png")
    return (discord.File(fp=img_byte_arr, filename=f"{text}.png"), out)

if __name__ == "__main__":
    data = httpx.get("https://img.rec.net/6ft3acy3jac3b1hmiiv5dsua4.jpg").content
    start = time.perf_counter()
    bytes = io.BytesIO(data)
    file, out = snapchat_caption(bytes, "hello wolrd")
    print(f"{time.perf_counter() - start} seconds")
    out.show()