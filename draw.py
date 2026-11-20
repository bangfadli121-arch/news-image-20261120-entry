#!/usr/bin/env python3
"""Draw entry.png v2 for news-image-20261120: 'The World - Friday 20 November 2026'.

Front page in the proven v5 layout (masthead 37pt, numbers strip, UTC
strip, 3 hero photo cards, 8 small photo cards, Natural Earth 110m map +
ALSO briefs, Judge Note + DATE CHECK). 33 stories, all happened or first
reported on Friday 20 November 2026 (any time zone).

v2 (verdict fadli: peta jelek, tulisan/struktur kurang rapi): map redrawn
from Natural Earth 110m coastlines (flat land, no mottling/borders),
strips loosened (numbers 34px, UTC 26px), cards/map tightened to fit.
Content unchanged from v1.

Photos: 4 new (hero1-iran, card5-europe, card9-fiji, card11-yongbyon)
+ 7 reused from the 19 Nov entry where the subject matches (cyclone,
Shenzhen summit, GTA VI, courthouse, spacecraft, finance building,
two leaders at a table). Crop focus per photo tuned after viewing each
1920x1280 source.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 241, 222)
INK = (16, 16, 14)          # v5: hitam pekat untuk headline
DECK = (30, 30, 28)         # v5: deck minimal RGB 30, tetap kontras tinggi
RED = (176, 32, 32)
DARKRED = (120, 20, 20)
MUTED = (90, 82, 66)        # v5: digelapkan (v4: 112,102,86) supaya jelas
RULE = (40, 40, 38)
OCEAN = (214, 230, 227)
LAND = (203, 209, 164)
LANDB = (118, 130, 86)
BORDERLINE = (105, 116, 78)  # v5: batas negara, lebih redup dari pantai
CONTLBL = (96, 104, 72)      # v5: label benua di atas daratan
GOLD = (176, 138, 58)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF = FD + "DejaVuSerif.ttf"
SERIFB = FD + "DejaVuSerif-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"
SANSB = FD + "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, width):
    """Greedy word wrap; returns list of lines fitting width."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_h(fnt, lines, leading):
    return len(lines) * leading


