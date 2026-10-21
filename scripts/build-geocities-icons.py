#!/usr/bin/env python3
"""Draw original 48 × 48 pixel icons and export them as real SVG paths.

Run with Python + Pillow. No external artwork, fonts, or raster images are
embedded in the SVGs. The drawing coordinates below are the editable source.
"""

from collections import defaultdict
from html import escape
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "geocities"
SIZE = 48
# Preserve the original tile dimensions and icon centers so the existing dog
# and pizza photo backgrounds replace icons in the same positions on repeat.
TILE_SIZE = (715, 1089)
TILE_CENTERS = [
    (94.5, 74.5), (330, 78), (568, 78),
    (94, 298), (330, 294), (568.5, 293.5),
    (95, 513.5), (330, 516), (568.5, 514.5),
    (94.5, 728), (330, 728), (568.5, 728.5),
    (94.5, 946), (330, 946), (568.5, 946),
]

COLORS = {
    "ink": "#241b3c", "white": "#fff9e8", "silver": "#c7d4e3",
    "steel": "#7d8ca9", "slate": "#4d587d", "purple": "#7046d9",
    "lavender": "#b293ff", "cyan": "#42e8ed", "teal": "#168e9b",
    "red": "#ef3658", "darkred": "#a51b48", "pink": "#ff8bb7",
    "rose": "#d94a87", "yellow": "#ffe94a", "gold": "#ffbd43",
    "orange": "#e68236", "brown": "#985036", "darkbrown": "#61313e",
    "cream": "#ffe3a0", "green": "#36b970", "lime": "#9ce66c",
    "forest": "#23735f",
}


def color(name):
    return COLORS.get(name, name)


class PixelIcon:
    def __init__(self):
        self.image = Image.new("RGBA", (SIZE, SIZE))
        self.draw = ImageDraw.Draw(self.image)

    def rect(self, box, fill):
        self.draw.rectangle(box, fill=color(fill))

    def poly(self, points, fill, outline=None, width=1):
        self.draw.polygon(points, fill=color(fill), outline=color(outline), width=width)

    def line(self, points, fill, width=1):
        self.draw.line(points, fill=color(fill), width=width)

    def ellipse(self, box, fill, outline=None, width=1):
        self.draw.ellipse(box, fill=color(fill), outline=color(outline), width=width)

    def dot(self, x, y, fill):
        self.rect((x, y, x, y), fill)

    def outline(self):
        edge = Image.new("RGBA", self.image.size, COLORS["ink"])
        edge.putalpha(self.image.getchannel("A").filter(ImageFilter.MaxFilter(3)))
        edge.alpha_composite(self.image)
        self.image = edge
        self.draw = ImageDraw.Draw(self.image)

    def sparkle(self, x, y):
        self.line([(x, y-3), (x, y+3)], "teal", 1)
        self.line([(x-3, y), (x+3, y)], "teal", 1)
        self.rect((x-1, y-1, x+1, y+1), "cyan")
        self.dot(x, y, "white")

    def metal_joint(self, x, y, radius=4):
        self.ellipse((x-radius, y-radius, x+radius, y+radius), "ink")
        self.ellipse((x-radius+1, y-radius+1, x+radius-1, y+radius-1), "steel")
        self.ellipse((x-2, y-2, x+1, y+1), "cyan")
        self.dot(x-1, y-1, "white")

    def svg_paths(self):
        """Merge horizontal pixel runs by color into compact vector paths."""
        paths = defaultdict(list)
        for y in range(SIZE):
            x = 0
            while x < SIZE:
                rgba = self.image.getpixel((x, y))
                end = x + 1
                while end < SIZE and self.image.getpixel((end, y)) == rgba:
                    end += 1
                if rgba[3]:
                    fill = "#%02x%02x%02x" % rgba[:3]
                    paths[fill].append(f"M{x} {y}h{end-x}v1H{x}z")
                x = end
        return "\n".join(f'<path fill="{fill}" d="{"".join(runs)}"/>'
                         for fill, runs in paths.items())


