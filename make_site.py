#!/usr/bin/env python3
"""Assemble the Netlify publish folder (dist/) - DILI ORBIT only."""
import shutil, subprocess, pathlib

ROOT = pathlib.Path(__file__).parent
DIST = ROOT / "dist"


def main():
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    shutil.copy(ROOT / "8bit" / "dili-orbit.html", DIST / "index.html")
    # share image for link previews (og:image): 2x the NES screen, centred, crisp pixels
    shot = ROOT / "8bit" / "preview" / "title.png"
    if shot.exists():
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(shot),
                        "-vf", "scale=512:480:flags=neighbor,pad=1200:630:344:75:black,"
                               "drawbox=x=344:y=75:w=512:h=480:color=0x3cbcfc@0.7:t=2",
                        str(DIST / "shot.png")], check=True)
    # old /8bit/ links keep working
    (DIST / "_redirects").write_text("/8bit/ /  301\n/8bit/* /  301\n", encoding="utf-8")
    (DIST / "_headers").write_text("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: no-referrer\n", encoding="utf-8")
    for p in sorted(DIST.rglob("*")):
        if p.is_file(): print(f"  {p.relative_to(DIST)}  {p.stat().st_size} bytes")
    print("dist ready:", DIST)


if __name__ == "__main__":
    main()