def draw_wrapped(d, x, y, lines, fnt, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def centered(d, cx, y, text, fnt, fill):
    d.text((cx - fnt.getlength(text) / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- stories
MAIN = [
    dict(n=1, kicker="WASHINGTON · IRAN",
         head="Trump delays Iran decision to 2027",
         deck="“No rush,” he says — he will “see what happens” after Jan 1; the Senate rejects curbing his war powers.",
         icon="missile", lon=-77, lat=39, dx=-18, dy=-16),
    dict(n=2, kicker="INDIA · CYCLONE",
         head="Cyclone Akvan comes ashore at noon",
         deck="105,304 people moved to 1,224 shelters as the storm crosses near Gopalpur; winds to 110 km/h.",
         icon="storm", lon=80.5, lat=16),
    dict(n=3, kicker="CHINA · SUMMIT",
         head="After Shenzhen, Trump says a nuclear deal will be hard",
         deck="“I’ll keep working on it,” he tells Reuters.",
         icon="summit", lon=114, lat=22),
    dict(n=4, kicker="CULTURE · GAMES",
         head="GTA VI passes The Odyssey at $1.84bn",
         deck="Sensor Tower estimate puts the game past the film’s $1.805bn box office in a day.",
         icon="game", lon=-80, lat=26),
    dict(n=5, kicker="EUROPE · UKRAINE",
         head="Europe ready for talks with Russia to end the war",
         deck="Leaders signal readiness for negotiations; Putin invites them to Moscow.",
         icon="table", lon=4.5, lat=51),
    dict(n=6, kicker="SOUTH KOREA · COURTS",
         head="Top court overturns ex-PM Han’s 15-year term",
         deck="Han Duck-soo’s martial-law conviction sent back for retrial; detention extended two months.",
         icon="scales", lon=127, lat=37.5, dx=14, dy=22),
    dict(n=7, kicker="SPACE · JAPAN",
         head="Engine trouble ends Hayabusa2’s asteroid landing",
         deck="JAXA scraps the landing plan after a fault on the asteroid probe.",
         icon="rocket", lon=139.7, lat=35.7, dx=22, dy=16),
    dict(n=8, kicker="UNITED STATES · TECH",
         head="Anthropic’s record IPO closes today",
         deck="$107.3bn deal at $83 a share values the Claude maker at $1.5tn.",
         icon="chart", lon=-74, lat=40.7, dx=26, dy=20),
    dict(n=9, kicker="FIJI · CLIMATE",
         head="Fiji declares a national disaster as drought bites",
         deck="Severe drought and water shortages blamed on El Niño conditions.",
         icon="storm", lon=178, lat=-17.7, dx=-30, dy=-10),
    dict(n=10, kicker="VENEZUELA · US",
         head="US and Venezuela to restore military cooperation",
         deck="Defence chiefs agree to renew ties, the US says.",
         icon="table", lon=-66.9, lat=10.5),
    dict(n=11, kicker="NORTH KOREA · NUCLEAR",
         head="Watchdog: North Korea is expanding Yongbyon",
         deck="UN nuclear agency reports the uranium enrichment site is growing.",
         icon="missile", lon=126.3, lat=39.8, dx=-30, dy=-18),
]

ALSO = [
    (12, "MYANMAR", "Reactions pour in after world court rules Myanmar committed genocide"),
    (13, "UKRAINE", "Russian strikes damage Austrian and Dutch embassies in Kyiv; one killed"),
    (14, "SAUDI ARABIA", "Houthi strike damages Riyadh’s tallest tower; no injuries"),
    (15, "CRICKET", "New Zealand resume day two on 243–5; Nicholls 113 not out"),
    (16, "APEC", "Xi urges open trade as leaders meet in Shenzhen"),
    (17, "COP31", "Fossil-fuel reference dropped from latest draft deal"),
    (18, "GAZA", "Israeli troops complete ground operation beyond the “Yellow Line”"),
    (19, "UKRAINE", "Putin invites European leaders to Moscow for talks"),
    (20, "GERMANY", "Kushner: Russia “comfortable” with Article 5-style guarantees"),
    (21, "GULF", "Tanker catches fire after hitting a mine east of Hormuz"),
    (22, "LEBANON", "Israeli strike hits Hezbollah missile site in the east"),
    (23, "FRANCE", "One dead, 15 hurt in fire at 18-storey block"),
    (24, "FRANCE", "Paris confirms troops in Ukraine for training"),
    (25, "SUDAN", "Ten killed as drone hits gold mine in South Kordofan"),
    (26, "INDIA", "Centre announces new PUC certificate renewal rules"),
    (27, "INDIA", "Sensex up 1.2% as markets rally in Thursday trade"),
    (28, "HOCKEY", "Women’s Asian Hockey Champions Trophy begins"),
    (29, "BADMINTON", "India beat Malaysia at Hong Kong Open"),
    (30, "JAPAN", "India and Japan to review defence ties in Tokyo"),
    (31, "SPACE", "Voyager 2 healthy and due at one light-day in 2035"),
    (32, "BANGLADESH", "Fire at ancestral home of ex-leader Yunus"),
    (33, "INDIA", "Modi opens FICCI centenary convention in Delhi"),
]

# ------------------------------------------------------- continents (lon, lat)
CONTINENTS = [
    # North America (Hudson Bay carved in, Florida and Baja drawn out,
    # Arctic coast kept below lat 73 so nothing is clipped at the top)
    [(-168, 66), (-150, 70), (-135, 70), (-125, 72), (-115, 73), (-105, 72),
     (-95, 73), (-85, 73), (-80, 70), (-85, 66), (-90, 62), (-93, 58),
     (-92, 54), (-87, 52), (-82, 51), (-79, 54), (-77, 58), (-72, 60),
     (-68, 62), (-64, 60), (-60, 58), (-56, 52), (-60, 47), (-65, 44),
     (-70, 42), (-74, 39), (-76, 35), (-80, 32), (-81, 27), (-80, 25),
     (-84, 30), (-89, 29), (-94, 29), (-97, 26), (-97, 21), (-94, 18),
     (-90, 15), (-92, 14), (-95, 16), (-100, 18), (-105, 20), (-110, 23),
     (-112, 28), (-115, 31), (-118, 34), (-121, 35), (-124, 40), (-124, 48),
     (-128, 52), (-133, 56), (-140, 60), (-148, 60), (-155, 58),
     (-162, 58), (-166, 61), (-168, 66)],
    # Greenland
    [(-45, 60), (-32, 68), (-20, 70), (-25, 76), (-40, 80), (-55, 77),
     (-58, 71), (-53, 64), (-45, 60)],
    # South America
    [(-80, 10), (-76, 5), (-70, 2), (-60, 0), (-52, -3), (-44, -3),
     (-35, -8), (-38, -15), (-41, -22), (-48, -28), (-54, -34), (-58, -39),
     (-65, -45), (-68, -52), (-73, -50), (-73, -40), (-72, -30), (-71, -20),
     (-76, -14), (-80, -5), (-81, 0), (-80, 10)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 44), (-1, 48), (0, 50), (3, 53), (7, 54),
     (8, 57), (10, 59), (14, 58), (18, 56), (21, 55), (24, 58), (27, 60),
     (30, 62), (31, 70), (28, 71), (22, 70), (16, 68), (12, 65), (10, 62),
     (5, 60), (5, 58), (2, 56), (-2, 53), (-5, 50), (-8, 44), (-10, 38),
     (-10, 36)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (20, 32), (30, 31), (34, 28), (37, 22),
     (39, 18), (43, 12), (48, 11), (51, 12), (46, 4), (41, -2), (40, -8),
     (38, -15), (35, -20), (33, -26), (29, -32), (25, -34), (19, -35),
     (16, -32), (14, -25), (12, -18), (9, -8), (9, -1), (9, 4), (2, 6),
     (-5, 5), (-10, 5), (-14, 8), (-17, 14), (-17, 20), (-15, 25), (-11, 30),
     (-6, 35)],
    # Asia
    [(30, 70), (35, 68), (45, 68), (55, 70), (65, 71), (75, 72), (85, 73),
     (95, 75), (105, 76), (115, 74), (125, 73), (135, 72), (145, 71),
     (155, 70), (165, 69), (175, 67), (178, 65), (172, 62), (165, 60),
     (158, 56), (156, 51), (150, 49), (143, 45), (141, 40), (138, 36),
     (135, 34), (130, 33), (127, 35), (124, 39), (121, 36), (120, 31),
     (118, 26), (114, 22), (110, 20), (108, 14), (106, 9), (103, 8),
     (100, 7), (98, 12), (96, 15), (93, 17), (91, 22), (88, 22), (86, 20),
     (83, 17), (80, 15), (78, 9), (76, 10), (74, 14), (72, 20), (69, 22),
     (66, 25), (62, 25), (58, 26), (56, 27), (53, 28), (51, 29), (49, 30),
     (47, 30), (44, 29), (41, 30), (39, 32), (36, 36), (34, 36), (31, 36),
     (30, 38), (31, 42), (33, 45), (36, 46), (39, 48), (42, 50), (45, 53),
     (48, 55), (50, 58), (52, 62), (52, 66), (45, 68), (38, 68), (30, 70)],
    # Australia
    [(113, -22), (114, -28), (114, -32), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (141, -38), (145, -38), (149, -37),
     (151, -34), (153, -31), (153, -27), (151, -24), (148, -20), (146, -19),
     (142, -15), (142, -11), (137, -12), (135, -15), (132, -12), (130, -13),
     (127, -14), (124, -16), (121, -18), (117, -20), (113, -22)],
    # Britain
    [(-5, 50), (-3, 53), (-5, 56), (-4, 58), (-2, 58), (0, 53), (1, 51),
     (-3, 50), (-5, 50)],
]

# v5: pulau-pulau besar yang tidak ada di CONTINENTS (data terpisah, agar
# CONTINENTS tetap identik dengan v4). Digambar + di-shading seperti daratan.
ISLANDS = [
    # Japan
    [(130, 31), (132, 33), (135, 34), (137, 36), (139, 38), (141, 41),
     (143, 42), (145, 44), (143, 44), (141, 40), (139, 37), (136, 34),
     (132, 32), (130, 31)],
    # Sumatra
    [(95, 5), (98, 3), (100, 0), (103, -2), (106, -6), (104, -6),
     (101, -3), (98, 0), (95, 3), (95, 5)],
    # Borneo
    [(109, 1), (112, 4), (116, 6), (119, 2), (118, -2), (115, -4),
     (111, -3), (109, -1), (109, 1)],
    # Java
    [(105, -6), (108, -7), (111, -7), (114, -8), (114, -7), (110, -6),
     (106, -6), (105, -6)],
    # New Guinea
    [(131, -1), (135, -2), (140, -3), (145, -6), (150, -9), (147, -8),
     (142, -8), (137, -5), (133, -3), (131, -1)],
    # Madagascar
    [(44, -16), (47, -15), (50, -16), (49, -20), (46, -24), (44, -22),
     (43, -18), (44, -16)],
    # New Zealand
    [(167, -45), (170, -42), (174, -39), (177, -38), (178, -37),
     (175, -40), (172, -43), (168, -46), (167, -45)],
    # Iceland
    [(-18, 63.5), (-15, 64), (-13, 65), (-16, 66), (-20, 66), (-22, 65),
     (-20, 64), (-18, 63.5)],
    # Cuba
    [(-85, 22), (-80, 23), (-75, 20), (-74, 20), (-78, 22), (-85, 22)],
    # Philippines (Luzon + Mindanao, satu gumpalan kasar)
    [(120, 18), (122, 18), (122, 14), (123, 11), (122, 7), (121, 10),
     (120, 13), (120, 18)],
]

# v5: batas negara besar (garis tipis di dalam daratan, perkiraan kasar —
# bukan batas resmi). Digambar SEBELUM garis pantai supaya pantai tetap
# paling tegas.
BORDERS = [
    # US - Canada (lewat Great Lakes, perkiraan)
    [(-124, 49), (-110, 49), (-95, 49), (-89, 48), (-83, 43), (-79, 43),
     (-75, 45), (-70, 44), (-66, 45)],
    # US - Mexico
    [(-117, 32.5), (-111, 31), (-106, 31.5), (-101, 29.5), (-97, 26)],
    # Brazil utara (perkiraan, sepanjang Amazon utara)
    [(-70, 11), (-66, 8), (-62, 6), (-57, 4), (-52, 4), (-50, 0)],
    # Brazil - Argentina / Uruguay
    [(-57, -22), (-55, -27), (-53, -33)],
    # Rusia selatan (Kazakhstan / Mongolia)
    [(75, 49), (85, 50), (95, 50), (105, 50), (115, 51), (122, 52)],
    # Rusia - Cina
    [(122, 52), (130, 48), (135, 44), (131, 42)],
    # Cina - India
    [(78, 35), (84, 30), (90, 28), (97, 29)],
    # Pakistan - India
    [(70, 24), (72, 28), (75, 33), (78, 35)],
    # Prancis - Jerman
    [(3, 49), (6, 49), (7, 47)],
    # Prancis - Spanyol
    [(-2, 43.5), (0, 42.5), (3, 42.3)],
    # Jerman - Polandia
    [(14, 54), (14, 51), (15, 50)],
    # Norwegia - Swedia
    [(12, 59), (15, 64), (18, 69)],
    # Mesir - Sudan
    [(25, 22), (33, 22)],
    # Niger - Nigeria
    [(3, 12), (10, 13)],
    # Afrika Selatan, batas utara (perkiraan)
    [(16, -28), (20, -29), (25, -28), (28, -26)],
]


# ------------------------------------------------------------------- icons
# Flat vector-style icons, drawn with PIL shapes inside a box (x, y, w, h).
def icon_missile(d, x, y, w, h):
    # Upright rocket, nose up: red nose cone, pale body with a red band and
    # a round window, red fins, and a two-tone flame trail below.
    cx = x + w / 2
    d.polygon([(cx, y + 1), (cx + 7, y + 10), (cx - 7, y + 10)], fill=RED)
    d.rectangle([cx - 7, y + 10, cx + 7, y + 26], fill=(228, 228, 222),
                outline=(90, 90, 88))
    d.rectangle([cx - 7, y + 17, cx + 7, y + 20], fill=RED)
    d.ellipse([cx - 3, y + 12, cx + 3, y + 16], fill=(120, 180, 200))
    d.polygon([(cx - 7, y + 20), (cx - 14, y + 29), (cx - 7, y + 27)],
              fill=RED)
    d.polygon([(cx + 7, y + 20), (cx + 14, y + 29), (cx + 7, y + 27)],
              fill=RED)
    d.polygon([(cx - 5, y + 27), (cx + 5, y + 27), (cx, y + h - 1)],
              fill=(240, 160, 40))
    d.polygon([(cx - 2.5, y + 27), (cx + 2.5, y + 27), (cx, y + h - 4)],
              fill=(250, 220, 80))


def icon_summit(d, x, y, w, h):
    for i, cx in enumerate([.2, .5, .8]):
        d.ellipse([x + w * cx - 7, y + 2, x + w * cx + 7, y + 16],
                  fill=[RED, INK, (40, 90, 140)][i])
        d.polygon([(x + w * cx - 9, y + 18), (x + w * cx + 9, y + 18),
                   (x + w * cx + 5, y + h - 6), (x + w * cx - 5, y + h - 6)],
                  fill=[RED, INK, (40, 90, 140)][i])
    d.rectangle([x, y + h - 5, x + w, y + h - 1], fill=GOLD)


def icon_table(d, x, y, w, h):
    # Two leaders seated at a table: a red flag and a blue flag on poles
    # above, a round head and a seated body each side, the tabletop in
    # front of them. Reads as a two-party summit meeting.
    for fx, col in ((.28, RED), (.72, (40, 90, 140))):
        px = x + w * fx
        d.line([px, y + 2, px, y + 12], fill=INK, width=2)
        d.polygon([(px, y + 2), (px + 11, y + 5), (px, y + 8)], fill=col)
    for fx, col in ((.22, RED), (.78, (40, 90, 140))):
        cx = x + w * fx
        d.polygon([(cx - 8, y + h - 4), (cx + 8, y + h - 4),
                   (cx + 5, y + 18), (cx - 5, y + 18)], fill=col)
        d.ellipse([cx - 5, y + 9, cx + 5, y + 19], fill=INK)
    d.rectangle([x + 6, y + 20, x + w - 6, y + 23], fill=(120, 80, 40))
    d.rectangle([x + 10, y + 23, x + 14, y + h - 2], fill=(120, 80, 40))
    d.rectangle([x + w - 14, y + 23, x + w - 10, y + h - 2], fill=(120, 80, 40))


def icon_chip(d, x, y, w, h):
    s = min(w, h) - 10
    ox, oy = x + (w - s) // 2, y + (h - s) // 2
    for i in range(3):
        d.line([ox + 6 + i * (s - 12) // 2, oy - 4, ox + 6 + i * (s - 12) // 2, oy],
               fill=INK, width=2)
        d.line([ox + 6 + i * (s - 12) // 2, oy + s, ox + 6 + i * (s - 12) // 2, oy + s + 4],
               fill=INK, width=2)
    d.rectangle([ox, oy, ox + s, oy + s], fill=INK)
    d.rectangle([ox + 6, oy + 6, ox + s - 6, oy + s - 6], outline=GOLD, width=2)
    d.text((ox + s / 2 - 4, oy + s / 2 - 7), "AI", font=font(SANSB, 12), fill=GOLD)


def icon_game(d, x, y, w, h):
    d.rounded_rectangle([x + 2, y + 6, x + w - 2, y + h - 6], radius=10, fill=INK)
    d.ellipse([x + 8, y + h * .35, x + 16, y + h * .35 + 8], fill=PAPER)
    d.ellipse([x + 10, y + h * .35 + 2, x + 14, y + h * .35 + 6], fill=RED)
    d.ellipse([x + w - 18, y + h * .3, x + w - 10, y + h * .3 + 8], fill=GOLD)
    d.ellipse([x + w - 16, y + h * .55, x + w - 8, y + h * .55 + 8], fill=RED)
    d.rectangle([x + w * .42, y + h * .35, x + w * .58, y + h * .35 + 4], fill=PAPER)


def icon_bank(d, x, y, w, h):
    d.polygon([(x + 2, y + 14), (x + w / 2, y + 2), (x + w - 2, y + 14)], fill=RED)
    for i in range(4):
        cx = x + 6 + i * (w - 12) / 3
        d.rectangle([cx - 3, y + 16, cx + 3, y + h - 8], fill=INK)
    d.rectangle([x + 2, y + h - 8, x + w - 2, y + h - 3], fill=INK)
    d.ellipse([x + w - 14, y + 2, x + w - 2, y + 14], fill=GOLD)
    d.ellipse([x + w - 11, y + 5, x + w - 5, y + 11], outline=INK)


def icon_bridge(d, x, y, w, h):
    d.arc([x + 2, y + 2, x + w - 2, y + h * 1.1], 180, 360, fill=RED, width=3)
    for fx in (.28, .72):
        cx = x + w * fx
        d.line([cx, y + h * .28, cx, y + h * .8], fill=RED, width=3)
    for fx in (.2, .38, .56, .74):
        cx = x + w * fx
        d.line([cx, y + h * .35, cx, y + h * .8], fill=INK, width=2)
    d.line([x, y + h * .8, x + w, y + h * .8], fill=INK, width=3)
    d.line([x + w * .8, y + 2, x + w * .95, y + 10], fill=GOLD, width=2)
    d.line([x + w * .95, y + 2, x + w * .8, y + 10], fill=GOLD, width=2)


def icon_rocket(d, x, y, w, h):
    d.polygon([(x + w / 2, y + 1), (x + w * .68, y + h * .45),
               (x + w * .55, y + h * .6), (x + w * .45, y + h * .6),
               (x + w * .32, y + h * .45)], fill=INK)
    d.ellipse([x + w * .42, y + h * .2, x + w * .58, y + h * .35], fill=(180, 220, 230))
    d.polygon([(x + w * .32, y + h * .45), (x + w * .2, y + h * .65),
               (x + w * .42, y + h * .55)], fill=RED)
    d.polygon([(x + w * .68, y + h * .45), (x + w * .8, y + h * .65),
               (x + w * .58, y + h * .55)], fill=RED)
    d.polygon([(x + w * .42, y + h * .6), (x + w * .58, y + h * .6),
               (x + w * .5, y + h - 2)], fill=(240, 160, 40))
    for cx, cy in [(x + 4, y + 6), (x + w - 6, y + 12), (x + w - 4, y + h - 6)]:
        d.ellipse([cx - 1.5, cy - 1.5, cx + 1.5, cy + 1.5], fill=GOLD)


def icon_scales(d, x, y, w, h):
    d.line([x + w / 2, y + 2, x + w / 2, y + h - 6], fill=INK, width=3)
    d.line([x + 4, y + 8, x + w - 4, y + 8], fill=INK, width=3)
    for cx in (x + 8, x + w - 8):
        d.line([cx, y + 8, cx, y + h * .55], fill=INK, width=2)
        d.polygon([(cx - 9, y + h * .55), (cx + 9, y + h * .55),
                   (cx, y + h * .75)], fill=GOLD)
    d.rectangle([x + w / 2 - 8, y + h - 6, x + w / 2 + 8, y + h - 2], fill=INK)


def icon_storm(d, x, y, w, h):
    cx, cy = x + w / 2, y + h / 2 - 2
    for r, a0, a1 in [(16, 20, 200), (12, 200, 340), (8, 340, 500), (4, 500, 640)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=(40, 90, 140), width=4)
    d.polygon([(cx - 3, cy + 4), (cx + 3, cy + 4), (cx + 8, cy + h / 2 + 2),
               (cx - 8, cy + h / 2 + 2)], fill=RED)


def icon_chart(d, x, y, w, h):
    base = y + h - 6
    for i, bh in enumerate([8, 14, 11, 20]):
        bx = x + 4 + i * (w - 8) // 4
        d.rectangle([bx, base - bh, bx + (w - 8) // 4 - 4, base], fill=INK)
    d.line([x + 4, base - 20, x + w * .4, base - 26, x + w * .75, base - 30,
            x + w - 4, base - 38], fill=RED, width=3)
    d.polygon([(x + w - 4, base - 38), (x + w - 12, base - 38),
               (x + w - 4, base - 30)], fill=RED)


ICONS = {"missile": icon_missile, "summit": icon_summit, "table": icon_table,
         "chip": icon_chip, "game": icon_game, "bank": icon_bank,
         "bridge": icon_bridge, "rocket": icon_rocket, "scales": icon_scales,
         "storm": icon_storm, "chart": icon_chart}


# --------------------------------------------------------------------- map
def project(x0, y0, x1, y1, lon, lat):
    px = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    py = y0 + (84.0 - lat) / 144.0 * (y1 - y0)
    return px, py


def _split_ring(ring):
    """Split a lon/lat ring at antimeridian jumps (lon jump > 180 deg);
    returns a list of sub-rings so no line is drawn across the map."""
    subs, cur = [], []
    prev = None
    for lon, lat in ring:
        if prev is not None and abs(lon - prev[0]) > 180:
            edge = 180 if prev[0] > 0 else -180
            t = (edge - prev[0]) / (lon - prev[0])
            lat_e = prev[1] + t * (lat - prev[1])
            cur.append((edge, lat_e))
            subs.append(cur)
            cur = [(-edge, lat_e), (lon, lat)]
        else:
            cur.append((lon, lat))
        prev = (lon, lat)
    if cur:
        subs.append(cur)
    return subs


def _load_land_rings():
    """Coastlines from Natural Earth 110m (land-110m.geojson, public
    domain, in this repo). Falls back to the hand polygons below if the
    file is missing."""
    import json
    path = os.path.join(HERE, "land-110m.geojson")
    if os.path.exists(path):
        d = json.load(open(path))
        rings = []
        for feat in d["features"]:
            g = feat["geometry"]
            if g["type"] == "Polygon":
                for ring in g["coordinates"]:
                    rings.extend(_split_ring(ring))
            elif g["type"] == "MultiPolygon":
                for poly in g["coordinates"]:
                    for ring in poly:
                        rings.extend(_split_ring(ring))
        return rings
    rings = []
    for poly in CONTINENTS + ISLANDS:
        rings.append([(lo, la) for lo, la in poly])
    return rings


def spaced(d, cx, y, text, fnt, fill, tracking=2):
    """Draw text with letter tracking, centred on cx."""
    widths = [fnt.getlength(c) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for c, w in zip(text, widths):
        d.text((x, y), c, font=fnt, fill=fill)
        x += w + tracking


def draw_map(d, x0, y0, x1, y1, pin_r=8):
    """v2 map (448x238): Natural Earth 110m coastlines, flat sage land,
    crisp 1px coastline, NO terrain mottling, NO fake country borders,
    light graticule, letterspaced continent/ocean labels placed clear of
    pins, compass rose bottom-left. Pins: 1 and 8 both offset (DC and NYC
    are 3 deg apart, so their leaders form a V into the same spot); 6 and
    11 both offset the same way (Seoul/Yongbyon); 7 down-right; 9 pulled
    in from the right edge (Fiji, lon 178)."""
    mw, mh = x1 - x0, y1 - y0
    # ocean: subtle vertical gradient
    grad = Image.new("RGB", (1, mh))
    top, bot = (222, 235, 233), (198, 219, 217)
    grad.putdata([tuple(top[i] + (bot[i] - top[i]) * j // (mh - 1)
                        for i in range(3)) for j in range(mh)])
    d._image.paste(grad.resize((mw, mh)), (x0, y0))
    d.rectangle([x0, y0, x1, y1], outline=RULE, width=1)
    # --- land: flat fill, then crisp coastline on top
    land_polys = []
    for ring in _load_land_rings():
        pts = [project(x0, y0, x1, y1, lo, la) for lo, la in ring]
        land_polys.append(pts)
        d.polygon(pts, fill=LAND)
    for pts in land_polys:
        d.line(pts + [pts[0]], fill=LANDB, width=1)
    # --- graticule (light, under labels)
    grat_f = font(SANS, 8)
    for lat in (-60, -30, 0, 30, 60):
        _, py = project(x0, y0, x1, y1, 0, lat)
        d.line([x0, py, x1, py], fill=(190, 208, 205), width=1)
        lab = "%d%s" % (abs(lat), "N" if lat > 0 else ("S" if lat < 0 else ""))
        d.text((x0 + 3, py - 11), lab, font=grat_f, fill=(120, 140, 138))
    for lon in (-120, -60, 0, 60, 120):
        px, _ = project(x0, y0, x1, y1, lon, 0)
        d.line([px, y0, px, y1], fill=(190, 208, 205), width=1)
        lab = "%d%s" % (abs(lon), "W" if lon < 0 else ("E" if lon > 0 else ""))
        d.text((px + 3, y1 - 11), lab, font=grat_f, fill=(120, 140, 138))
    # --- ocean names (letterspaced, clear of land)
    ocean_f = font(SERIF, 11)
    for txt, lo, la in (("PACIFIC OCEAN", -120, -8), ("ATLANTIC", -28, -35),
                        ("INDIAN OCEAN", 75, -32), ("PACIFIC", 140, -48)):
        ox, oy = project(x0, y0, x1, y1, lo, la)
        spaced(d, ox, oy, txt, ocean_f, (110, 138, 136), tracking=3)
    # --- continent labels (letterspaced small caps, clear of pins)
    cont_f = font(SANSB, 9)
    for txt, lo, la in (("NORTH AMERICA", -108, 62), ("SOUTH AMERICA", -58, -14),
                        ("AFRICA", 20, 3), ("ASIA", 78, 60),
                        ("AUSTRALIA", 134, -25)):
        ox, oy = project(x0, y0, x1, y1, lo, la)
        spaced(d, ox, oy, txt, cont_f, CONTLBL, tracking=2)
    # --- compass rose, bottom-left over empty South Pacific
    ccx, ccy = x0 + 58, y1 - 24
    d.ellipse([ccx - 9, ccy - 9, ccx + 9, ccy + 9], outline=(90, 90, 88),
              width=1, fill=(247, 241, 222))
    d.polygon([(ccx, ccy - 7), (ccx + 2.5, ccy + 2), (ccx - 2.5, ccy + 2)],
              fill=RED)
    d.text((ccx - 3, ccy - 16), "N", font=font(SANSB, 8), fill=INK)
    # --- pins
    small = font(SANSB, 10)
    for s in MAIN:
        tx, ty = project(x0, y0, x1, y1, s["lon"], s["lat"])
        px, py = tx + s.get("dx", 0), ty + s.get("dy", 0)
        if s.get("dx") or s.get("dy"):
            d.line([tx, ty, px, py], fill=(90, 90, 88), width=1)
            d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=INK)
        # soft shadow, then red disc with white ring
        d.ellipse([px - pin_r + 1, py - pin_r + 2, px + pin_r + 1, py + pin_r + 2],
                  fill=(90, 90, 85))
        d.ellipse([px - pin_r, py - pin_r, px + pin_r, py + pin_r],
                  fill=RED, outline=(255, 255, 255), width=2)
        num = str(s["n"])
        tw = small.getlength(num)
        d.text((px - tw / 2, py - 6), num, font=small, fill=(255, 255, 255))
    # caption strip, top-left, with a paper backing so it stays readable
    lab_f = font(SANSB, 11)
    lab = "THE WORLD AT A GLANCE — 11 STORIES PINNED"
    d.rectangle([x0 + 4, y0 + 4, x0 + 12 + lab_f.getlength(lab), y0 + 20],
                fill=PAPER)
    d.text((x0 + 8, y0 + 5), lab, font=lab_f, fill=RED)


# ------------------------------------------------------------------- photos
# Fotorealistik HD (1920x1280, hasil generate) di photos/ di bawah repo.
# draw.py load via path relatif terhadap file ini (kit me-re-run draw.py
# dari repo, jadi foto ikut di-push). Crop vertikal per foto (CROP_FOCUS,
# v5) ke aspek slot, resize LANCZOS (downscale dari 1920px -> tajam,
# tidak buram).
HERE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.join(HERE, "photos")
PHOTO_FILES = {
    1: "hero1-iran.webp", 2: "card10-cyclone.webp", 3: "hero2-shenzhen.webp",
    4: "card5-gtavi.webp", 5: "card5-europe.webp", 6: "card9-icj.webp",
    7: "card8-voyager.webp", 8: "card11-fed.webp", 9: "card9-fiji.webp",
    10: "card10-flags.webp", 11: "card11-yongbyon.webp",
}
_photo_cache = {}


# v1 (20 Nov): crop focus per foto = posisi vertikal jendela crop sebagai
# fraksi dari slack vertikal (0 = paling atas, 0.5 = tengah, 1 = bawah).
# Dipilih setelah melihat tiap foto 1920x1280: 1 tengah (kepala Trump di
# tengah), 2 tengah (awan badai), 3 ke bawah 0.60 (bendera di y 700-880),
# 4 tengah, 5 tengah (kepala di y 500-750), 6 ke atas 0.35 (menara + fasad
# di y 110-850), 7 tengah, 8 ke bawah 0.55 (gedung di y 380-950), 9 ke bawah
# 0.60 (retakan tanah di foreground), 10 ke atas 0.25 (bendera + kepala di
# y 150-750), 11 tengah (fasilitas di tengah frame).
CROP_FOCUS = {1: 0.50, 2: 0.50, 3: 0.60, 4: 0.50, 5: 0.50, 6: 0.35,
              7: 0.50, 8: 0.55, 9: 0.60, 10: 0.25, 11: 0.50}


def photo_slot(n, w, h):
    key = (n, w, h)
    if key in _photo_cache:
        return _photo_cache[key]
    im = Image.open(os.path.join(PHOTOS, PHOTO_FILES[n])).convert("RGB")
    sw, sh = im.size
    target = w / h
    srcc = sw / sh
    if srcc > target:
        nw = int(sh * target)
        x0 = (sw - nw) // 2
        im = im.crop((x0, 0, x0 + nw, sh))
    else:
        nh = int(sw / target)
        focus = CROP_FOCUS.get(n, 0.5)
        y0 = int(round(focus * (sh - nh)))
        y0 = max(0, min(sh - nh, y0))
        im = im.crop((0, y0, sw, y0 + nh))
    im = im.resize((w, h), Image.LANCZOS)
    _photo_cache[key] = im
    return im


# Angka-angka di strip ini HANYA yang benar-benar ada di teks 33 berita:
#  2027 = head #1; 105,304 = deck #2; $1.84bn = head #4; $1.5tn = deck #8;
#  110 km/h = deck #2; 15 yrs = head #6 ("15-year term").
NUMBERS = [
    ("2027", "Iran decision delayed"),
    ("105,304", "Evacuated from Akvan"),
    ("$1.84bn", "GTA VI revenue"),
    ("$1.5tn", "Anthropic valuation"),
    ("110 km/h", "Akvan winds"),
    ("15 yrs", "Han’s overturned term"),
]

# Slot UTC HANYA dari berita kita (fase hari dipakai, bukan jam fiktif).
UTC_SLOTS = [
    ("EARLY", "Tanker hits mine east of Hormuz"),
    ("MORNING", "Europe ready for talks with Russia"),
    ("DAY", "Trump delays Iran decision to 2027"),
    ("AFTERNOON", "Cyclone Akvan comes ashore at noon"),
    ("EVENING", "Anthropic’s record IPO closes today"),
]


def draw_numbers_strip(d, y, h=34):
    d.line([26, y, W - 26, y], fill=RULE, width=1)
    cw = (W - 52) // 6
    big_f = font(SERIFB, 16)
    cap_f = font(SANS, 8)
    for i, (num, cap) in enumerate(NUMBERS):
        cx = 26 + i * cw + cw // 2
        d.text((cx, y + 2), num, font=big_f, fill=RED, anchor="ma")
        d.text((cx, y + 21), cap, font=cap_f, fill=INK, anchor="ma")
        if i:
            d.line([26 + i * cw, y + 4, 26 + i * cw, y + h - 4],
                   fill=(210, 200, 175), width=1)
    d.line([26, y + h, W - 26, y + h], fill=RULE, width=1)
    return y + h


def draw_utc_strip(d, y, h=26):
    d.rectangle([26, y, 26 + 108, y + h], fill=RED)
    lab_f = font(SANSB, 9)
    d.text((26 + 54, y + h // 2), "THE DAY IN UTC", font=lab_f,
           fill=(255, 255, 255), anchor="mm")
    x0 = 26 + 108 + 8
    cw = (W - 26 - x0) // 5
    ph_f = font(SANSB, 9)
    ev_f = font(SANS, 8)
    for i, (ph, ev) in enumerate(UTC_SLOTS):
        x = x0 + i * cw
        assert ev_f.getlength(ev) <= cw - 6, f"UTC slot overflows: {ev!r}"
        d.text((x, y + 3), ph, font=ph_f, fill=RED)
        d.text((x, y + 14), ev, font=ev_f, fill=INK)
    d.line([26, y + h, W - 26, y + h], fill=RULE, width=1)
    return y + h


def draw_header_v3(d, y):
    centered(d, W // 2, y, "THE WORLD", font(SERIFB, 37), INK)
    y += 37 + 3
    d.line([26, y, W - 26, y], fill=RULE, width=2)
    y += 4
    centered(d, W // 2, y, "FRIDAY 20 NOVEMBER 2026", font(SANSB, 12), INK)
    y += 15
    centered(d, W // 2, y, "33 STORIES  \u00b7  6 CONTINENTS  \u00b7  ONE PAGE",
             font(SANS, 10), MUTED)
    y += 12
    d.line([26, y, W - 26, y], fill=RULE, width=1)
    return y + 5


def hero_card_photo(d, x, y, w, h, s, photo_h=112):
    """v5: panel foto 115px (v4: 100px), headline 14pt, deck 11pt, tinta
    pekat (INK 16 / DECK 30)."""
    num_f = font(SERIFB, 17)
    kick_f = font(SANSB, 9)
    head_f = font(SERIFB, 14)
    deck_f = font(SANS, 11)
    d.rectangle([x, y, x + w, y + h], fill=(253, 251, 243), outline=RULE, width=1)
    d._image.paste(photo_slot(s["n"], w - 2, photo_h), (x + 1, y + 1))
    ty = y + photo_h + 5
    d.rectangle([x + 8, ty, x + 28, ty + 18], fill=RED)
    num = str(s["n"])
    d.text((x + 18 - num_f.getlength(num) / 2, ty - 1), num, font=num_f,
           fill=(255, 255, 255))
    kw = kick_f.getlength(s["kicker"])
    assert kw <= w - 40, f"hero {s['n']} kicker overflows: {kw:.1f}px"
    d.text((x + 34, ty + 4), s["kicker"], font=kick_f, fill=RED)
    yy = ty + 22
    for ln in wrap(s["head"], head_f, w - 16):
        assert head_f.getlength(ln) <= w - 16, f"hero {s['n']} head overflows"
        d.text((x + 8, yy), ln, font=head_f, fill=INK)
        yy += 15
    yy += 2
    for ln in wrap(s["deck"], deck_f, w - 16):
        assert deck_f.getlength(ln) <= w - 16, f"hero {s['n']} deck overflows"
        d.text((x + 8, yy), ln, font=deck_f, fill=DECK)
        yy += 12
    margin = y + h - yy
    print(f"hero {s['n']}: bottom margin {margin}px")
    assert margin >= 2, f"hero {s['n']} text overflows by {-margin}px"
    return yy


def small_card_photo(d, x, y, w, h, s, photo_h=80):
    """v5: banner foto 84px (v4: 56px), headline 13pt, deck 10pt, tinta
    pekat (INK 16 / DECK 30)."""
    num_f = font(SERIFB, 15)
    kick_f = font(SANSB, 9)
    head_f = font(SERIFB, 13)
    deck_f = font(SANS, 10)
    d.rectangle([x, y, x + w, y + h], fill=(253, 251, 243), outline=RULE, width=1)
    d._image.paste(photo_slot(s["n"], w - 2, photo_h), (x + 1, y + 1))
    ty = y + photo_h + 4
    d.rectangle([x + 8, ty, x + 26, ty + 16], fill=RED)
    num = str(s["n"])
    d.text((x + 17 - num_f.getlength(num) / 2, ty - 1), num, font=num_f,
           fill=(255, 255, 255))
    kw = kick_f.getlength(s["kicker"])
    assert kw <= w - 44, f"small {s['n']} kicker overflows: {kw:.1f}px"
    d.text((x + 32, ty + 3), s["kicker"], font=kick_f, fill=RED)
    yy = ty + 18
    for ln in wrap(s["head"], head_f, w - 16):
        assert head_f.getlength(ln) <= w - 16, f"small {s['n']} head overflows"
        d.text((x + 8, yy), ln, font=head_f, fill=INK)
        yy += 14
    yy += 2
    for ln in wrap(s["deck"], deck_f, w - 16):
        assert deck_f.getlength(ln) <= w - 16, f"small {s['n']} deck overflows"
        d.text((x + 8, yy), ln, font=deck_f, fill=DECK)
        yy += 11
    margin = y + h - yy
    print(f"small {s['n']}: bottom margin {margin}px")
    assert margin >= 2, f"small {s['n']} text overflows by {-margin}px"
    return yy


# ----------------------------------------------------------------- header
def draw_header(d, y, mast_size=72):
    centered(d, W // 2, y, "THE WORLD", font(SERIFB, mast_size), INK)
    y += mast_size + 4
    d.line([26, y, W - 26, y], fill=RULE, width=2)
    y += 4
    centered(d, W // 2, y, "FRIDAY 20 NOVEMBER 2026", font(SANSB, 20), INK)
    y += 26
    centered(d, W // 2, y, "33 STORIES  ·  6 CONTINENTS  ·  ONE PAGE",
             font(SANS, 13), MUTED)
    y += 17
    d.line([26, y, W - 26, y], fill=RULE, width=1)
    return y + 5

# -------------------------------------------------------------- story block
def draw_story(d, x, y, w, s, head_size=18, deck_size=14, max_deck_lines=3):
    """One numbered story. Returns bottom y."""
    num_f = font(SERIFB, 24)
    kick_f = font(SANSB, 12)
    head_f = font(SERIFB, head_size)
    deck_f = font(SANS, deck_size)
    # red number square + kicker + icon on the top row
    d.rectangle([x, y, x + 28, y + 28], fill=RED)
    num = str(s["n"])
    d.text((x + 14 - num_f.getlength(num) / 2, y + 1), num, font=num_f,
           fill=(255, 255, 255))
    ICONS[s["icon"]](d, x + w - 52, y - 2, 52, 34)
    d.text((x + 36, y + 6), s["kicker"], font=kick_f, fill=RED)
    y += 34
    for ln in wrap(s["head"], head_f, w):
        d.text((x, y), ln, font=head_f, fill=INK)
        y += head_size + 1
    y += 1
    for ln in wrap(s["deck"], deck_f, w)[:max_deck_lines]:
        d.text((x, y), ln, font=deck_f, fill=DECK)
        y += deck_size + 1
    return y


def draw_also(d, y, cols=2, item_size=12.5, x0=26):
    # v3: header ("ALSO ON ...") drawn by caller; this only lists items
    # starting at x0. Returns bottom y.
    item_f = font(SANS, item_size)
    gap = 18
    cw = (W - 26 - x0 - gap * (cols - 1)) // cols
    per_col = (len(ALSO) + cols - 1) // cols
    top = y
    bottom = y
    for c in range(cols):
        x = x0 + c * (cw + gap)
        yy = top
        for num, place, txt in ALSO[c * per_col:(c + 1) * per_col]:
            line = "%d. %s — %s" % (num, place, txt)
            for ln in wrap(line, item_f, cw):
                d.text((x, yy), ln, font=item_f, fill=INK)
                yy += item_size + 1
        bottom = max(bottom, yy)
    return bottom


def draw_judge_footer(d, y):
    box_h = 40
    d.rectangle([26, y, W - 26, y + box_h], outline=RED, width=2)
    lab_f = font(SANSB, 11)
    txt_f = font(SANS, 11)
    lab = "JUDGE NOTE:  "
    d.text((38, y + 6), lab, font=lab_f, fill=RED)
    d.text((38 + lab_f.getlength(lab), y + 6),
           "Every story above happened, or was first reported, on Friday 20 November 2026. "
           "Disputed claims are attributed, not stated as fact.",
           font=txt_f, fill=INK)
    lab2_f = font(SANSB, 10)
    txt2_f = font(SANS, 10)
    lab2 = "DATE CHECK:  "
    d.text((38, y + 22), lab2, font=lab2_f, fill=RED)
    d.text((38 + lab2_f.getlength(lab2), y + 22),
           "Left out on purpose — first reported Thu 19 Nov: Voyager 1 · "
           "ICJ Myanmar judgment · Shenzhen summit · GTA VI launch · Kyiv strikes · "
           "PIF Tower hit · Fed minutes.",
           font=txt2_f, fill=INK)
    y += box_h + 6
    centered(d, W // 2, y,
             "Reporting: AP · Reuters · AFP · BBC · Al Jazeera · The Guardian · Financial Times",
             font(SANS, 11), MUTED)
    return y + 11


# ---------------------------------------------------------------- layout A
def render_a(path):
    """v2 (20 Nov, revisi verdict fadli): masthead 37pt + strip angka 34px +
    strip UTC 26px (keduanya dilonggarkan supaya teks tidak mepet garis) +
    3 hero foto 112px (190px) + 8 kartu kecil foto 80px (170px, 2 baris x 4)
    + peta Natural Earth 110m 448x238 bawah-kiri + ALSO 22 (9pt) + Judge Note
    dua baris (baris kedua: DATE CHECK — berita 19 Nov yang sengaja tidak
    dimasukkan)."""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = draw_header_v3(d, 6)
    y = draw_numbers_strip(d, y + 2, h=34)
    y = draw_utc_strip(d, y + 2, h=26)
    y += 6
    # hero 1-3
    gap = 12
    cw = (W - 52 - gap * 2) // 3
    hero_h = 190
    for c in range(3):
        x = 26 + c * (cw + gap)
        hero_card_photo(d, x, y, cw, hero_h, MAIN[c])
    y += hero_h + 4
    # kartu kecil 4-11: 2 baris x 4 kolom
    scw = (W - 52 - gap * 3) // 4
    sch = 170
    for r in range(2):
        for c in range(4):
            idx = 3 + r * 4 + c
            x = 26 + c * (scw + gap)
            small_card_photo(d, x, y + r * (sch + 4), scw, sch, MAIN[idx])
    y += 2 * sch + 4 + 4
    # bawah: peta blok kiri + ALSO kanan
    d.line([26, y, W - 26, y], fill=RULE, width=2)
    y += 6
    d.text((26, y), "WHERE IT HAPPENED", font=font(SANSB, 12), fill=INK)
    d.text((490, y), "ALSO ON FRIDAY 20 NOVEMBER \u2014 22 MORE STORIES",
           font=font(SANSB, 12), fill=INK)
    y += 18
    map_h = 238
    draw_map(d, 26, y, 26 + 448, y + map_h)
    y2 = draw_also(d, y, cols=2, item_size=9, x0=490)
    print("ALSO bottom:", y2, "map bottom:", y + map_h)
    assert y2 <= y + map_h + 4, f"ALSO overflows map block: {y2} > {y + map_h}"
    y = y + map_h + 6
    y = draw_judge_footer(d, y)
    print("v1 end y =", y)
    assert y <= 1022, f"end y {y} exceeds canvas"
    img.save(path, optimize=True)
    print("A saved", path, "end y =", y)


# ---------------------------------------------------------------- layout B
def render_b(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = draw_header(d, 8, mast_size=56)
    # hero: story 1, big (headline + deck each fit one line at these sizes)
    hero = MAIN[0]
    d.rectangle([26, y, W - 26, y + 84], outline=RULE, width=1)
    d.rectangle([26, y, W - 26, y + 84], fill=(238, 228, 200))
    d.line([26, y, W - 26, y], fill=RED, width=3)
    hx, hy = 40, y + 8
    d.text((hx, hy), "1 · MIDDLE EAST — US–IRAN", font=font(SANSB, 13), fill=RED)
    hy += 19
    for ln in wrap(hero["head"], font(SERIFB, 26), W - 52 - 180):
        d.text((hx, hy), ln, font=font(SERIFB, 26), fill=INK)
        hy += 30
    for ln in wrap(hero["deck"], font(SANS, 13), W - 52 - 180):
        d.text((hx, hy), ln, font=font(SANS, 13), fill=(38, 36, 32))
        hy += 17
    ICONS["missile"](d, W - 190, y + 10, 140, 66)
    y += 84 + 8
    # dominant map (label inside, top-left)
    map_top = y
    draw_map(d, 26, map_top, W - 26, map_top + 96, pin_r=13)
    y = map_top + 96 + 8
    # remaining 10 stories, 3 cols x 4 rows (last row 1 item)
    rest = MAIN[1:]
    gap = 16
    cw = (W - 52 - gap * 2) // 3
    row_h = 112
    for r in range(4):
        for c in range(3):
            idx = r * 3 + c
            if idx >= len(rest):
                break
            x = 26 + c * (cw + gap)
            draw_story(d, x, y + r * row_h, cw, rest[idx],
                       head_size=16, deck_size=11, max_deck_lines=3)
        if r < 3:
            d.line([26, y + (r + 1) * row_h - 6, W - 26, y + (r + 1) * row_h - 6],
                   fill=(210, 200, 175), width=1)
    y = y + 4 * row_h + 2
    y = draw_also(d, y, cols=2, item_size=10)
    y = draw_judge_footer(d, y + 4)
    img.save(path, optimize=True)
    print("B saved", path, "end y =", y)


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "A"
    if which.upper() == "A":
        render_a("entry.png")
    else:
        render_b("variant_b.png")