def bicycle():
    a = PixelIcon()
    for cx in (11, 37):
        a.ellipse((cx-9, 25, cx+9, 43), "ink")
        a.ellipse((cx-7, 27, cx+7, 41), "steel")
        a.ellipse((cx-5, 29, cx+5, 39), (0, 0, 0, 0))
        a.line([(cx-5, 34), (cx+5, 34)], "silver")
        a.line([(cx, 29), (cx, 39)], "silver")
        a.line([(cx-5, 28), (cx-2, 27), (cx+2, 27)], "white")
    frame = [(11, 34), (19, 21), (32, 21), (27, 34), (11, 34), (19, 21), (27, 34)]
    a.line(frame, "ink", 4)
    a.line(frame, "red", 2)
    a.line([(20, 20), (31, 20)], "pink")
    a.line([(17, 15), (19, 21)], "ink", 3)
    a.line([(17, 16), (19, 20)], "silver")
    a.rect((13, 13, 23, 15), "ink")
    a.rect((14, 13, 20, 13), "purple")
    a.line([(37, 34), (31, 14), (35, 12), (39, 12), (39, 16)], "ink", 3)
    a.line([(37, 33), (32, 16)], "cyan")
    a.line([(32, 13), (37, 13)], "silver")
    a.ellipse((25, 32, 29, 36), "ink")
    a.dot(26, 33, "white")
    a.line([(27, 34), (29, 38), (32, 38)], "ink", 2)
    a.rect((30, 38, 34, 39), "purple")
    return a


def robot():
    a = PixelIcon()
    a.rect((22, 7, 24, 13), "ink")
    a.ellipse((20, 3, 26, 9), "ink")
    a.rect((22, 4, 24, 6), "red")
    a.dot(22, 4, "pink")
    a.rect((5, 21, 10, 30), "ink")
    a.rect((6, 22, 8, 28), "teal")
    a.rect((6, 22, 7, 24), "cyan")
    a.rect((37, 21, 42, 30), "ink")
    a.rect((39, 22, 41, 28), "teal")
    a.poly([(12, 12), (35, 12), (38, 15), (38, 36), (35, 39), (12, 39), (9, 36), (9, 15)], "ink")
    a.poly([(12, 14), (34, 14), (36, 16), (36, 35), (34, 37), (13, 37), (11, 35), (11, 16)], "silver")
    a.line([(12, 32), (12, 16), (34, 16)], "white")
    a.poly([(34, 17), (36, 17), (36, 35), (34, 37), (13, 37), (13, 35), (33, 35), (34, 34)], "steel")
    for x in (14, 27):
        a.rect((x, 20, x+6, 25), "ink")
        a.rect((x+1, 21, x+4, 23), "cyan")
        a.dot(x+1, 21, "white")
    a.rect((14, 29, 33, 34), "ink")
    for x in (16, 21, 26, 31):
        a.rect((x, 30, x+1, 32), "white")
    a.rect((12, 26, 15, 27), "pink")
    a.rect((32, 26, 35, 27), "pink")
    a.sparkle(41, 9)
    return a


def floppy_disk():
    a = PixelIcon()
    a.poly([(8, 4), (35, 4), (41, 10), (41, 43), (7, 43), (7, 5)], "ink")
    a.poly([(9, 6), (34, 6), (39, 11), (39, 41), (9, 41)], "purple")
    a.line([(10, 39), (10, 7), (33, 7)], "lavender")
    a.line([(38, 12), (38, 40), (10, 40)], "slate")
    a.rect((14, 5, 33, 21), "ink")
    a.rect((15, 6, 32, 19), "silver")
    a.rect((15, 6, 31, 7), "white")
    a.rect((16, 18, 31, 19), "steel")
    a.rect((26, 8, 30, 17), "ink")
    a.rect((27, 9, 29, 17), "slate")
    a.rect((12, 25, 36, 41), "ink")
    a.rect((13, 26, 35, 40), "white")
    a.rect((13, 26, 35, 29), "red")
    a.rect((14, 26, 34, 26), "pink")
    a.rect((16, 32, 31, 32), "teal")
    a.rect((16, 35, 28, 35), "steel")
    a.rect((16, 38, 23, 38), "steel")
    a.dot(10, 38, "white")
    a.dot(38, 38, "white")
    return a


def robotic_arm():
    a = PixelIcon()
    a.poly([(28, 15), (26, 9), (28, 4), (32, 3), (32, 6), (30, 8), (30, 12), (34, 13), (38, 10), (38, 6), (41, 6), (42, 12), (37, 17)], "ink")
    a.line([(29, 12), (28, 9), (30, 5)], "silver", 2)
    a.line([(36, 14), (40, 11), (40, 7)], "silver", 2)
    a.poly([(29, 13), (37, 16), (30, 36), (25, 40), (9, 40), (9, 30), (23, 30)], "ink")
    a.poly([(30, 16), (34, 17), (28, 34), (23, 36), (11, 36), (11, 32), (25, 32)], "silver")
    a.line([(30, 17), (26, 30)], "white", 2)
    a.line([(33, 19), (29, 32)], "steel", 2)
    a.rect((12, 33, 22, 34), "white")
    a.rect((11, 37, 24, 38), "steel")
    a.line([(34, 20), (33, 28), (28, 36), (20, 37)], "red")
    a.metal_joint(25, 34, 5)
    a.rect((5, 28, 12, 42), "ink")
    a.rect((7, 30, 10, 40), "purple")
    a.rect((7, 30, 8, 38), "lavender")
    a.dot(9, 40, "cyan")
    return a


