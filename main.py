#!/usr/bin/env python3
"""Entry for make.fun's "Sum up 20 November's world news in one image".

The picture itself — a front page summing up Friday 20 November
2026 — sits in this repository as entry.png (JPEG bytes under a
.png name, which the gate allows: it reads the format from the
file's first bytes). This program's whole job is to place that
picture at /output/entry.png, byte for byte, every run.

Standard library only, no network, fully deterministic.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main() -> int:
    # Copy, never re-encode: the gate measures the exact bytes, and
    # re-encoding a JPEG would change them from run to run.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
