#!/bin/env python3

import argparse
import math
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk

def offset_line(line, offset_x, offset_y):
    return [(x + offset_x, y + offset_y) for x, y in line]

def calc_hexagon_points(size, offset=0):
    width, height = size
    mid_x = (width / 2) + offset
    mid_y = height / 2
    r = mid_y / math.cos(math.radians(30))
    s = r * math.sin(math.radians(30))

    # TODO implement collision with border detection

    sides = []
    for direction in [-1, 1]:
        side = ((mid_x + direction * s, 0), (mid_x + direction * r, mid_y), (mid_x + direction * s, height))
        sides.append(side)

    return sides

def draw_guides(image, offset=0, cutting_edge=None):
    draw = ImageDraw.Draw(image)
    if cutting_edge is None:
        cutting_edge = (0,0,0,0)
    lines = calc_hexagon_points((image.size[0] - cutting_edge[1] - cutting_edge[3], image.size[1] - cutting_edge[0] - cutting_edge[2]), offset=offset)
    lines = map(lambda line: offset_line(line, cutting_edge[3], cutting_edge[0]), lines)
    for line in lines:
        draw.line(line, fill="white", width=3)
        draw.line(line, fill="black", width=2)


class GUI(tk.Frame):
    def __init__(self, image, width, callback, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.callback = callback
        self.width = width
        self.resize_factor = image.size[0] / width
        self.resized_image = image.resize((width, int(image.size[1] / self.resize_factor)))
        tk_image = ImageTk.PhotoImage(self.resized_image)
        self.image_view = tk.Label(self, image=tk_image)
        self.image_view.image = tk_image
        self.image_view.pack()
        self.draw_guides_and_callback(width // 2, self.image_view)
        self.master.bind("<Button-1>", lambda event: self.draw_guides_and_callback(event.x, self.image_view))
        self.master.bind("<B1-Motion>", lambda event: self.draw_guides_and_callback(event.x, self.image_view))

    def draw_guides_and_callback(self, x, image_view):
        drawn_image = self.resized_image.copy()
        draw_guides(drawn_image, offset=(x - self.width//2))
        tk_image = ImageTk.PhotoImage(drawn_image)
        image_view.configure(image=tk_image)
        image_view.image = tk_image
        self.callback((x - self.width // 2) * self.resize_factor)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Add hexagon guides to photo")
    parser.add_argument("filename", help="The input file")
    parser.add_argument("-r", "--force-resolution", help="Scale, crop, extend the image to this resolution. e.g 640x320")
    parser.add_argument("-c", "--cutting-edge", help="Cutting Edge in pixels. e.g. 5,23,4,1 (top, right, bottom, left)")
    parser.add_argument("-g", "--gui", help="display gui for offset adjustment and specify preview width, e.g. 1024 "
                        "Note: the GUI preview is not perfectly accurate, double check resulting image!", type=int)
    # TODO implement guide color and width parameter
    args = parser.parse_args()

    im = Image.open(args.filename)

    if args.force_resolution is not None:
        force_width, force_height = [int(x) for x in args.force_resolution.split("x")]
        im = im.resize((int(im.size[0] * force_height / im.size[1]), force_height))
        width_diff = abs(im.size[0] - force_width)
        if (im.size[0] / im.size[1]) > (force_width / force_height):
            print("input image is wider, cropping...")
            # input image is wider, cropping
            im = im.crop((width_diff // 2, 0, im.size[0] - width_diff // 2, im.size[1]))
        else:
            print("input image is taller, adding white")
            white_im = Image.new(im.mode, (force_width, force_height), "white")
            white_im.paste(im, box=(width_diff // 2, 0, im.size[0] + width_diff // 2, im.size[1]))
            im = white_im
            # TODO remember whitespace position for collision detection

    if args.cutting_edge is None:
        cutting_edge = (0,0,0,0)
    else:
        cutting_edge = [int(x) for x in args.cutting_edge.split(",")]
        assert len(cutting_edge) == 4

    offset = 0

    def offset_callback(set_offset):
        global offset
        offset = int(set_offset)

    if args.gui is not None:
        root = tk.Tk()
        app = GUI(im.crop((cutting_edge[3], cutting_edge[0], im.size[0] - cutting_edge[1], im.size[1] - cutting_edge[2])), args.gui, offset_callback, master=root)
        app.mainloop()

    print(f"using offset {offset}")


    draw_guides(im, cutting_edge=cutting_edge, offset=offset)

    #im.show()
    im.save(args.filename + "_guides.png")



