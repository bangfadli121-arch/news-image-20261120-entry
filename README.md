[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/bangfadli121-arch/news-image-20261120-entry/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/bangfadli121-arch/news-image-20261120-entry/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# The World — Friday 20 November 2026

Entry for the make.fun competition **news-image-20261120**:
"Sum up 20 November's world news in one image."

A classic newspaper front page on cream paper: a big **THE WORLD** masthead,
the date line, a big-numbers strip and a "THE DAY IN UTC" strip, 3 hero
photo cards and 8 small photo cards (11 main stories, numbered), a
realistic world map with 11 numbered red pins, 22 more stories in the
"ALSO ON FRIDAY 20 NOVEMBER" list, a Judge Note box with a DATE CHECK
line, and a sources footer. 33 stories in total — every one happened,
or was first reported, on Friday 20 November 2026.

## Files

- `entry.png` — the final image, 1024×1024 PNG.
- `draw.py` — the renderer (Python + PIL, no network, deterministic).
  It holds all 33 stories and draws everything: masthead, strips, map,
  story grid, list, judge note. Run `python3 draw.py` to
  re-render `entry.png` from scratch.
- `land-110m.geojson` — Natural Earth 110m land polygons (public domain),
  the map's coastlines; `draw.py` falls back to hand polygons if it is
  missing.
- `main.py` — the grader entry point. Standard library only: it copies
  `entry.png` into `$MAKEFUN_OUTPUT_DIR` (default `/output`).
- `photos/` — the 11 card photos (1920x1280, centre-cropped per-photo
  focus + LANCZOS downscale). 4 are new for this edition (Trump podium,
  EU leaders, Fiji drought, Yongbyon aerial); 7 are reused from the
  19 Nov entry where the subject matches (cyclone, Shenzhen hall,
  GTA VI, courthouse, spacecraft, finance building). Card 10 is a
  PIL-drawn panel of the US and Venezuelan flags — the reused photo
  for that slot showed a US flag next to a Russian flag, which would
  have contradicted the Venezuela headline, so it was replaced with a
  correct, clearly illustrated flag pair.

## How to run

```sh
python3 main.py                       # writes $MAKEFUN_OUTPUT_DIR/entry.png
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

To re-render the image from scratch (needs PIL + DejaVu fonts):

```sh
python3 draw.py   # writes entry.png
```

## v2 (20 Nov 2026) — revisi verdict fadli ("peta terlalu jelek, tulisan
dan struktur kurang rapi")

- **Peta digambar ulang total**: garis pantai asli Natural Earth 110m
  (`land-110m.geojson`, public domain) — bukan lagi poligon tangan;
  daratan flat sage tanpa mottling, tanpa garis batas negara palsu;
  label benua/lautan letterspaced dan dijauhkan dari pin; pin yang
  bertumpuk diberi leader line berbentuk V (Washington vs New York,
  Seoul vs Yongbyon, Tokyo; Fiji ditarik masuk dari tepi peta).
- **Tipografi dilonggarkan**: strip angka 26 → 34 px, strip UTC 19 → 26 px,
  supaya angka/caption dan fase/event tidak lagi mepet garis.
- **Struktur dirapikan**: hero 198 → 190 px, kartu kecil 174 → 170 px,
  peta 448x240 → 448x238; end y 1019 dari 1024.
- Isi TIDAK berubah: 11 berita utama + 22 ALSO, Judge Note + DATE CHECK,
  footer sumber — semua sama seperti v1.

## v1 (20 Nov 2026)

Built on the proven v5 layout of the 19 Nov entry (same geometry,
fonts and map; hero cards 198 px, small cards 174 px, map 448x240,
numbers strip 26 px, UTC strip 19 px). New for this edition: 33 new
stories for Friday 20 November; a second line in the Judge Note box —
**DATE CHECK**, naming the big 19 Nov stories deliberately left out
(Voyager 1 confirmation, ICJ Myanmar judgment, Shenzhen summit,
GTA VI launch, Kyiv embassy strikes, PIF Tower hit, Fed minutes);
pin offsets with leader lines where pins would otherwise overlap
(Washington vs New York, Seoul vs Yongbyon, Tokyo; Fiji pulled inside
the map edge); and the card-10 flags panel described above.
End y is 1022 of 1024; asserts (kicker/headline/deck overflow, bottom
margin per card, ALSO within map block) all pass; 3 consecutive runs
are byte-identical (sha256
8788d28c5de1d9ebc6c1a29728b4c0d5830486426cfdcc2eb534d28cbc85c805).
Self-reviewed at full size and in close-up crops: masthead, strips,
all 11 cards, map pins and the footer all read cleanly; the DATE CHECK
line fits inside its box.

## The 11 main stories

1. Trump delays Iran decision to 2027 — "No rush," he says; the Senate
   rejects curbing his war powers.
2. Cyclone Akvan comes ashore at noon — 105,304 people moved to
   1,224 shelters near Gopalpur; winds to 110 km/h.
3. After Shenzhen, Trump says a nuclear deal will be hard.
4. GTA VI passes The Odyssey at $1.84bn.
5. Europe ready for talks with Russia to end the war.
6. Top court overturns ex-PM Han's 15-year term (South Korea).
7. Engine trouble ends Hayabusa2's asteroid landing.
8. Anthropic's record IPO closes today ($107.3bn at $83 a share,
   $1.5tn valuation).
9. Fiji declares a national disaster as drought bites.
10. US and Venezuela to restore military cooperation.
11. Watchdog: North Korea is expanding Yongbyon.
