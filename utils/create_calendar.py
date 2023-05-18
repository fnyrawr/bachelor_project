from datetime import datetime, timedelta
from io import BytesIO

import PIL.ImageColor
from PIL import Image, ImageDraw, ImageFont


def str_to_date(d):
    return datetime.strptime(d, "%Y-%m-%d")


def empty_calendar():
    bitmap = Image.new("RGB", (1000, 1), color='white')
    with BytesIO() as output:
        bitmap.save(output, format="PNG")
        contents = output.getvalue()
    return contents


def draw_calendar(start_date=None, end_date=None, center_date=None, objects=None, target=None):
    # (almost) empty image if no object is given
    if len(objects) == 0 or target is None:
        return empty_calendar()

    # prepare rows
    d_center = center_date
    if start_date is None:
        d_min = d_center - timedelta(days=7)
    else:
        d_min = start_date
    if start_date is None:
        d_max = d_center + timedelta(days=6)
    else:
        d_max = end_date
    col_count = len(objects) + 1
    row_count = (d_max-d_min).days+2
    lst_start = []
    lst_end = []
    lst_start_date = []
    lst_end_date = []
    lst_colheader = []
    lst_text = []
    lst_highlight = []  # 0: approved (blue) | 1: sent/not decided (grey) | 2: declined (red)

    for obj in objects:
        # set text of dates and duration
        lst_start_date.append(obj.start_date.strftime("%A") + '\n' + obj.start_date.strftime("%d.%m."))
        if obj.start_date < obj.end_date:
            lst_end_date.append(obj.end_date.strftime("%A") + '\n' + obj.end_date.strftime("%d.%m."))
            text = str((obj.end_date - obj.start_date).days + 1) + ' days'
        else:
            lst_end_date.append('')
            text = '1 day'

        # determine start and end row
        start = (str_to_date(str(obj.start_date)) - d_min).days
        if start < 0:
            start = 0
        end = (str_to_date(str(obj.end_date)) - d_min).days + 1
        if end > row_count-1:
            end = row_count-1
        lst_start.append(start)
        lst_end.append(end)

        # absence only: add text depending on reason
        if target == 'absences':
            if obj.reason == 0 or obj.reason == 1:
                text += '\nsickness'
            elif obj.reason == 2:
                text += '\nprivate related'
            elif obj.reason == 2:
                text += '\nbusiness related'
            else:
                text += '\nother reason'

        # add text depending on status
        if obj.status == 0:
            lst_highlight.append(1)
            text += '\nopen'
        elif obj.status == 1:
            lst_highlight.append(1)
            text += '\nnot decided'
        elif obj.status == 2:
            lst_highlight.append(2)
            text += '\ndeclined'
        else:
            lst_highlight.append(0)
            text += '\napproved'
        lst_colheader.append(str(obj.employee))
        lst_text.append(text)

    # constants [dimensions: A4 landscape page]
    h_row = 150
    width = 2480
    height = 3508
    # adjust row height to fit all lines on one page, leaving a small margin at the bottom
    if row_count * h_row >= height:
        h_row = height / row_count
    w_col = width / col_count
    mgs = h_row/20
    black = PIL.ImageColor.getrgb('#000000')
    white = PIL.ImageColor.getrgb('#FFFFFF')
    blue = PIL.ImageColor.getrgb('#039BE5')
    red = PIL.ImageColor.getrgb('#E53935')
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
    # vertical
    for i in range(row_count):
        if i == 0:
            fillcolor = grey4
        elif i % 2 == 0:
            fillcolor = grey2
        else:
            fillcolor = grey1
        img.rectangle((0, i*h_row, width, (i+1)*h_row), fill=fillcolor, outline=fillcolor)

        # color coding for today, weekend
        d = (d_min + timedelta(days=i - 1))
        if d == d_center:
            fillcolor = amber
            img.rectangle((0, i*h_row, width, (i+1)*h_row), fill=fillcolor, outline=fillcolor)
        l_width = 10
        fontcolor = black
        if i > 0 and d.strftime("%w") == '6':
            img.line((w_col-l_width/2-1, i*h_row, w_col-l_width/2-1, (i+1)*h_row), fill=blue, width=l_width)
        if i > 0 and d.strftime("%w") == '0':
            img.line((w_col-l_width/2-1, i*h_row, w_col-l_width/2-1, (i+1)*h_row), fill=amber, width=l_width)
        # print out dates
        if i > 0:
            d_str = d.strftime("%A") + '\n' + d.strftime("%d. %B %Y")
            tw, th = img.textsize(str(d_str), font=font)
            h_center = i*h_row + h_row/2 - th/2
            img.text((2*mgs, h_center), str(d_str), fill=fontcolor, font=font)
    # horizontal
    for i in range(col_count):
        if i > 0:
            img.line((i*w_col, h_row/2, i*w_col, h_row), fill=white, width=1)
            img.line((i*w_col, h_row, i*w_col, row_count*h_row), fill=grey3, width=1)
    fontcolor = white
    text = 'Date'
    tw, th = img.textsize(str(text), font=font)
    h_center = h_row/2 - th/2
    img.text((2*mgs, h_center), str(text), fill=fontcolor, font=font)

    # draw objects in timeline
    for i in range(len(objects)):
        # draw column headline
        fontsize = h_row / 3
        font = ImageFont.truetype(font_family, int(fontsize))

        text = lst_colheader[i]
        tw, th = img.textsize(text, font=font)
        img.text(((i+1)*w_col + w_col/2 - tw/2, h_row/2 - th/2), text, fill=fontcolor, font=font)

        # draw calendar marker
        fontsize = h_row / 4
        font = ImageFont.truetype(font_family, int(fontsize))
        start = lst_start[i]+1
        end = lst_end[i]+1
        tw, th = img.textsize(lst_text[i], font=font)
        h_center = (start + (end-start)/2)*h_row
        h_start = start*h_row
        h_end = end*h_row
        w_center = (i+1)*w_col + w_col/2
        if lst_highlight[i] == 1:
            fillcolor = grey3
            textcolor = white
        elif lst_highlight[i] == 2:
            fillcolor = red
            textcolor = white
        else:
            fillcolor = blue
            textcolor = white
        img.rounded_rectangle(((i+1)*w_col+mgs, start*h_row+mgs, (i+2)*w_col-mgs, end*h_row-mgs), radius=mgs,
                              fill=fillcolor, outline=fillcolor)
        # draw text
        img.text((w_center-tw/2, h_center-th/2), lst_text[i], fill=textcolor, font=font, align='center')
        # draw dates
        img.text(((i+1)*w_col + 2*mgs, h_start+2*mgs), lst_start_date[i], fill=textcolor, font=font, align='left')
        tw, th = img.textsize(lst_end_date[i], font=font)
        img.text(((i+2)*w_col-tw-2*mgs, h_end-th-2*mgs), lst_end_date[i], fill=textcolor, font=font, align='right')

    # save image and return it
    with BytesIO() as output:
        bitmap.save(output, format="PNG")
        contents = output.getvalue()
    return contents
