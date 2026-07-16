#!/usr/bin/env python3
"""Build a wider GitCity skyline — uniform scale + crop (no squashed text)."""

import re
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets" / "gitcity-skyline.svg"
URL = "https://gitcity.natrajx.in/api/svg?u=hannahpaterka&theme=aurora"

NATIVE_W = 400
NATIVE_H = 296
SCALE = 1.2  # uniform — keeps labels readable, skyline wider
HEIGHT_RATIO = 2 / 3

OUT_W = NATIVE_W * SCALE
OUT_H = OUT_W * (NATIVE_H / NATIVE_W) * HEIGHT_RATIO


def fetch_inner_svg() -> str:
    with urllib.request.urlopen(URL, timeout=30) as resp:
        raw = resp.read().decode("utf-8")
    match = re.search(r"<svg[^>]*>(.*)</svg>", raw, re.DOTALL | re.IGNORECASE)
    if not match:
        raise RuntimeError("Could not parse GitCity SVG")
    return match.group(1).strip()


def main() -> None:
    inner = fetch_inner_svg()
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{OUT_W:.0f}" height="{OUT_H:.1f}" viewBox="0 0 {OUT_W:.0f} {OUT_H:.1f}" role="img" aria-label="Contribution city skyline">
  <defs>
    <clipPath id="skyline-clip">
      <rect width="{OUT_W:.0f}" height="{OUT_H:.1f}" rx="12"/>
    </clipPath>
  </defs>
  <g clip-path="url(#skyline-clip)" transform="scale({SCALE:.4f})">
{inner}
  </g>
</svg>
'''
    OUT.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUT} ({OUT_W:.0f}x{OUT_H:.1f}, uniform scale {SCALE}x, cropped)")


if __name__ == "__main__":
    main()
