import math
from io import BytesIO

import PIL.ImageColor
from PIL import Image, ImageDraw


def draw_timeline(objects):
    # (almost) empty image if no object is given
    if len(objects) == 0:
        bitmap = Image.new("RGB", (1000, 1), color='white')
        with BytesIO() as output:
            bitmap.save(output, format="PNG")
            contents = output.getvalue()
        return contents

    # constants
    h_row = 50
    width = 1500
    height = h_row*(len(objects)+1)
    t_min = 6
    t_max = 23
    w_row = width / (t_max - t_min)
    black = PIL.ImageColor.getrgb('#000000')
    white = PIL.ImageColor.getrgb('#FFFFFF')
    blue = PIL.ImageColor.getrgb('#039BE5')
    amber = PIL.ImageColor.getrgb('#FFB300')
    grey1 = PIL.ImageColor.getrgb('#E0E0E0')
    grey2 = PIL.ImageColor.getrgb('#BDBDBD')
    grey3 = PIL.ImageColor.getrgb('#757575')

    # init
    bitmap = Image.new("RGB", (width, height))
    img = ImageDraw.Draw(bitmap)

    # clear image
    fillcolor = white
    img.rectangle([(0, 0), (width, height)], fill=fillcolor, outline=fillcolor)
    # grid pattern
    for i in range(t_max - t_min + 1):
        if i % 2 == 0:
            fillcolor = grey1
        else:
            fillcolor = grey2
        img.rectangle([(i*w_row, 0), ((i+1)*w_row, height)], fill=fillcolor, outline=fillcolor)

    # save image and return it
    with BytesIO() as output:
        bitmap.save(output, format="PNG")
        contents = output.getvalue()
    return contents
