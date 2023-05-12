from datetime import datetime, timedelta
from io import BytesIO

import PIL.ImageColor
from PIL import Image, ImageDraw, ImageFont

from utils.create_timeline import time_to_dec


def empty_shiftplan():
    bitmap = Image.new("RGB", (1000, 1), color='white')
    with BytesIO() as output:
        bitmap.save(output, format="PNG")
        contents = output.getvalue()
    return contents


def draw_shiftplan(objects=None, department=None, target=None):
    # (almost) empty image if no object is given
    if len(objects) == 0 or target is None:
        return empty_shiftplan()

    # prepare dimensions
    col_count = len(objects)+1
    row_count = len(objects[0])

    # constants [dimensions: A4 landscape page]
    h_row = 150
    width = 3508
    height = 2480

    if row_count*h_row > height:
        h_row = height / row_count

    w_col = width / col_count
    mgs = h_row/20
    black = PIL.ImageColor.getrgb('#000000')
    white = PIL.ImageColor.getrgb('#FFFFFF')
    blue = PIL.ImageColor.getrgb('#039BE5')
    amber = PIL.ImageColor.getrgb('#FFB300')
    darkamber = PIL.ImageColor.getrgb('#FF6F00')
    grey1 = PIL.ImageColor.getrgb('#FAFAFA')
    grey2 = PIL.ImageColor.getrgb('#EEEEEE')
    grey3 = PIL.ImageColor.getrgb('#424242')
    grey4 = PIL.ImageColor.getrgb('#757575')

    l_width = 15
    hl_width = int(l_width/2)

    font_family = "arial.ttf"

    # init
    bitmap = Image.new("RGB", (width, height))
    img = ImageDraw.Draw(bitmap)

    # clear image
    fillcolor = white
    img.rectangle((0, 0, width, height), fill=fillcolor, outline=fillcolor)

    # grid pattern
    fontsize = h_row / 4
    font = ImageFont.truetype(font_family, int(fontsize))
    # vertical
    for i in range(row_count):
        if i == 0:
            fillcolor = grey3
        elif i % 2 == 0:
            fillcolor = grey2
        else:
            fillcolor = grey1
        img.rectangle((0, i*h_row, width, (i+1)*h_row), fill=fillcolor, outline=fillcolor)
        # mark weekends
        i_sat = 6
        i_sun = 7
        img.line((i_sat*w_col, h_row - l_width/2+1, (i_sat+1)*w_col, h_row - l_width/2+1), fill=blue, width=l_width)
        img.line((i_sun*w_col, h_row - l_width/2+1, (i_sun+1)*w_col, h_row - l_width/2+1), fill=amber, width=l_width)

    # horizontal
    fontcolor = white
    title = (objects[0][0]).strftime("Week %W") + '\n' + department.name
    tw, th = img.textsize(title, font=font)
    img.text((2*mgs, h_row / 2 - th / 2), title, fill=fontcolor, font=font,
             align='left')

    for i in range(col_count):
        if i > 0:
            # draw lines between dates
            img.line((i * w_col, h_row/2, i * w_col, h_row), fill=white, width=1)
            img.line((i*w_col, h_row, i*w_col, h_row*row_count), fill=grey3, width=1)
            # print out dates
            d = objects[i-1][0]
            d_str = d.strftime("%A") + '\n' + d.strftime("%d. %B %Y")
            tw, th = img.textsize(str(d_str), font=font)
            img.text((i*w_col + w_col/2 - tw/2, h_row/2 - th/2), str(d_str), fill=fontcolor, font=font, align='center')

    # draw employee names
    for i in range(len(objects[0])):
        if i > 0:
            fontcolor = black
            text = str(objects[1][i].employee)
            if text == 'None':
                fontcolor = grey4
                text = 'unassigned'
            tw, th = img.textsize(text, font=font)
            img.text((2*mgs, i*h_row + h_row/2 - th/2), text, fill=fontcolor, font=font, align='left')

    # draw shifts
    for i in range(len(objects)):
        for j in range(len(objects[i])):
            # i: col | j: row
            # skip j==0 which contains just the Date
            if j > 0:
                fontsize = h_row / 4
                font = ImageFont.truetype(font_family, int(fontsize))

                text = ''
                entry = objects[i][j]
                # draw absent and holiday
                if entry.etype in ['Absent', 'Holiday']:
                    fontcolor = grey3
                    text = entry.etype
                    tw, th = img.textsize(text, font=font)
                    img.text(((i+1)*w_col + w_col/2 - tw/2, j*h_row + h_row/2 - th/2),
                             text, fill=fontcolor, font=font, align='center')
                    if entry.etype == 'Absent':
                        img.line(((i+1)*w_col+1, j*h_row+hl_width/2, (i+2)*w_col-1, j*h_row+hl_width/2),
                                 fill=amber, width=hl_width)
                    else:
                        img.line(((i+1)*w_col+1, j*h_row+hl_width/2, (i+2)*w_col-1, j*h_row+hl_width/2),
                                 fill=blue, width=hl_width)
                # draw shift
                elif entry.etype == 'Shift':
                    if entry.shift.highlight:
                        img.rectangle(((i+1)*w_col+1, j*h_row+1, (i+2)*w_col-1, j*h_row + h_row/3 + mgs), fill=amber)
                        # mark shifts with grey lines above
                        img.line(((i+1)*w_col+1, j*h_row+hl_width/2, (i+2)*w_col-1, j*h_row+hl_width/2),
                                 fill=grey4, width=hl_width)

                    # define if employee's shift is in the displayed department
                    if entry.shift.employee:
                        dep = department.id
                        emp_dep = entry.shift.employee.department.id
                        sft_dep = entry.shift.department.id
                        if (emp_dep == dep and sft_dep == emp_dep) or (emp_dep != dep and sft_dep == dep):
                            other_department = False
                            fontcolor = black
                        else:
                            other_department = True
                            fontcolor = grey4
                    else:
                        other_department = False
                        fontcolor = black
                        img.line(((i+1)*w_col+1, j*h_row+hl_width/2, (i+2)*w_col-1, j*h_row+hl_width/2),
                                 fill=darkamber, width=hl_width)

                    # change color for better contrast if shift is highlighted
                    if entry.shift.highlight:
                        fontcolor = black

                    # print time
                    time = entry.shift.start.strftime("%H:%M") + ' - ' + entry.shift.end.strftime("%H:%M")
                    tw, th = img.textsize(time, font=font)
                    img.text(((i+1)*w_col + w_col/2 - tw/2, j*h_row + 2*mgs),
                             time, fill=fontcolor, font=font, align='center')

                    if not other_department:
                        # print hours and break
                        fontcolor = black
                        hrs = str(time_to_dec(entry.shift.get_work_hours())) + ' hours'
                        tw, th = img.textsize(hrs, font=font)
                        img.text(((i+1)*w_col + 2*mgs, j*h_row + h_row/2 - th/2),
                                 hrs, fill=fontcolor, font=font, align='left')
                        fontcolor = grey4
                        brk_min = int(time_to_dec(entry.shift.break_duration)*60)
                        if brk_min > 0:
                            brk = str(brk_min) + ' min'
                        else:
                            brk = 'no break'
                        tw, th = img.textsize(brk, font=font)
                        img.text(((i+2)*w_col - 2*mgs - tw, j*h_row + h_row/2 - th/2),
                                 brk, fill=fontcolor, font=font, align='right')

                        # print note
                        fontsize = h_row / 5
                        font = ImageFont.truetype(font_family, int(fontsize))
                        fontcolor = black
                        note = entry.shift.note
                        tw, th = img.textsize(note, font=font)
                        img.text(((i+1)*w_col + w_col/2 - tw/2, (j+1) * h_row - 2*mgs - th),
                                 note, fill=fontcolor, font=font, align='center')
                    else:
                        # employee has shift in other department
                        dep = str(entry.shift.department)
                        tw, th = img.textsize(dep, font=font)
                        img.text(((i+1)*w_col + w_col/2 - tw/2, j*h_row + h_row/2 - th/2),
                                 dep, fill=fontcolor, font=font, align='left')
                        img.line(((i+1)*w_col+1, j*h_row+hl_width/2, (i+2)*w_col-1, j*h_row+hl_width/2),
                                 fill=grey4, width=hl_width)

        # draw work hours
        fontsize = h_row / 5
        font = ImageFont.truetype(font_family, int(fontsize))
        for i in range(len(objects[0])):
            if i > 0 and objects[1][i].employee:
                fontcolor = grey4
                text = '{0:g}'.format(objects[1][i].employee.week_work_hours) + '/' +\
                       str(objects[1][i].employee.work_hours) + ' hours'
                tw, th = img.textsize(text, font=font)
                img.text((w_col - tw - 2*mgs, (i+1)*h_row - th - 2*mgs), text,
                         fill=fontcolor, font=font)

    # save image and return it
    with BytesIO() as output:
        bitmap.save(output, format="PNG")
        contents = output.getvalue()
    return contents
