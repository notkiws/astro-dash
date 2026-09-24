#!/usr/bin/env python3
"""Assemble the Netlify publish folder (dist/) from the two builds."""
import os, shutil, subprocess, pathlib

ROOT = pathlib.Path(__file__).parent
DIST = ROOT / "dist"

def main():
    if DIST.exists(): shutil.rmtree(DIST)
    (DIST / "8bit").mkdir(parents=True)
    shutil.copy(ROOT / "index.html", DIST / "index.html")                    # smooth build at /
    shutil.copy(ROOT / "8bit" / "astro-dash-8bit.html", DIST / "8bit" / "index.html")   # 8-bit at /8bit/
    shots = [(ROOT / "preview" / "title_final.png", DIST / "shot.png",
              "scale=1200:680:flags=lanczos,crop=1200:630:0:25"),
             (ROOT / "8bit" / "preview" / "title_v3.png", DIST / "shot-8bit.png",
              "scale=672:630:flags=neighbor,pad=1200:630:(ow-iw)/2:0:black")]
    for src, dst, vf in shots:
        if src.exists():
            subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src), "-vf", vf, str(dst)], check=True)
    (DIST / "_headers").write_text(
        "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: no-referrer\n", encoding="utf-8")
    for p in sorted(DIST.rglob("*")):
        if p.is_file(): print(f"  {p.relative_to(DIST)}  {p.stat().st_size} bytes")
    print("dist ready:", DIST)

if __name__ == "__main__":
    main()
