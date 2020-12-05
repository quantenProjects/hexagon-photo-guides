#!/bin/env python3

import argparse

from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype("/usr/share/fonts/TTF/Verdana.TTF", 50)

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


def checker_board(draw, position, tile_size, color_a="white", color_b="black"):
    for x in range(position[0], position[2]):
        for y in range(position[1], position[3]):
            if (x // tile_size % 2 == 0) != (y // tile_size % 2 == 0):
                draw.point((x, y), fill=color_a)
            else:
                draw.point((x, y), fill=color_b)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--geometry", help="geometry, eg. 800x600")
    parser.add_argument("-w", "--width", help="line base width in pixels", type=int)
    parser.add_argument("-c", "--comment", help="will be printed in image")
    parser.add_argument("file")
    args = parser.parse_args()

    size = tuple(map(int, args.geometry.split("x")))
    image = Image.new("RGB", size, color="white")
    draw = ImageDraw.Draw(image)
    draw_measurment_axis(draw, size[1] // 2, size[0], True)
    draw_measurment_axis(draw, size[0] // 2, size[1], False)
    # draw_test_lines(draw, (10,10),(100,0),"black")
    draw_test_lines(draw, (100, 1000), (300, -800), "black")
    draw_test_lines(draw, (500, 1000), (300, -800), "green")
    draw_test_lines(draw, (900, 1000), (300, -800), "red")
    draw_test_lines(draw, (1300, 1000), (300, -800), "blue")
    checker_board(draw, (200, 1500, 600, 1900), 1)
    checker_board(draw, (200, 1900, 600, 2300), 8)
    checker_board(draw, (600, 1500, 1000, 1900), 2)
    checker_board(draw, (600, 1900, 1000, 2300), 4)

    long_text = "Falls diese Bilder noch ein Mensch sieht:\nJa, ich versuche gerade die genauen Schnittmaße\n" \
                "der Abzüge herauszufinden\n" \
                "Die Weboberfläche vom Fotoparadies\n" \
                "sagt da nichts genaues.\n" \
                "Über sachdienliche Hinweise aus dem Labor wäre ich\n" \
                "natürlich sehr froh:\n "
    draw.text((2100, 1500), text=long_text, font=font, fill="black")
    if args.comment is not None:
        draw.text((2100, 200), text=args.comment, font=font, fill="black")

    image.save(args.file)

    #image.show()
