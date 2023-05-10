import math
from io import BytesIO

import PIL.ImageColor
from PIL import Image, ImageDraw, ImageFont


def time_to_dec(t):
    hours = t.hour
    minutes = t.minute
    return hours + minutes/60.0


def draw_timeline(objects):
    # (almost) empty image if no object is given
    if len(objects) == 0:
        bitmap = Image.new("RGB", (1000, 1), color='white')
        with BytesIO() as output:
            bitmap.save(output, format="PNG")
            contents = output.getvalue()
        return contents

    # prepare rows
    t_min = 24
    t_max = 0
    row_count = 1
    lst_start = []
    lst_end = []
    lst_rows = []
    lst_text = []
    rows_max = [0.0]
    for obj in objects:
        t_start = time_to_dec(obj.start_time)
        t_end = time_to_dec(obj.end_time)
        lst_start.append(t_start)
        lst_end.append(t_end)
        lst_text.append(str(obj.staff_count))
        if t_start < t_min:
            t_min = math.floor(t_start)
        if t_end > t_max:
            t_max = math.ceil(t_end)
        # allocate space in rows
        i = 0
        while t_start + 1/60 <= rows_max[i]:
            i += 1
            # new row if no existing row has free space
            if i >= len(rows_max):
                rows_max.append(0.0)
                row_count += 1
        # set the allocated row for obj and block this row until the end time
        rows_max[i] = t_end
        lst_rows.append(i)

    # constants
    h_row = 50
    width = 1500
    height = h_row*(row_count+1)
    w_row = width / (t_max - t_min)
    mgs = h_row/12
    black = PIL.ImageColor.getrgb('#000000')
    white = PIL.ImageColor.getrgb('#FFFFFF')
    blue = PIL.ImageColor.getrgb('#039BE5')
    amber = PIL.ImageColor.getrgb('#FFB300')
    grey1 = PIL.ImageColor.getrgb('#E0E0E0')
    grey2 = PIL.ImageColor.getrgb('#BDBDBD')
    grey3 = PIL.ImageColor.getrgb('#757575')
    font_family = "arial.ttf"

    # init
    bitmap = Image.new("RGB", (width, height))
    img = ImageDraw.Draw(bitmap)

    # clear image
    fillcolor = white
    fontsize = height / 4
    font = ImageFont.truetype(font_family, int(fontsize))
    img.rectangle((0, 0, width, height), fill=fillcolor, outline=fillcolor)
    # grid pattern
    for i in range(t_max - t_min + 1):
        if i % 2 == 0:
            fillcolor = grey1
        else:
            fillcolor = grey2
        img.rectangle((i*w_row, 0, (i+1)*w_row, height), fill=fillcolor, outline=fillcolor)
        img.text((i*w_row+mgs, 0+mgs), str(t_min+i), fill=black, font=font)
    # draw objects in timeline
    for i in range(len(objects)):
        fillcolor = blue
        start = lst_start[i]-t_min
        end = lst_end[i]-t_min
        tw, th = img.textsize(lst_text[i], font=font)
        w_center = start + (end-start)/2
        row = lst_rows[i]
        h_center = (row + 1) * h_row + h_row/2
        img.rounded_rectangle((start*w_row+mgs, (row+1)*h_row+mgs, end*w_row-mgs, (row+2)*h_row-mgs), radius=mgs,
                              fill=fillcolor, outline=fillcolor)
        img.text((w_center*w_row-tw/2, h_center-th/2-mgs/2), lst_text[i], fill=white, font=font, align='center')

    # save image and return it
    with BytesIO() as output:
        bitmap.save(output, format="PNG")
        contents = output.getvalue()
    return contents