def bread():
    a = PixelIcon()
    a.poly([(4, 26), (6, 20), (12, 14), (19, 11), (29, 11), (37, 15), (42, 21), (44, 28), (42, 35), (37, 38), (11, 38), (5, 34)], "ink")
    a.poly([(6, 26), (8, 21), (13, 16), (20, 13), (29, 13), (36, 17), (40, 22), (42, 29), (40, 34), (36, 36), (12, 36), (7, 32)], "orange")
    a.poly([(7, 25), (13, 18), (21, 14), (29, 14), (36, 19), (39, 25), (36, 30), (29, 33), (13, 32), (8, 29)], "gold")
    a.line([(8, 25), (10, 22), (15, 18), (21, 16)], "cream", 2)
    a.poly([(8, 32), (13, 35), (33, 35), (39, 32), (41, 28), (40, 34), (36, 36), (12, 36)], "brown")
    for x, y in ((17, 18), (26, 17), (34, 20)):
        a.line([(x, y), (x-4, y+7)], "brown", 3)
        a.line([(x, y), (x-3, y+5)], "cream", 2)
    for x, y in ((10, 29), (14, 31), (19, 32), (24, 33), (30, 32), (36, 29), (39, 27)):
        a.dot(x, y, "orange")
    a.dot(17, 28, "cream")
    a.dot(28, 27, "cream")
    return a


def brain():
    a = PixelIcon()
    a.poly([(24, 31), (32, 31), (32, 37), (29, 37), (29, 42), (23, 42), (23, 36)], "ink")
    a.poly([(25, 33), (30, 33), (30, 35), (27, 37), (27, 40), (25, 40)], "rose")
    outline = [(7, 30), (5, 26), (5, 21), (8, 18), (8, 13), (12, 10), (16, 10), (19, 6), (24, 6), (27, 8), (31, 7), (35, 10), (35, 13), (39, 14), (42, 18), (42, 23), (40, 26), (41, 30), (37, 34), (30, 34), (26, 36), (19, 34), (13, 35), (9, 33)]
    a.poly(outline, "pink", "ink", 2)
    a.poly([(37, 17), (40, 19), (40, 23), (38, 26), (39, 30), (36, 32), (29, 32), (25, 34), (20, 32), (14, 33), (10, 30), (17, 30), (23, 31), (30, 29), (34, 25)], "rose")
    a.line([(10, 19), (10, 15), (13, 12), (17, 12), (20, 9), (23, 9)], "white", 2)
    a.line([(29, 10), (32, 10), (33, 13)], "white")
    folds = [([(23, 10), (21, 15), (24, 18), (23, 23), (25, 27), (24, 32)], "darkred"),
             ([(15, 15), (17, 18), (16, 23), (11, 23), (10, 27), (13, 30)], "rose"),
             ([(18, 26), (19, 29), (17, 32)], "darkred"),
             ([(30, 14), (28, 17), (29, 21), (34, 22), (36, 19)], "rose"),
             ([(29, 25), (31, 27), (31, 30)], "darkred")]
    for points, fill in folds:
        a.line(points, fill, 2)
    return a


