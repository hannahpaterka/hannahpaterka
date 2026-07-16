#!/usr/bin/env python3
"""Build featured-work cards SVG for GitHub README."""

from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets" / "project-timeline.svg"

CARD_W = 300
CARD_GAP = 12
MARGIN = 18
PAD = 16
CARD_TOP = 58
SVG_W = MARGIN * 2 + CARD_W * 3 + CARD_GAP * 2  # 960

PROJECTS = [
    {
        "company": "B.well",
        "accent": "#7c3aed",
        "metric": "65M+",
        "title": "Connected Health",
        "subtitle": "Enterprise healthcare platform",
        "dates": "2021 – 2025",
        "achievements": [
            "75% faster feature delivery for Walgreens & Samsung",
            "Monolith → React micro-frontends & NestJS microservices",
            "Releases 2hr → 20min · 85%+ test coverage",
            "HIPAA Cognito/SSO, IAM & Kafka event pipelines",
        ],
        "tech": ["React", "TypeScript", "NestJS", "Kafka", "AWS", "GraphQL"],
    },
    {
        "company": "Contract",
        "accent": "#9333ea",
        "metric": "Full-stack",
        "title": "Business Portal",
        "subtitle": "Invoicing, maps & vendor coordination",
        "dates": "2023 – 2024",
        "achievements": [
            "Spring Boot portal for invoices, work orders & scheduling",
            "Maps, messaging & vendor tools for field teams",
            "PostgreSQL schemas & secure role-based REST APIs",
        ],
        "tech": ["Java", "Spring Boot", "PostgreSQL", "JavaScript", "Bootstrap"],
    },
    {
        "company": "Kronos",
        "accent": "#8b5cf6",
        "metric": "85%",
        "title": "Business Management",
        "subtitle": "Spring Boot · office & field teams",
        "dates": "2025 – Present",
        "achievements": [
            "85% fewer data entry errors & support calls via automation",
            "Invoicing, payments, scheduling & job tracking",
            "Zero-downtime deploys · desktop & mobile portals",
        ],
        "tech": ["Java", "Spring Boot", "PostgreSQL", "Bootstrap", "Heroku"],
    },
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


def achievement_block(x: int, y: int, achievements: list[str]) -> tuple[str, int]:
    parts: list[str] = []
    cy = y
    line_h = 11.5
    max_chars = 36
    for achievement in achievements:
        lines = wrap_text(achievement, max_chars)
        parts.append(
            f'<text x="{x}" y="{cy + 4}" fill="#64748b" '
            f'font-family="ui-monospace, Menlo, monospace" font-size="8">—</text>'
        )
        for index, line in enumerate(lines):
            parts.append(
                f'<text x="{x + 10}" y="{cy + 4 + index * line_h}" fill="#374151" '
                f'font-family="ui-monospace, Menlo, monospace" font-size="8.5">{esc(line)}</text>'
            )
        cy += 6 + len(lines) * line_h
    return "\n    ".join(parts), cy


def body_bottom(project: dict) -> int:
    ach_start = CARD_TOP + 82
    _, ach_end = achievement_block(PAD + 4, ach_start, project["achievements"])
    return ach_end + 22


def card(project: dict, x: int, card_h: int) -> str:
    inner = x + PAD
    right = x + CARD_W - PAD
    ach_start = CARD_TOP + 82
    achievements, _ = achievement_block(inner + 4, ach_start, project["achievements"])
    stack_y = CARD_TOP + card_h - 12
    badge_w = max(48, len(project["metric"]) * 8 + 18)

    return "\n  ".join([
        f'<!-- {esc(project["company"])} -->',
        f'<rect x="{x}" y="{CARD_TOP}" width="{CARD_W}" height="{card_h}" '
        f'fill="#ffffff" stroke="#e5e7eb" stroke-width="1"/>',
        f'<rect x="{x}" y="{CARD_TOP}" width="3" height="{card_h}" fill="{project["accent"]}"/>',
        f'<text x="{inner + 4}" y="{CARD_TOP + 22}" fill="{project["accent"]}" '
        f'font-family="ui-monospace, Menlo, monospace" font-size="9" font-weight="700" letter-spacing="0.14em">'
        f'{esc(project["company"].upper())}</text>',
        f'<text x="{right}" y="{CARD_TOP + 22}" text-anchor="end" fill="#64748b" '
        f'font-family="ui-monospace, Menlo, monospace" font-size="8">{esc(project["dates"])}</text>',
        f'<rect x="{right - badge_w}" y="{CARD_TOP + 8}" width="{badge_w}" height="26" '
        f'fill="#f5f3ff" stroke="{project["accent"]}" stroke-width="1"/>',
        f'<text x="{right - badge_w / 2}" y="{CARD_TOP + 26}" text-anchor="middle" fill="{project["accent"]}" '
        f'font-family="ui-monospace, Menlo, monospace" font-size="10" font-weight="700">{esc(project["metric"])}</text>',
        f'<text x="{inner + 4}" y="{CARD_TOP + 44}" fill="#111827" font-family="ui-monospace, Menlo, monospace" '
        f'font-size="13" font-weight="700">{esc(project["title"])}</text>',
        f'<text x="{inner + 4}" y="{CARD_TOP + 60}" fill="#64748b" font-family="ui-monospace, Menlo, monospace" font-size="8">'
        f'{esc(project["subtitle"])}</text>',
        achievements,
        f'<text x="{inner + 4}" y="{stack_y}" fill="#64748b" font-family="ui-monospace, Menlo, monospace" '
        f'font-size="7.5" letter-spacing="0.06em">STACK</text>',
        f'<text x="{inner + 44}" y="{stack_y}" fill="#475569" font-family="ui-monospace, Menlo, monospace" font-size="7.5">'
        f'{esc(" · ".join(project["tech"]))}</text>',
    ])


def main() -> None:
    card_x = [MARGIN, MARGIN + CARD_W + CARD_GAP, MARGIN + (CARD_W + CARD_GAP) * 2]
    card_h = max(body_bottom(p) for p in PROJECTS) - CARD_TOP
    rendered = [card(project, x, card_h) for project, x in zip(PROJECTS, card_x)]
    timeline_centers = [x + CARD_W / 2 for x in card_x]
    timeline_y = CARD_TOP + card_h + 24
    svg_h = timeline_y + 32

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" height="{svg_h}" viewBox="0 0 {SVG_W} {svg_h}" role="img" aria-label="Featured work">
  <rect width="{SVG_W}" height="{svg_h}" fill="#ffffff"/>

  <text x="{SVG_W / 2:.0f}" y="28" text-anchor="middle" fill="#7c3aed"
    font-family="ui-monospace, Menlo, monospace" font-size="12" letter-spacing="0.18em" font-weight="700">FEATURED WORK</text>

  {"  ".join(rendered)}

  <rect x="{timeline_centers[0] - 3:.0f}" y="{timeline_y - 3}" width="6" height="6" fill="{PROJECTS[0]["accent"]}"/>
  <rect x="{timeline_centers[1] - 3:.0f}" y="{timeline_y - 3}" width="6" height="6" fill="{PROJECTS[1]["accent"]}"/>
  <rect x="{timeline_centers[2] - 3:.0f}" y="{timeline_y - 3}" width="6" height="6" fill="{PROJECTS[2]["accent"]}"/>
  <text x="{timeline_centers[0]:.0f}" y="{timeline_y + 18}" text-anchor="middle" fill="#64748b"
    font-family="ui-monospace, Menlo, monospace" font-size="9">2021</text>
  <text x="{timeline_centers[1]:.0f}" y="{timeline_y + 18}" text-anchor="middle" fill="#64748b"
    font-family="ui-monospace, Menlo, monospace" font-size="9">2023</text>
  <text x="{timeline_centers[2]:.0f}" y="{timeline_y + 18}" text-anchor="middle" fill="#64748b"
    font-family="ui-monospace, Menlo, monospace" font-size="9">2025</text>
</svg>
'''
    OUT.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUT} ({SVG_W}x{svg_h})")


if __name__ == "__main__":
    main()
