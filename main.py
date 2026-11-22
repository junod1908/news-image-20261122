# news-image-20261122 — "Sum up 22 November's world news in one image."
#
# The entry is a one-page pictorial broadsheet, "The World in One Day",
# for Sunday 22 November 2026. This program draws the whole page itself
# with the Python 3.13 standard library only: no network, no clock, no
# randomness, so two runs write byte-identical files.
#
# What it draws, top to bottom:
#   * masthead naming the day: THE WORLD IN ONE DAY / SUNDAY, 22 NOV 2026
#   * three painted hero panels (Las Vegas GP, COP31 Antalya, Ashes Perth)
#     with caption bars, composited from assets/panel_*.rgbz
#   * a dense dot world map with red markers at the stories' places
#   * 19 numbered story cards in two columns — every story date-audited
#     to Sunday 22 November 2026 (see the audit notes in the repo)
#
# The painted panels are generated illustrations shipped as assets; every
# word on the page is set in type by this program from the bitmap fonts in
# assets/font.bin (DejaVu glyphs, rendered at build time).
#
# Run it locally with:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import binascii
import os
import struct
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

W = 1024
H = 1024

# ---------------------------------------------------------------- palette
PAPER = (246, 241, 230)
INK = (26, 26, 26)
DETAIL = (51, 48, 42)
NAVY = (23, 38, 63)
MAPDOT = (51, 80, 126)
GOLD = (217, 164, 65)
RED = (180, 35, 24)
MUTED = (107, 101, 88)
HAIRLINE = (220, 213, 195)
WHITE = (255, 255, 255)

# ---------------------------------------------------------------- copy
TITLE = "THE WORLD IN ONE DAY"
DATE = "SUNDAY, 22 NOVEMBER 2026"
SECTION = "THE DAY IN 19 STORIES"
FOOTER = ("All 19 stories happened, or were first reported, "
          "on Sunday 22 November 2026  -  news-image-20261122")

CAPTIONS = [
    ("panel_f1.rgbz", "LAS VEGAS - VERSTAPPEN WINS"),
    ("panel_cop31.rgbz", "ANTALYA - COP31 COLLAPSES, NO DEAL"),
    ("panel_ashes.rgbz", "PERTH - HEAD'S 123 SEALS 2-DAY WIN"),
]

# (headline, detail) — all 19 stories happened, or were first reported,
# on Sunday 22 November 2026. Item 5 is an agenda item (tonight's show),
# item 6 is framed as the collapse it was: no deal was reached.
ITEMS = [
    ("VERSTAPPEN WINS LAS VEGAS GP",
     "50 laps, 35 lead changes; Norris 2nd, Piastri 3rd"),
    ("CHIEFS BEAT COLTS 23-20 IN OT",
     "Mahomes comeback; Butker 27-yd field goal wins it"),
    ("SANDERS WINS FIRST NFL START",
     "Browns 24-10 Raiders; 10 sacks on Geno Smith"),
    ("COWBOYS RALLY PAST EAGLES 24-21",
     "Eagles blow a 21-0 lead in Dallas"),
    ("MISS UNIVERSE PRELIMINARY TONIGHT",
     "Preliminary show in San Juan, 7 PM; Top 30 decided"),
    ("COP31 COLLAPSES - NO DEAL",
     "Final draft with no 'fossil fuels' rejected"),
    ("RUSSIAN DRONE HITS FLATS IN DYMER",
     "14 missing, 2 dead; 186 drones launched overnight"),
    ("FLOODS HIT CORNWALL AND DEVON",
     "Up to 100 mm rain on Dartmoor; roads closed"),
    ("4 KILLED IN GAZA DESPITE CEASEFIRE",
     "Beit Lahia, Khan Younis, al-Mawasi"),
    ("EISENKOT OPENS TALKS WITH LIKUD",
     "Coalition talks begin in Herzliya, 1 PM"),
    ("SUDAN CONDEMNS RSF EXECUTIONS",
     "Captured soldiers killed in Blue Nile"),
    ("INDIA 720/9 - RECORD TOTAL IN NZ",
     "Pant 128; New Zealand 119/2 at stumps, Day 4"),
    ("FIVE CHAMPIONS AT HONG KONG OPEN",
     "Antonsen walkover; Wang Zhiyi; Malaysia sweep doubles"),
    ("CHAHAL JOINS BJP",
     "Cricketer joins the OBC Morcha committee"),
    ("CHENNAI BOOK FAIR 2027 ANNOUNCED",
     "Dates set for 16-18 January 2027"),
    ("POLIO DRIVE ACROSS INDIA",
     "Millions of under-5s vaccinated in 10+ states"),
    ("AUSTRALIA WIN ASHES TEST IN 2 DAYS",
     "Head 123 off 83 balls; Starc takes 10 wickets"),
    ("BITCOIN HOLDS ABOVE $60,000",
     "$60,324 on Sunday; stays above the mark"),
    ("SPACEX LAUNCHES NROL-136",
     "Falcon 9, 12:23 UTC; booster lands at LZ-4"),
]