def dog_face():
    a = PixelIcon()
    a.poly([(11, 13), (15, 8), (32, 8), (36, 13), (37, 28), (33, 35), (29, 38), (18, 38), (12, 33), (10, 25)], "gold", "ink", 2)
    a.poly([(14, 14), (18, 10), (29, 10), (33, 14), (31, 28), (17, 29)], "cream")
    a.poly([(11, 11), (7, 14), (4, 23), (6, 32), (9, 35), (13, 33), (15, 15)], "brown", "ink", 2)
    a.poly([(36, 11), (40, 14), (43, 23), (41, 32), (38, 35), (34, 33), (32, 15)], "brown", "ink", 2)
    a.line([(10, 15), (7, 23), (8, 29)], "gold", 2)
    a.line([(37, 15), (40, 23), (39, 29)], "orange", 2)
    for x in (17, 28):
        a.rect((x, 19, x+3, 23), "ink")
        a.dot(x, 19, "white")
    a.poly([(18, 25), (29, 25), (32, 29), (30, 34), (27, 36), (20, 36), (15, 32), (15, 29)], "white")
    a.poly([(20, 27), (27, 27), (27, 30), (24, 32), (20, 30)], "ink")
    a.rect((22, 27, 24, 27), "steel")
    a.poly([(20, 33), (27, 33), (28, 36), (27, 41), (23, 43), (20, 40)], "ink")
    a.poly([(22, 35), (26, 35), (26, 40), (23, 41), (22, 39)], "pink")
    a.line([(24, 35), (24, 38)], "rose")
    a.dot(18, 31, "brown")
    a.dot(29, 31, "brown")
    return a


def lemon():
    a = PixelIcon()
    a.poly([(30, 10), (33, 5), (41, 4), (39, 10), (34, 13)], "green", "ink", 1)
    a.line([(34, 10), (38, 7)], "lime")
    a.poly([(8, 29), (11, 21), (20, 13), (29, 10), (33, 10), (36, 8), (39, 10), (40, 13), (38, 17), (38, 24), (34, 32), (26, 38), (18, 40), (13, 38), (9, 41), (6, 37), (9, 33)], "yellow", "ink", 2)
    a.poly([(35, 15), (37, 14), (36, 24), (32, 31), (25, 36), (18, 38), (12, 36), (18, 35), (26, 31), (31, 25)], "gold")
    a.line([(12, 27), (15, 22), (21, 17), (27, 15)], "white", 2)
    a.dot(11, 30, "white")
    for x, y in ((20, 30), (24, 27), (28, 25), (29, 31), (19, 35), (33, 22)):
        a.dot(x, y, "orange")
    return a


def evergreen():
    a = PixelIcon()
    a.rect((20, 33, 27, 44), "ink")
    a.rect((22, 35, 25, 42), "brown")
    a.rect((22, 37, 23, 41), "gold")
    a.poly([(24, 3), (34, 16), (30, 16), (39, 27), (34, 27), (44, 38), (4, 38), (14, 27), (9, 27), (18, 16), (14, 16)], "green", "ink", 2)
    a.poly([(24, 6), (25, 15), (31, 15), (26, 11)], "forest")
    a.poly([(25, 16), (27, 23), (35, 25), (24, 25), (17, 22)], "forest")
    a.poly([(27, 27), (34, 34), (39, 36), (11, 36), (15, 33), (25, 33)], "forest")
    a.line([(23, 8), (19, 14), (23, 14)], "lime", 2)
    a.line([(19, 19), (15, 24), (21, 24)], "lime", 2)
    a.line([(15, 29), (10, 34), (15, 34)], "lime", 2)
    for x, y in ((22, 20), (26, 29), (31, 32), (17, 35)):
        a.dot(x, y, "lime")
    return a


def pizza():
    a = PixelIcon()
    a.poly([(6, 13), (40, 13), (26, 44), (23, 44)], "ink")
    a.poly([(9, 15), (37, 15), (25, 41)], "yellow")
    a.poly([(34, 17), (37, 15), (25, 41), (24, 36)], "orange")
    a.poly([(5, 11), (8, 7), (16, 5), (29, 5), (38, 8), (42, 12), (39, 17), (32, 14), (14, 13), (8, 16)], "ink")
    a.poly([(7, 11), (10, 9), (17, 7), (29, 7), (37, 10), (40, 12), (38, 14), (32, 12), (14, 11), (8, 13)], "gold")
    a.line([(10, 10), (17, 8), (28, 8), (35, 10)], "cream")
    a.line([(14, 13), (30, 13), (37, 16)], "brown")
    for x, y, r in ((16, 20, 3), (30, 20, 3), (24, 30, 3)):
        a.ellipse((x-r, y-r, x+r, y+r), "darkred")
        a.ellipse((x-r+1, y-r+1, x+r-1, y+r-1), "red")
        a.dot(x-1, y-1, "pink")
    a.line([(21, 17), (23, 18), (23, 20)], "forest", 2)
    a.line([(29, 26), (31, 25)], "forest", 2)
    a.dot(20, 26, "white")
    a.dot(25, 37, "white")
    return a


