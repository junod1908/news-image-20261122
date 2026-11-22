# news-image-20261122 — "Sum up 22 November's world news in one image."
#
# The entry is the front page saved as entry.png next to this file: a single
# page that names the day (Sunday, 22 November 2026) and packs its world news
# into painted hero panels, a numbered world map and story cards — every story
# date-checked to that Sunday. This program's whole job is to place that image
# where the grader looks for it: /output/entry.png (or $MAKEFUN_OUTPUT_DIR
# outside the grader). It reads no input and uses no clock or randomness, so
# two runs write byte-identical files.
#
# Run it locally with:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

OUT_DIR.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "entry.png", OUT_DIR / "entry.png")
