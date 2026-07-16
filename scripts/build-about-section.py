#!/usr/bin/env python3
"""Build About Me section SVG for GitHub README."""

from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets" / "about-section.svg"

SVG_W = 680
PAD = 24
TEXT_X = PAD + 8
MAX_W = SVG_W - PAD * 2 - 8
RADIUS = 14
LINE_H = 13

INTRO = [
    "Senior Software Engineer with 5 years of experience building HIPAA-compliant "
    "enterprise healthcare platforms — secure distributed systems, React micro-frontends, "
    "NestJS microservices, and event-driven apps serving 65M+ users.",
    "Currently at Kronos, building Java/Spring Boot business portals for desktop and "
    "mobile to streamline workflows for office and field teams.",
]

BULLETS = [
    "B.well Connected Health — Modernized a monolithic platform into React micro-frontends "
    "and NestJS microservices, cutting feature delivery time by 75% for clients like "
    "Walgreens and Samsung",
    "Strengthened security with AWS Cognito, SSO, IAM, and HIPAA-aligned access controls "
    "across distributed REST/GraphQL and Kafka event workflows",
    "Improved release velocity from ~2 hours to ~20 minutes with GitHub Actions, 85%+ test "
    "coverage, and monitoring via Datadog & Grafana",
    "At Kronos, building invoicing, payments, scheduling, and job-tracking systems — "
    "reducing data entry errors and calls/emails by 85% through automation",
    "Developing responsive Bootstrap/JavaScript frontends for field use, with PostgreSQL "
    "schemas and secure REST APIs with role-based permissions",
]


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def wrap_text(text: str, max_chars: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        trial = " ".join([*current, word])
        if len(trial) <= max_chars:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def text_block(x: int, y: int, lines: list[str], size: float, fill: str, weight: str = "400") -> tuple[str, int]:
    parts: list[str] = []
    cy = y
    for line in lines:
        parts.append(
            f'<text x="{x}" y="{cy}" fill="{fill}" '
            f'font-family="system-ui, -apple-system, sans-serif" font-size="{size}" '
            f'font-weight="{weight}">{esc(line)}</text>'
        )
        cy += LINE_H
    return "\n  ".join(parts), cy


def bullet_block(x: int, y: int, bullets: list[str]) -> tuple[str, int]:
    parts: list[str] = []
    cy = y
    max_chars = max(42, int(MAX_W / 5.2) - 4)
    for bullet in bullets:
        lines = wrap_text(bullet, max_chars)
        for index, line in enumerate(lines):
            if index == 0:
                parts.append(
                    f'<text x="{x}" y="{cy}" fill="#7c3aed" '
                    f'font-family="system-ui, -apple-system, sans-serif" font-size="9">•</text>'
                )
                text_x = x + 10
            else:
                text_x = x + 10
            parts.append(
                f'<text x="{text_x}" y="{cy}" fill="#374151" '
                f'font-family="system-ui, -apple-system, sans-serif" font-size="9">'
                f"{esc(line)}</text>"
            )
            cy += LINE_H
        cy += 4
    return "\n  ".join(parts), cy


def svg_height() -> int:
    y = PAD
    max_chars = max(48, int(MAX_W / 5.0))
    for paragraph in INTRO:
        y += len(wrap_text(paragraph, max_chars)) * LINE_H + 6
    y += 4
    max_chars = max(42, int(MAX_W / 5.2) - 4)
    for bullet in BULLETS:
        y += len(wrap_text(bullet, max_chars)) * LINE_H + 4
    return y + PAD


def build() -> str:
    h = svg_height()
    y = PAD + 4
    parts: list[str] = [
        f'<rect width="{SVG_W}" height="{h}" rx="{RADIUS}" fill="#ffffff" '
        f'stroke="#e5e7eb" stroke-width="1"/>',
        f'<rect x="0" y="0" width="4" height="{h}" rx="{RADIUS}" fill="#111827"/>',
    ]

    max_chars = max(48, int(MAX_W / 5.0))
    for paragraph in INTRO:
        lines = wrap_text(paragraph, max_chars)
        block, y = text_block(TEXT_X, y, lines, 9.5, "#374151")
        parts.append(block)
        y += 6

    y += 4
    bullets, y = bullet_block(TEXT_X, y, BULLETS)
    parts.append(bullets)

    body = "\n  ".join(parts)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" height="{h}" viewBox="0 0 {SVG_W} {h}" role="img" aria-label="About Me">
  {body}
</svg>
'''


def main() -> None:
    svg = build()
    OUT.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUT} ({SVG_W}x{svg_height()})")


if __name__ == "__main__":
    main()