def mountains():
    a = PixelIcon()
    a.poly([(18, 40), (31, 9), (35, 14), (46, 40)], "ink")
    a.poly([(21, 38), (31, 12), (34, 16), (43, 38)], "purple")
    a.poly([(31, 12), (31, 26), (25, 38), (21, 38)], "lavender")
    a.poly([(31, 12), (36, 22), (32, 20), (29, 23), (28, 20)], "white")
    a.poly([(2, 40), (16, 7), (20, 8), (37, 40)], "ink")
    a.poly([(5, 38), (17, 10), (19, 11), (34, 38)], "steel")
    a.poly([(17, 11), (18, 25), (14, 29), (17, 38), (5, 38)], "silver")
    a.poly([(19, 13), (34, 38), (23, 38), (22, 31), (19, 28), (21, 24)], "slate")
    a.poly([(17, 10), (19, 11), (25, 22), (20, 20), (17, 23), (15, 20), (12, 22)], "white")
    a.poly([(19, 12), (25, 22), (20, 20), (18, 17)], "cyan")
    a.rect((3, 40, 45, 42), "ink")
    a.rect((5, 40, 43, 41), "forest")
    a.rect((10, 40, 20, 40), "green")
    return a


def dog():
    a = PixelIcon()
    a.line([(33, 24), (39, 21), (43, 16), (42, 11), (38, 9)], "ink", 5)
    a.line([(33, 23), (39, 20), (41, 16), (40, 12), (38, 11)], "gold", 3)
    a.dot(40, 14, "cream")
    a.poly([(19, 26), (25, 27), (22, 38), (25, 39), (25, 42), (18, 42)], "brown", "ink", 1)
    a.poly([(29, 26), (35, 26), (33, 36), (35, 38), (35, 40), (28, 40)], "brown", "ink", 1)
    a.poly([(5, 16), (9, 16), (10, 11), (17, 11), (21, 18), (31, 18), (36, 23), (35, 29), (35, 37), (39, 39), (39, 42), (31, 42), (29, 31), (22, 31), (18, 38), (18, 42), (10, 42), (10, 39), (13, 36), (14, 26), (8, 26), (5, 23)], "gold", "ink", 2)
    a.poly([(19, 20), (29, 20), (33, 22), (30, 24), (20, 24)], "cream")
    a.poly([(17, 26), (21, 28), (29, 28), (31, 26), (33, 30), (33, 38), (36, 39), (33, 40), (30, 30), (20, 30), (16, 37), (14, 39)], "orange")
    a.poly([(14, 13), (17, 13), (20, 19), (18, 26), (15, 25), (13, 20)], "brown", "ink")
    a.line([(15, 14), (17, 18), (16, 22)], "orange")
    a.rect((4, 17, 7, 20), "ink")
    a.dot(11, 16, "ink")
    a.dot(10, 15, "white")
    a.line([(14, 26), (18, 28)], "teal", 3)
    a.line([(15, 26), (18, 27)], "cyan")
    a.dot(18, 29, "yellow")
    a.rect((11, 40, 15, 40), "cream")
    a.rect((33, 40, 36, 40), "cream")
    return a


def treble_clef():
    a = PixelIcon()
    curve = [(19, 39), (20, 42), (25, 43), (29, 41), (30, 37),
             (24, 10), (23, 6), (25, 3), (28, 3), (30, 6), (30, 10),
             (28, 14), (22, 19), (16, 24), (14, 28), (14, 32),
             (17, 36), (22, 38), (28, 38), (33, 35), (35, 31),
             (34, 27), (31, 24), (27, 24), (24, 26), (23, 29), (25, 32), (28, 32)]
    a.line(curve, "gold", 3)
    a.line([(25, 5), (27, 4), (29, 7), (29, 10), (27, 13), (22, 17), (16, 23)], "white")
    a.line([(16, 26), (15, 29), (16, 32), (19, 35), (23, 36)], "yellow")
    a.line([(28, 25), (31, 25), (33, 28)], "white")
    a.ellipse((17, 37, 21, 41), "ink")
    a.rect((18, 38, 20, 39), "gold")
    a.outline()
    a.sparkle(9, 11)
    a.sparkle(39, 40)
    return a