# ---------------------------------------------------------------- dot map
# Coarse continent outlines as (lon, lat) polygons, equirectangular.
# Good enough for a dot map at 8 px spacing; the red markers below are
# what ties the map to the day's stories.
NORTH_AMERICA = [
    (-168, 66), (-164, 60), (-160, 58), (-155, 56), (-150, 59),
    (-145, 60), (-140, 60), (-135, 58), (-130, 54),
    (-125, 49), (-124, 41), (-120, 34), (-114, 29), (-107, 24),
    (-101, 19), (-95, 16), (-90, 14), (-84, 11), (-80, 8),
    (-76, 9), (-71, 12), (-64, 11), (-59, 8), (-54, 5),
    (-52, 4), (-55, 7), (-59, 10), (-61, 14), (-65, 17),
    (-68, 18), (-71, 19), (-74, 20), (-78, 21), (-81, 24),
    (-81, 27), (-80, 31), (-78, 34), (-76, 36), (-74, 39),
    (-71, 41), (-69, 43), (-66, 44), (-63, 45), (-60, 46),
    (-57, 47), (-55, 49), (-58, 51), (-60, 52), (-64, 54),
    (-68, 55), (-72, 54), (-76, 53), (-79, 52), (-82, 53),
    (-85, 55), (-86, 58), (-88, 60), (-90, 63), (-93, 66),
    (-98, 68), (-104, 68), (-110, 68), (-116, 69), (-122, 70),
    (-128, 70), (-134, 69), (-140, 70), (-147, 70), (-154, 71),
    (-161, 70), (-166, 68),
]
GREENLAND = [
    (-45, 60), (-40, 63), (-32, 68), (-25, 70), (-30, 74),
    (-40, 76), (-52, 76), (-58, 74), (-58, 70), (-53, 65), (-48, 61),
]
SOUTH_AMERICA = [
    (-80, 9), (-76, 7), (-72, 11), (-66, 11), (-61, 9),
    (-56, 6), (-51, 4), (-50, 0), (-44, -3), (-38, -5),
    (-35, -8), (-37, -13), (-39, -17), (-41, -22), (-46, -24),
    (-49, -28), (-53, -33), (-58, -38), (-62, -41), (-65, -45),
    (-67, -50), (-69, -52), (-71, -54), (-74, -52), (-74, -47),
    (-73, -42), (-73, -37), (-72, -30), (-71, -22), (-70, -18),
    (-74, -15), (-78, -10), (-80, -5), (-81, -1), (-80, 4),
]
AFRICA = [
    (-17, 15), (-16, 20), (-14, 25), (-10, 30), (-6, 33),
    (-2, 35), (3, 37), (9, 37), (11, 34), (15, 32),
    (20, 32), (25, 31), (30, 31), (33, 28), (35, 24),
    (37, 20), (39, 16), (41, 12), (44, 11), (48, 11),
    (51, 12), (50, 8), (46, 4), (43, 0), (41, -3),
    (40, -8), (38, -13), (36, -18), (34, -22), (33, -26),
    (30, -30), (27, -33), (22, -34), (19, -35), (16, -33),
    (14, -29), (13, -24), (12, -18), (12, -13), (9, -8),
    (9, -3), (9, 1), (8, 4), (4, 6), (-2, 5),
    (-7, 5), (-12, 8), (-15, 11),
]
EURASIA = [
    (-10, 37), (-9, 43), (-2, 48), (0, 51), (4, 53),
    (8, 57), (10, 59), (18, 56), (21, 55), (24, 58),
    (28, 60), (30, 62), (32, 66), (36, 67), (44, 68),
    (54, 69), (68, 72), (78, 73), (90, 75), (104, 76),
    (115, 74), (128, 72), (142, 72), (155, 70), (170, 67),
    (178, 65), (170, 60), (162, 56), (158, 52), (156, 50),
    (150, 47), (142, 42), (135, 35), (130, 33), (127, 35),
    (126, 38), (122, 39), (120, 35), (121, 31), (118, 25),
    (113, 22), (109, 18), (106, 10), (104, 9), (101, 8),
    (100, 6), (98, 10), (95, 15), (92, 21), (89, 22),
    (86, 20), (82, 16), (80, 13), (77, 8), (75, 11),
    (73, 17), (71, 20), (68, 23), (66, 25), (62, 25),
    (58, 26), (48, 29), (43, 28), (36, 36), (30, 36),
    (27, 37), (23, 36), (19, 40), (15, 44), (12, 44),
    (8, 44), (3, 42), (0, 38), (-6, 36),
]
ARABIA = [
    (43, 12), (40, 16), (38, 20), (39, 25), (42, 28),
    (46, 29), (48, 29), (50, 26), (52, 25), (55, 24),
    (57, 25), (59, 22), (58, 19), (55, 17), (51, 15),
    (47, 13), (44, 12),
]
UK = [(-5, 50), (-3, 53), (-5, 56), (-4, 58), (-2, 57), (0, 53), (1, 51), (-1, 50)]
SUMATRA = [(95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (103, -5), (100, -2), (97, 1)]
BORNEO = [(109, 1), (111, 3), (114, 5), (117, 6), (119, 3), (118, 0), (116, -3), (113, -4), (110, -3)]
JAVA = [(105, -6), (108, -7), (111, -7), (114, -8), (113, -9), (109, -8), (106, -7)]
SULAWESI = [(119, 0), (121, 1), (123, 0), (121, -2), (120, -4), (119, -2)]
NEW_GUINEA = [
    (131, -1), (134, -2), (137, -3), (141, -4), (145, -6),
    (148, -8), (150, -9), (147, -9), (143, -8), (139, -7),
    (135, -5), (132, -3),
]
PHILIPPINES = [
    (120, 18), (121, 17), (122, 15), (121, 13), (122, 11),
    (123, 10), (121, 11), (120, 13), (120, 16),
]
JAPAN = [
    (130, 31), (132, 33), (134, 34), (136, 35), (138, 35),
    (140, 36), (141, 38), (141, 41), (142, 43), (144, 44),
    (142, 42), (140, 39), (138, 37), (136, 35), (134, 34),
    (132, 33), (130, 32),
]
AUSTRALIA = [
    (113, -22), (114, -28), (115, -33), (118, -35), (122, -34),
    (126, -32), (129, -32), (132, -32), (135, -35), (137, -35),
    (139, -37), (142, -38), (146, -39), (150, -37), (153, -32),
    (153, -27), (151, -24), (148, -20), (145, -17), (142, -14),
    (142, -11), (139, -12), (136, -12), (133, -12), (130, -13),
    (127, -14), (124, -15), (121, -17), (118, -20), (115, -21),
]
NEW_ZEALAND = [
    (167, -45), (169, -43), (171, -41), (174, -39), (176, -38),
    (178, -38), (176, -40), (174, -42), (171, -44), (168, -46),
]
MADAGASCAR = [
    (44, -16), (47, -15), (50, -16), (49, -19), (47, -23),
    (45, -25), (44, -22), (43, -18),
]
LAND = [
    NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, AFRICA, EURASIA, ARABIA,
    UK, SUMATRA, BORNEO, JAVA, SULAWESI, NEW_GUINEA, PHILIPPINES,
    JAPAN, AUSTRALIA, NEW_ZEALAND, MADAGASCAR,
]

# Red markers on the dot map, one per story place (lon, lat).
MARKERS = [
    (-115, 36),   # Las Vegas GP
    (-94, 39),    # Kansas City, Chiefs
    (-81, 41),    # Cleveland, Browns
    (-97, 32),    # Dallas, Cowboys
    (-66, 18),    # San Juan, Miss Universe
    (30, 37),     # Antalya, COP31
    (30, 51),     # Dymer, Ukraine
    (-5, 50),     # Cornwall, UK floods
    (34, 31),     # Gaza
    (35, 32),     # Herzliya, Eisenkot-Likud
    (34, 12),     # Blue Nile, Sudan
    (175, -41),   # Wellington, India Test
    (114, 22),    # Hong Kong Open
    (77, 28),     # New Delhi, Chahal / Pulse Polio
    (80, 13),     # Chennai Book Fair
    (116, -32),   # Perth, Ashes
    (-120, 35),   # Vandenberg, NROL-136
]

# Map geometry: lon -180..180 -> x 24..1000, lat 76..-56 -> y 356..462.
MAP_X0, MAP_X1 = 24, 1000
MAP_Y0, MAP_Y1 = 356, 462
MAP_LAT_TOP, MAP_LAT_BOT = 76, -56


def lon_to_x(lon):
    return MAP_X0 + (lon + 180) / 360 * (MAP_X1 - MAP_X0)


def lat_to_y(lat):
    return MAP_Y0 + (MAP_LAT_TOP - lat) / (MAP_LAT_TOP - MAP_LAT_BOT) * (MAP_Y1 - MAP_Y0)


def point_in_polygon(lon, lat, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > lat) != (yj > lat):
            x_cross = xi + (lat - yi) * (xj - xi) / (yj - yi)
            if lon < x_cross:
                inside = not inside
        j = i
    return inside


def on_land(lon, lat):
    for poly in LAND:
        lons = [p[0] for p in poly]
        lats = [p[1] for p in poly]
        if min(lons) - 2 <= lon <= max(lons) + 2 and min(lats) - 2 <= lat <= max(lats) + 2:
            if point_in_polygon(lon, lat, poly):
                return True
    return False


# ---------------------------------------------------------------- fonts
class Font:
    def __init__(self, name, px, ascent, height, glyphs):
        self.name = name
        self.px = px
        self.ascent = ascent
        self.height = height
        self.glyphs = glyphs  # code -> (width, bytes); bytes are height rows

    def width_of(self, text, tracking=0):
        total = 0
        for ch in text:
            g = self.glyphs.get(ord(ch))
            total += g[0] if g else 0
        if len(text) > 1:
            total += tracking * (len(text) - 1)
        return total


def load_fonts(path):
    raw = zlib.decompress(Path(path).read_bytes())
    assert raw[:4] == b"FNT1", "bad font file"
    pos = 4
    nfonts = raw[pos]
    pos += 1
    fonts = {}
    for _ in range(nfonts):
        name, px, ascent, height = struct.unpack_from(">8sHHH", raw, pos)
        pos += 14
        glyphs = {}
        for _ in range(95):
            code, w, blen = struct.unpack_from(">BBH", raw, pos)
            pos += 4
            glyphs[code] = (w, raw[pos:pos + blen])
            pos += blen
        fonts[name.rstrip(b"\0").decode()] = Font(
            name.rstrip(b"\0").decode(), px, ascent, height, glyphs)
    return fonts


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.buf = bytearray(bytes(bg) * (w * h))

    def _off(self, x, y):
        return (y * self.w + x) * 3

    def set_px(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            o = self._off(x, y)
            self.buf[o:o + 3] = bytes(color)

    def fill_rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(color) * (x1 - x0)
        for yy in range(y0, y1):
            o = self._off(x0, yy)
            self.buf[o:o + len(row)] = row

    def disc(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            dx = int((r * r - dy * dy) ** 0.5)
            self.fill_rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)

    def blit_rgb(self, x, y, w, h, rgb):
        for row in range(h):
            yy = y + row
            if 0 <= yy < self.h:
                src = row * w * 3
                o = self._off(x, yy)
                self.buf[o:o + w * 3] = rgb[src:src + w * 3]

    def draw_text(self, fonts, font_name, x, baseline, text, color, tracking=0):
        font = fonts[font_name]
        top0 = baseline - font.ascent
        pen = x
        for ch in text:
            g = font.glyphs.get(ord(ch))
            if g is None:
                continue
            gw, bits = g
            stride = (gw + 7) // 8
            for row in range(font.height):
                rowbytes = bits[row * stride:(row + 1) * stride]
                yy = top0 + row
                if yy < 0 or yy >= self.h:
                    continue
                for bi, byte in enumerate(rowbytes):
                    if not byte:
                        continue
                    for bit in range(8):
                        xx = pen + bi * 8 + bit
                        if bit >= gw - bi * 8:
                            break
                        if byte & (0x80 >> bit):
                            self.set_px(xx, yy, color)
            pen += gw + tracking

    def draw_text_centered(self, fonts, font_name, cx, baseline, text, color, tracking=0):
        font = fonts[font_name]
        w = font.width_of(text, tracking)
        self.draw_text(fonts, font_name, cx - w // 2, baseline, text, color, tracking)


# ---------------------------------------------------------------- assets
def load_panel(path):
    raw = Path(path).read_bytes()
    assert raw[:4] == b"RGBZ", "bad panel file"
    w, h = struct.unpack_from(">HH", raw, 4)
    rgb = zlib.decompress(raw[8:])
    assert len(rgb) == w * h * 3, "bad panel size"
    return w, h, rgb


# ---------------------------------------------------------------- PNG out
def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", binascii.crc32(kind + data) & 0xFFFFFFFF)
    return out


def encode_png(canvas):
    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    raw = bytearray()
    stride = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)
        raw += canvas.buf[y * stride:(y + 1) * stride]
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", ihdr)
    png += _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += _chunk(b"IEND", b"")
    return png


# ---------------------------------------------------------------- build
def build():
    fonts = load_fonts(HERE / "assets" / "font.bin")
    cv = Canvas(W, H, PAPER)

    # Masthead.
    cv.fill_rect(0, 0, W, 104, NAVY)
    cv.draw_text_centered(fonts, "TITLE", W // 2, 64, TITLE, WHITE, tracking=1)
    cv.draw_text_centered(fonts, "HEAD", W // 2, 92, DATE, GOLD)
    cv.fill_rect(0, 104, W, 4, RED)

    # Hero panels with caption bars.
    for i, (asset, caption) in enumerate(CAPTIONS):
        x = 24 + i * 328
        pw, ph, rgb = load_panel(HERE / "assets" / asset)
        cv.fill_rect(x - 1, 117, pw + 2, ph + 30, NAVY)
        cv.blit_rgb(x, 118, pw, ph, rgb)
        cv.fill_rect(x, 298, pw, 28, NAVY)
        cv.draw_text_centered(fonts, "CAPT", x + pw // 2, 317, caption, WHITE)

    # Section label with hairline rules.
    label_w = fonts["CAP"].width_of(SECTION, tracking=2)
    mid = W // 2
    cv.draw_text_centered(fonts, "CAP", mid, 348, SECTION, NAVY, tracking=2)
    cv.fill_rect(24, 342, mid - label_w // 2 - 16 - 24, 1, HAIRLINE)
    cv.fill_rect(mid + label_w // 2 + 16, 342, 1000 - (mid + label_w // 2 + 16), 1, HAIRLINE)

    # Dense dot world map.
    for gx in range(28, 997, 8):
        lon = (gx - MAP_X0) / (MAP_X1 - MAP_X0) * 360 - 180
        for gy in range(360, 461, 6):
            lat = MAP_LAT_TOP - (gy - MAP_Y0) / (MAP_Y1 - MAP_Y0) * (MAP_LAT_TOP - MAP_LAT_BOT)
            if on_land(lon, lat):
                cv.disc(gx, gy, 2, MAPDOT)
    for lon, lat in MARKERS:
        cv.disc(int(lon_to_x(lon)), int(lat_to_y(lat)), 3, RED)

    # Story cards, two columns: items 1-10 left, 11-19 right.
    row_y0 = 472
    row_h = 50
    for idx, (headline, detail) in enumerate(ITEMS):
        col = 0 if idx < 10 else 1
        row = idx if idx < 10 else idx - 10
        x = 24 if col == 0 else 524
        y = row_y0 + row * row_h
        num = "%02d" % (idx + 1)
        cv.fill_rect(x, y + 2, 26, 26, RED)
        cv.draw_text_centered(fonts, "CAP", x + 13, y + 21, num, WHITE)
        cv.draw_text(fonts, "HEAD", x + 36, y + 21, headline, INK)
        cv.draw_text(fonts, "BODY", x + 36, y + 40, detail, DETAIL)
        if row < 9:
            cv.fill_rect(x, y + 49, 476, 1, HAIRLINE)

    # Footer.
    cv.draw_text_centered(fonts, "SMALL", W // 2, 994, FOOTER, MUTED)

    return encode_png(cv)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    data = build()
    (OUT_DIR / "entry.png").write_bytes(data)


if __name__ == "__main__":
    main()
