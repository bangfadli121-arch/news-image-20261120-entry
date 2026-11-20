#!/usr/bin/env python3
"""Entry point for the news-image-20261120 entry.

Copies the pre-rendered entry.png (same directory as this file) into the
output directory. Standard library only, no network, deterministic.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(OUT, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"),
                os.path.join(OUT, "entry.png"))