def chili_pepper():
    a = PixelIcon()
    a.poly([(33, 14), (34, 10), (32, 7), (28, 6), (29, 3), (35, 4), (39, 9), (38, 15)], "forest", "ink", 1)
    a.line([(30, 4), (34, 5), (37, 9), (36, 12)], "lime")
    a.poly([(31, 13), (36, 12), (41, 15), (43, 20), (42, 27), (37, 34), (31, 38), (23, 40), (15, 39), (9, 36), (4, 30), (12, 32), (20, 32), (26, 29), (30, 24), (32, 18)], "red", "ink", 2)
    a.poly([(39, 18), (41, 21), (40, 27), (35, 33), (30, 36), (23, 38), (15, 37), (10, 34), (19, 35), (26, 33), (33, 28), (37, 23)], "darkred")
    a.line([(35, 19), (35, 23), (31, 29), (26, 32), (21, 34)], "pink", 2)
    a.line([(35, 18), (35, 21)], "white")
    a.poly([(31, 14), (35, 12), (39, 14), (40, 18), (36, 16), (33, 18)], "green", "ink", 1)
    a.line([(34, 14), (37, 14)], "lime")
    a.dot(16, 34, "pink")
    return a


def robotic_leg():
    a = PixelIcon()
    a.poly([(24, 5), (32, 5), (37, 9), (37, 14), (27, 25), (19, 22), (19, 17)], "ink")
    a.poly([(25, 7), (31, 7), (35, 10), (35, 13), (26, 22), (21, 20), (21, 17)], "silver")
    a.line([(22, 18), (26, 9), (31, 9)], "white", 2)
    a.poly([(33, 12), (35, 12), (26, 22), (23, 21)], "steel")
    a.line([(32, 15), (28, 19)], "purple", 2)
    a.poly([(19, 23), (27, 26), (22, 37), (24, 40), (14, 40), (14, 35)], "ink")
    a.poly([(20, 26), (24, 27), (20, 36), (20, 38), (16, 38), (16, 35)], "silver")
    a.line([(20, 27), (17, 35)], "white")
    a.line([(23, 28), (20, 35)], "teal")
    a.metal_joint(23, 24, 5)
    a.poly([(15, 36), (21, 37), (23, 39), (28, 40), (30, 44), (10, 44), (10, 41)], "ink")
    a.poly([(16, 38), (20, 39), (23, 41), (27, 41), (28, 42), (12, 42)], "purple")
    a.line([(15, 40), (20, 40)], "lavender")
    a.line([(12, 43), (27, 43)], "steel")
    a.sparkle(10, 10)
    return a


ICONS = [
    ("bicycle", "Bicycle", bicycle),
    ("robot", "Robot", robot),
    ("floppy-disk", "Floppy disk", floppy_disk),
    ("robotic-arm", "Robotic arm", robotic_arm),
    ("bread", "Bread", bread),
    ("brain", "Brain", brain),
    ("dog-face", "Dog face", dog_face),
    ("lemon", "Lemon", lemon),
    ("evergreen", "Evergreen tree", evergreen),
    ("pizza", "Pizza", pizza),
    ("mountains", "Mountains", mountains),
    ("dog", "Dog", dog),
    ("treble-clef", "Treble clef", treble_clef),
    ("chili-pepper", "Chili pepper", chili_pepper),
    ("robotic-leg", "Robotic leg", robotic_leg),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    definitions = []
    uses = []
    for index, (slug, title, draw) in enumerate(ICONS):
        icon = draw()
        paths = icon.svg_paths()
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" '
               f'viewBox="0 0 48 48" shape-rendering="crispEdges" role="img" aria-labelledby="title">\n'
               f'<title id="title">{escape(title)} — GeoCities pixel icon</title>\n'
               f'{paths}\n</svg>\n')
        (OUT / f"{slug}.svg").write_text(svg)
        definitions.append(f'<g id="{slug}">\n{paths}\n</g>')
        left, top, right, bottom = icon.image.getbbox()
        center_x, center_y = TILE_CENTERS[index]
        x = round(center_x - (left + right) / 2)
        y = round(center_y - (top + bottom) / 2)
        uses.append(f'<use href="#{slug}" x="{x}" y="{y}"/>')
    tile_width, tile_height = TILE_SIZE
    tile = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{tile_width}" height="{tile_height}" '
            f'viewBox="0 0 {tile_width} {tile_height}" shape-rendering="crispEdges" role="img" aria-labelledby="title">\n'
            '<title id="title">GeoCities icon background</title>\n<defs>\n'
            + '\n'.join(definitions) + '\n</defs>\n<g>\n'
            + '\n'.join(uses) + '\n</g>\n</svg>\n')
    (OUT / "background.svg").write_text(tile)
    print(f"Wrote {len(ICONS)} icons and a repeating background tile to {OUT}")


if __name__ == "__main__":
    main()
