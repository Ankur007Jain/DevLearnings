#!/usr/bin/env python3
"""Rebuild the HTML pages from md/ with pandoc. Run from any folder: python3 dp700-study-pack/tools/build.py"""
import pathlib, subprocess

HERE = pathlib.Path(__file__).resolve().parent.parent
PAGES = {
    "reading-pack": ("Reading pack", True),
    "question-bank": ("Question bank", False),
    "mock-1": ("Mock 1", False),
    "mock-2": ("Mock 2", False),
    "mock-3": ("Mock 3", False),
    "journey": ("From 619 to 745", False),
}
for name, (title, toc) in PAGES.items():
    cmd = ["pandoc", str(HERE / "md" / f"{name}.md"), "-f", "markdown-implicit_figures",
           "-t", "html5", "--template", str(HERE / "tools" / "template.html"),
           "--metadata", f"pagetitle={title}", "-o", str(HERE / f"{name}.html")]
    if toc:
        cmd += ["--toc", "--toc-depth=2"]
    subprocess.run(cmd, check=True)
    print("built", name)
