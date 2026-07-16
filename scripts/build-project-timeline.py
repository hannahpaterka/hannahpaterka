#!/usr/bin/env python3
"""Build featured-work cards SVG for GitHub README."""

from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets" / "project-timeline.svg"

SVG_W = 680
CARD_W = SVG_W
CARD_GAP = 16
LEFT_W = 164
PAD = 20
RADIUS = 14

PROJECTS = [
    {
        "company": "B.well",
        "panel": "#7c3aed",
        "metric": "65M+",
        "metric_label": "users served",
        "title": "Connected Health",
        "subtitle": "Enterprise healthcare platform",
        "achievements": [
            "75% faster feature delivery for Walgreens & Samsung",
            "Monolith → React micro-frontends & NestJS microservices",
            "Releases 2hr → 20min · 85%+ test coverage",
            "HIPAA Cognito/SSO, IAM & Kafka event pipelines",
        ],
        "tech": ["React", "TypeScript", "NestJS", "Kafka", "AWS", "GraphQL"],
    },
    {
        "company": "Independent",
        "panel": "#6d28d9",
        "metric": "End-to-end",
        "metric_label": "portal delivery",
        "title": "Business Portal",
        "subtitle": "Invoicing, maps & vendor coordination",
        "achievements": [
            "Spring Boot portal for invoices, work orders & scheduling",
            "Maps, messaging & vendor tools for field teams",
            "PostgreSQL schemas & secure role-based REST APIs",
        ],
        "tech": ["Java", "Spring Boot", "PostgreSQL", "JavaScript", "Bootstrap"],
    },
    {
        "company": "Kronos",
        "panel": "#8b5cf6",
        "metric": "Automation",
        "metric_label": "ops & workflows",
        "title": "Business Management",
        "subtitle": "Spring Boot · office & field teams",
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


def achievement_block(x: int, y: int, achievements: list[str], max_w: int) -> tuple[str, int]:
    parts: list[str] = []
    cy = y
    line_h = 12
    max_chars = max(26, int(max_w / 5.4) - 2)
    for achievement in achievements:
        lines = wrap_text(achievement, max_chars)
        for index, line in enumerate(lines):
            if index == 0:
                parts.append(
                    f'<text x="{x}" y="{cy + 4 + index * line_h}" fill="#7c3aed" '
                    f'font-family="system-ui, -apple-system, sans-serif" font-size="9">'
                    f"•</text>"
                )
                text_x = x + 10
            else:
                text_x = x + 10
            parts.append(
                f'<text x="{text_x}" y="{cy + 4 + index * line_h}" fill="#374151" '
                f'font-family="system-ui, -apple-system, sans-serif" font-size="9">'
                f"{esc(line)}</text>"
            )
        cy += 6 + len(lines) * line_h
    return "\n    ".join(parts), cy


def tech_pills(x: int, y: int, tech: list[str], max_w: int) -> tuple[str, int]:
    parts: list[str] = [
        f'<text x="{x}" y="{y}" fill="#64748b" '
        f'font-family="ui-monospace, Menlo, monospace" font-size="7.5" '
        f'letter-spacing="0.08em">TECH</text>',
    ]
    pill_h = 17
    gap_x = 5
    gap_y = 5
    cx = x + 34
    cy = y - 11
    row_start = cx
    for label in tech:
        pill_w = max(32, len(label) * 5.4 + 12)
        if cx + pill_w > x + max_w:
            cx = row_start
            cy += pill_h + gap_y
        parts.extend(
            [
                f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{pill_w:.1f}" height="{pill_h}" '
                f'rx="8" fill="#f9fafb" stroke="#e5e7eb" stroke-width="1"/>',
                f'<text x="{cx + pill_w / 2:.1f}" y="{cy + 11.5}" text-anchor="middle" '
                f'fill="#475569" font-family="ui-monospace, Menlo, monospace" '
                f'font-size="7.5">{esc(label)}</text>',
            ]
        )
        cx += pill_w + gap_x
    return "\n    ".join(parts), cy + pill_h + 4


def panel_path(y: int, h: float) -> str:
    r = RADIUS
    return (
        f"M 0 {y + r} Q 0 {y} {r} {y} L {LEFT_W} {y} L {LEFT_W} {y + h} "
        f"L {r} {y + h} Q 0 {y + h} 0 {y + h - r} Z"
    )


def card_height(project: dict) -> int:
    content_x = LEFT_W + PAD
    content_w = CARD_W - content_x - PAD
    _, ach_end = achievement_block(content_x, 78, project["achievements"], content_w)
    _, tech_end = tech_pills(content_x, ach_end + 18, project["tech"], content_w)
    return max(132, tech_end + PAD)


def panel_sidebar(project: dict, y: int, card_h: int) -> str:
    cx = LEFT_W / 2
    metric_lines = wrap_text(project["metric"], 11)
    metric_size = 10 if max(len(line) for line in metric_lines) > 9 else 12
    line_step = 13

    block_h = 10 + 10 + len(metric_lines) * line_step + metric_size + 8
    block_top = y + (card_h - block_h) / 2
    company_y = block_top + 10
    rule_y = company_y + 10
    metric_y = rule_y + 14
    label_y = metric_y + (len(metric_lines) - 1) * line_step + metric_size + 4

    parts = [
        f'<text x="{cx:.0f}" y="{company_y:.1f}" text-anchor="middle" fill="#ffffff" '
        f'font-family="ui-monospace, Menlo, monospace" font-size="8.5" font-weight="700" '
        f'letter-spacing="0.14em">{esc(project["company"].upper())}</text>',
        f'<line x1="{cx - 22:.0f}" y1="{rule_y:.1f}" x2="{cx + 22:.0f}" y2="{rule_y:.1f}" '
        f'stroke="#ffffff" stroke-width="1" opacity="0.35"/>',
    ]
    for index, line in enumerate(metric_lines):
        parts.append(
            f'<text x="{cx:.0f}" y="{metric_y + index * line_step:.1f}" text-anchor="middle" '
            f'fill="#ffffff" font-family="system-ui, -apple-system, sans-serif" '
            f'font-size="{metric_size}" font-weight="700">{esc(line)}</text>'
        )
    parts.append(
        f'<text x="{cx:.0f}" y="{label_y:.1f}" text-anchor="middle" fill="#ffffff" '
        f'opacity="0.78" font-family="system-ui, -apple-system, sans-serif" font-size="7">'
        f'{esc(project["metric_label"])}</text>'
    )
    return "\n      ".join(parts)


def card(project: dict, y: int, card_h: int) -> str:
    panel = project["panel"]
    content_x = LEFT_W + PAD
    content_w = CARD_W - content_x - PAD

    achievements, ach_end = achievement_block(content_x, y + 78, project["achievements"], content_w)
    tech, _ = tech_pills(content_x, ach_end + 18, project["tech"], content_w)

    return "\n  ".join(
        [
            f'<!-- {esc(project["company"])} -->',
            f'<rect x="0" y="{y}" width="{CARD_W}" height="{card_h}" rx="{RADIUS}" '
            f'fill="#ffffff" stroke="#e5e7eb" stroke-width="1"/>',
            f'<path d="{panel_path(y, card_h)}" fill="{panel}"/>',
            f"  {panel_sidebar(project, y, card_h)}",
            f'<text x="{content_x}" y="{y + 34}" fill="#111827" '
            f'font-family="system-ui, -apple-system, sans-serif" font-size="16" '
            f'font-weight="700">{esc(project["title"])}</text>',
            f'<text x="{content_x}" y="{y + 52}" fill="#64748b" '
            f'font-family="system-ui, -apple-system, sans-serif" font-size="8.5">'
            f'{esc(project["subtitle"])}</text>',
            f'<line x1="{content_x}" y1="{y + 62}" x2="{CARD_W - PAD}" y2="{y + 62}" '
            f'stroke="#f3f4f6" stroke-width="1"/>',
            f"  {achievements}",
            f"  {tech}",
        ]
    )


def main() -> None:
    heights = [card_height(p) for p in PROJECTS]
    y = 0
    rendered: list[str] = []
    for project, card_h in zip(PROJECTS, heights):
        rendered.append(card(project, y, card_h))
        y += card_h + CARD_GAP

    svg_h = y - CARD_GAP if y else 0
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" height="{svg_h}" viewBox="0 0 {SVG_W} {svg_h}" role="img" aria-label="Featured work">
  <rect width="{SVG_W}" height="{svg_h}" fill="#ffffff"/>
  {"  ".join(rendered)}
</svg>
'''
    OUT.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUT} ({SVG_W}x{svg_h})")


if __name__ == "__main__":
    main()
