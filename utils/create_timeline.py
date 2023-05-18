import math
from io import BytesIO

import PIL.ImageColor
from PIL import Image, ImageDraw, ImageFont


def time_to_dec(t):
    hours = t.hour
    minutes = t.minute
    return hours + minutes/60.0


def empty_timeline():
    bitmap = Image.new("RGB", (1000, 1), color='white')
    with BytesIO() as output:
        bitmap.save(output, format="PNG")
        contents = output.getvalue()
    return contents


def draw_timeline(objects, target):
    # (almost) empty image if no object is given
    if len(objects) == 0:
        return empty_timeline()

    # prepare rows
    t_min = 24
    t_max = 0
    row_count = 1
    lst_desc = []
    lst_start = []
    lst_end = []
    lst_rows = []
    lst_text = []
    lst_weekday = []
    lst_highlight = []  # 0: normal (blue) | 1: no employee (grey) | 2: highlighted (yellow)
    rows_max = [0.0]

    for obj in objects:
        # since data structure is different filter target
        if target == 'demand':
            lst_text.append(str(obj.staff_count))
            lst_highlight.append(0)
            t_start = time_to_dec(obj.start_time)
            t_end = time_to_dec(obj.end_time)
        elif target == 'day_templates':
            lst_text.append(obj.department.name + '\n' + obj.name)
            t_start = time_to_dec(obj.start_time)
            t_end = time_to_dec(obj.end_time)
            lst_highlight.append(0)
        elif target == 'shifts':
            if obj.employee:
                employee = str(obj.employee)
            else:
                employee = '(not assigned)'
            text = obj.department.name + '\n' + employee
            if obj.note != '':
                text += '\n' + obj.note
            lst_text.append(text)
            t_start = time_to_dec(obj.start)
            t_end = time_to_dec(obj.end)
            if obj.highlight:
                lst_highlight.append(2)
            elif not obj.employee:
                lst_highlight.append(1)
            else:
                lst_highlight.append(0)
        elif target == 'shifts_listed':
            desc = obj.start.strftime("%A\n%d.%m.%Y\n%H:%M ") + obj.end.strftime("- %H:%M")
            lst_desc.append(desc)
            weekday = int(obj.start.weekday())
            lst_weekday.append(weekday)
            text = obj.department.name
            if obj.note != '':
                text += '\n' + obj.note
            lst_text.append(text)
            t_start = time_to_dec(obj.start)
            t_end = time_to_dec(obj.end)
            if obj.highlight:
                lst_highlight.append(2)
            elif not obj.employee:
                lst_highlight.append(1)
            else:
                lst_highlight.append(0)
        else:
            return empty_timeline()

        if t_end < t_start:
            t_end += 24
        lst_start.append(t_start)
        lst_end.append(t_end)
        if t_start < t_min:
            t_min = math.floor(t_start)
        if t_end > t_max:
            t_max = math.ceil(t_end)

        if target == 'shifts_listed':
            # new row for every shift
            lst_rows.append(row_count-1)
            if row_count < len(objects):
                row_count += 1
        else:
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
    desc_col = 0
    h_row = 75
    width = 1500
    height = h_row*(row_count+1)
    # descriptor column with 20% width
    if target == 'shifts_listed':
        desc_col = width*0.2
    w_col = (width-desc_col) / (t_max - t_min)
    mgs = h_row/20
    black = PIL.ImageColor.getrgb('#000000')
    white = PIL.ImageColor.getrgb('#FFFFFF')
    blue = PIL.ImageColor.getrgb('#039BE5')
    lightblue = PIL.ImageColor.getrgb('#29B6F6')
    amber = PIL.ImageColor.getrgb('#FFB300')
    grey1 = PIL.ImageColor.getrgb('#FAFAFA')
    grey2 = PIL.ImageColor.getrgb('#EEEEEE')
    grey3 = PIL.ImageColor.getrgb('#424242')
    grey4 = PIL.ImageColor.getrgb('#757575')
    font_family = "arial.ttf"

    # init
    bitmap = Image.new("RGB", (width, height))
    img = ImageDraw.Draw(bitmap)

    # clear image
    fillcolor = white
    img.rectangle((0, 0, width, height), fill=fillcolor, outline=fillcolor)

    # grid pattern
    fontsize = h_row / 3
    font = ImageFont.truetype(font_family, int(fontsize))
    # horizontal
    for i in range(row_count+1):
        if i == 0:
            fillcolor = grey4
        elif i % 2 == 0:
            fillcolor = grey2
        else:
            fillcolor = grey1
        img.rectangle((0, i*h_row, width, (i+1)*h_row), fill=fillcolor, outline=fillcolor)
    if desc_col > 0:
        fontsize = h_row / 3.5
        font = ImageFont.truetype(font_family, int(fontsize))
        txt = 'Date\nTime'
        tw, th = img.textsize(txt, font=font)
        img.text((2*mgs, h_row/2-th/2), txt, fill=white, font=font)
    # vertical
    fontsize = h_row / 3
    font = ImageFont.truetype(font_family, int(fontsize))
    for i in range(t_max - t_min):
        h = t_min+i if t_min+i < 24 else t_min+i-24
        tw, th = img.textsize(str(h), font=font)
        w_center = i*w_col - tw/2
        if i > 0 or desc_col > 0:
            img.line((desc_col+i*w_col, 3*h_row/4, desc_col+i*w_col, h_row), fill=white, width=1)
            img.line((desc_col+i*w_col, h_row, desc_col+i*w_col, height), fill=grey3, width=1)
        if i == 0 and desc_col == 0:
            img.text((desc_col+mgs, h_row/2-th/2), str(h), fill=white, font=font)
        else:
            img.text((desc_col+w_center, h_row/2-th/2), str(h), fill=white, font=font)
    # draw objects in timeline
    for i in range(len(objects)):
        row = lst_rows[i]
        h_center = (row+1)*h_row + h_row/2
        # extra descriptor column
        if target == 'shifts_listed':
            fontsize = h_row / 4
            font = ImageFont.truetype(font_family, int(fontsize))
            tw, th = img.textsize(lst_text[i], font=font)
            img.text((2*mgs, h_center - th/2 - 3*mgs), lst_desc[i],
                     fill=black, font=font, align='left')
            # saturday and sunday markings
            l_width = 10
            if lst_weekday[i] == 5:
                img.line((desc_col-l_width/2-1, (row+1)*h_row, desc_col-l_width/2-1, (row+2)*h_row),
                         fill=blue, width=l_width)
            if lst_weekday[i] == 6:
                img.line((desc_col-l_width/2-1, (row+1)*h_row, desc_col-l_width/2-1, (row+2)*h_row),
                         fill=amber, width=l_width)
        fontsize = h_row / 4
        font = ImageFont.truetype(font_family, int(fontsize))
        start = lst_start[i]-t_min
        end = lst_end[i]-t_min
        tw, th = img.textsize(lst_text[i], font=font)
        # make font smaller if text is bigger than row
        while th > h_row-4*mgs:
            fontsize -= 1
            font = ImageFont.truetype(font_family, int(fontsize))
            tw, th = img.textsize(lst_text[i], font=font)
        w_center = start + (end-start)/2
        if lst_highlight[i] == 1:
            fillcolor = lightblue
            textcolor = white
        elif lst_highlight[i] == 2:
            fillcolor = amber
            textcolor = black
        else:
            fillcolor = blue
            textcolor = white
        img.rounded_rectangle((start*w_col+desc_col+mgs, (row+1)*h_row+mgs, end*w_col+desc_col-mgs, (row+2)*h_row-mgs),
                              radius=mgs, fill=fillcolor, outline=fillcolor)
        img.text((w_center*w_col+desc_col-tw/2, h_center-th/2-mgs/2), lst_text[i],
                 fill=textcolor, font=font, align='center')

    # save image and return it
    with BytesIO() as output:
        bitmap.save(output, format="PNG")
        contents = output.getvalue()
    return contents
