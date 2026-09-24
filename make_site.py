#!/usr/bin/env python3
"""Assemble the Netlify publish folder (dist/) - DILI ORBIT only."""
import shutil, subprocess, pathlib

ROOT = pathlib.Path(__file__).parent
DIST = ROOT / "dist"


def main():
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    shutil.copy(ROOT / "8bit" / "dili-orbit.html", DIST / "index.html")
    # share image for link previews (og:image), from the 8-bit title screen
    shot = ROOT / "8bit" / "preview" / "title_v3.png"
    if shot.exists():
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(shot),
                        "-vf", "scale=672:630:flags=neighbor,pad=1200:630:(ow-iw)/2:0:black",
                        str(DIST / "shot.png")], check=True)
    # old /8bit/ links keep working
    (DIST / "_redirects").write_text("/8bit/ /  301\n/8bit/* /  301\n", encoding="utf-8")
    (DIST / "_headers").write_text("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: no-referrer\n", encoding="utf-8")
    for p in sorted(DIST.rglob("*")):
        if p.is_file(): print(f"  {p.relative_to(DIST)}  {p.stat().st_size} bytes")
    print("dist ready:", DIST)


if __name__ == "__main__":
    main()
