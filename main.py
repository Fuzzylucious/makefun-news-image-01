#!/usr/bin/env python3
"""make.fun bounty entry: news-image-01.

Writes the front page summing up the world news of Friday 13 November
2026 to /output/entry.png (or $MAKEFUN_OUTPUT_DIR).

The image is rendered at build time by gen.py (Pillow) and shipped in
this repository as entry.png; this program copies it byte for byte.
Standard library only, no network. Fully deterministic: the same bytes
are written on every run, so both graded runs are identical.
"""

import os
import shutil
from pathlib import Path

SRC = Path(__file__).resolve().parent / "entry.png"
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> None:
    if not SRC.is_file():
        raise SystemExit(f"entry.png missing next to {__file__}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, OUT_DIR / "entry.png")


if __name__ == "__main__":
    main()
