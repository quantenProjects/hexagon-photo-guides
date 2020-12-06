#!/bin/env python3

import argparse

from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype("/usr/share/fonts/TTF/Verdana.TTF", 50)

def ap(a, b): # add pair (or sequence)
    return tuple((val + b[i] for i, val in enumerate(a)))

def sp(s, p): # scale pair (or sequence)
    return tuple((val * s for val in p))


def draw_measurment_axis(draw, position, end, horizontal, ticks=25, bigger_ticks=5, tick_length=50, tick_width=2,
                         labels=True):
    """

    :param draw: the draw object
    :param position: the other coordinate, orthogonal to the axis
    :param end: the position on the axis where the measurment should end
    :param horizontal: boolean, if in x direction. If false, than in y
    :param ticks: tick every x pixels
    :param bigger_ticks: bigger tick every x smaller ticks
    :param labels: boolean
    :return:
    """
    ticks = list(range(0, end + 1, ticks))
    print(ticks)
    if horizontal:
        draw.line((0, position, end, position), fill="black", width=tick_width)
    else:
        draw.line((position, 0, position, end), fill="black", width=tick_width)
    for i in range(len(ticks)):
        width = tick_width if i % bigger_ticks != 0 else tick_width * 2
        if horizontal:
            draw.line((ticks[i], position - tick_length, ticks[i], position + tick_length), fill="black", width=width)
        else:
            draw.line((position - tick_length, ticks[i], position + tick_length, ticks[i]), fill="black", width=width)
        if i % bigger_ticks == 0:
            if horizontal:
                draw.text((ticks[i], position + tick_length * (-2 if ((i // bigger_ticks) % 2 == 0) else 1)), str(ticks[i]), fill="black", font=font)
            else:
                draw.text((position + tick_length, ticks[i]), str(ticks[i]), fill="black", font=font)


def draw_test_lines(draw, position, relative_position, color, offset_multiplier=25):
    widths = [1, 2, 3, 4, 8, 16]
    for i in range(len(widths)):
        draw.line((position[0] + i * offset_multiplier, position[1] + i * offset_multiplier,
                   position[0] + i * offset_multiplier + relative_position[0],
                   position[1] + i * offset_multiplier + relative_position[1]), width=widths[i], fill=color)
        draw.text((position[0] + i * offset_multiplier, position[1] + i * offset_multiplier + widths[i] // 2),
                  str(widths[i]), fill="black", font=font)

def draw_bw_test_lines(draw, offset, relative_position, inner_color, inner_width, outer_color, outer_width):
    draw.line( ap((0,0), offset) + ap(relative_position, offset), fill=outer_color, width=outer_width)
    draw.line( ap((0,0), offset) + ap(relative_position, offset), fill=inner_color, width=inner_width)

def checker_board(draw, position, tile_size, color_a="white", color_b="black"):
    for x in range(position[0], position[2]):
        for y in range(position[1], position[3]):
            if (x // tile_size % 2 == 0) != (y // tile_size % 2 == 0):
                draw.point((x, y), fill=color_a)
            else:
                draw.point((x, y), fill=color_b)

def add_margin_indicator(draw, axis, direction, offset, text_anchor, start_pixel, stop_pixel, start, stop, step):
    ax = 1 if axis == "x" else -1
    count = int((stop - start) / step)
    step_width = (stop_pixel - start_pixel) / count
    for i in range(count):
        draw.rectangle(((i * step_width + start_pixel, offset)[::ax], ((i + 1) * step_width + start_pixel, (i + 1) * step * direction + offset - 1)[::ax]), fill="black")
        draw.text(((i + 0.5) * step_width + start_pixel, (i + 0.5) * step * direction + offset)[::ax], str((i + 1) * step), fill="black", font=font, anchor=text_anchor)

def add_margin_indicators(draw, size, start, stop, step):
    for i, axis in enumerate(["x", "y"]):
        for direction in [-1, 1]:
            offset = 0 if direction == 1 else size[1 - i]
            text_anchor = ("m" if axis == "x" else ("l" if direction == 1 else "r")) + ("m" if axis == "y" else ("a" if direction == 1 else "d"))
            add_margin_indicator(draw, axis, direction, offset, text_anchor, 0, size[i]//2, start, stop, step)
            add_margin_indicator(draw, axis, direction, offset, text_anchor, size[i], size[i]//2, start, stop, step)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--geometry", help="geometry, eg. 800x600")
    parser.add_argument("-w", "--width", help="line base width in pixels", type=int)
    parser.add_argument("-c", "--comment", help="will be printed in image")
    parser.add_argument("-m", "--margin", help="cutting margin indicators. <start>,<stop>,<step> in pixels")
    parser.add_argument("-a", "--axis", help="add measurment axis", action="store_true")
    parser.add_argument("--checkerboard", help="add checkerboard", action="store_true")
    parser.add_argument("--test-lines-color", help="add color test lines", action="store_true")
    parser.add_argument("--test-lines-bw", help="add bw test lines", action="store_true")
    parser.add_argument("-b", "--background", help="set background color")
    parser.add_argument("--print-args", help="print args on image", action="store_true")
    parser.add_argument("file")
    args = parser.parse_args()

    size = tuple(map(int, args.geometry.split("x")))
    image = Image.new("RGB", size, color="white")
    draw = ImageDraw.Draw(image)
    if args.background:
        draw.rectangle((0,0,size[0], size[1]), fill=args.background)
    if args.axis:
        draw_measurment_axis(draw, size[1] // 2, size[0], True)
        draw_measurment_axis(draw, size[0] // 2, size[1], False)
    if args.test_lines_color:
        draw_test_lines(draw, (100, 1000), (300, -800), "black")
        draw_test_lines(draw, (500, 1000), (300, -800), "green")
        draw_test_lines(draw, (900, 1000), (300, -800), "red")
        draw_test_lines(draw, (1300, 1000), (300, -800), "blue")
    if args.test_lines_bw:
        # why this specific number? It a really precise integer 30 degree angle, perfect for hexagons
        # 30 - math.degrees(math.atan(780/1351)) == 6e-06
        base_offset = (400, 500)
        offset_per_line = (100,0)
        line = (780, 1351)
        options = ((1, 2), (1, 3), (2, 3), (3, 3), (3, 4), (3, 5), (3, 6), (3, 9), (4, 6), (4, 8))
        for i, option in enumerate(options):
            draw_bw_test_lines(draw, ap(base_offset, sp(i, offset_per_line)) , line, "white", option[0], "black", option[1])
            draw_bw_test_lines(draw, ap(base_offset, sp(i + 0.5, offset_per_line)), line, "black", option[0], "white", option[1])
    if args.checkerboard:
        checker_board(draw, (200, 1500, 600, 1900), 1)
        checker_board(draw, (200, 1900, 600, 2300), 8)
        checker_board(draw, (600, 1500, 1000, 1900), 2)
        checker_board(draw, (600, 1900, 1000, 2300), 4)
    if args.margin is not None:
        range_parm = [int(x) for x in args.margin.split(",")]
        add_margin_indicators(draw, size, range_parm[0], range_parm[1], range_parm[2])

    if args.comment is not None:
        draw.text((150, 100), text=args.comment, font=font, fill="black")

    if args.print_args:
        args_str = ""
        current_line = ""
        for key in vars(args):
            current_line += f"{key}={vars(args)[key]} "
            if draw.textsize(text=current_line, font=font)[0] > 1500:
                args_str += current_line + "\n"
                current_line = ""
        args_str += current_line

        draw.text((200, 200), text=args_str, font=font, fill="black")

    image.save(args.file)

    #image.show()
