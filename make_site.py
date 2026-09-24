#!/usr/bin/env python3
"""Assemble the Netlify publish folder (dist/) from the two builds."""
import os, shutil, pathlib

ROOT = pathlib.Path(__file__).parent
DIST = ROOT / "dist"

def main():
    if DIST.exists(): shutil.rmtree(DIST)
    (DIST / "8bit").mkdir(parents=True)
    shutil.copy(ROOT / "index.html", DIST / "index.html")                    # smooth build at /
    shutil.copy(ROOT / "8bit" / "astro-dash-8bit.html", DIST / "8bit" / "index.html")   # 8-bit at /8bit/
    (DIST / "_headers").write_text(
        "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: no-referrer\n", encoding="utf-8")
    for p in sorted(DIST.rglob("*")):
        if p.is_file(): print(f"  {p.relative_to(DIST)}  {p.stat().st_size} bytes")
    print("dist ready:", DIST)

if __name__ == "__main__":
    main()
