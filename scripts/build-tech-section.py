#!/usr/bin/env python3
"""Build minimalist tech section SVG for GitHub README."""

from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets" / "tech-section.svg"

SVG_W = 680
PAD = 24
LABEL_W = 92
CONTENT_X = PAD + LABEL_W
RADIUS = 14

CORE = ["React", "TypeScript", "Java", "Spring Boot", "NestJS", "AWS"]

CATEGORIES = [
    ("Frontend", ["JavaScript", "Bootstrap", "jQuery", "Storybook", "Webpack", "Figma", "WCAG", "i18n"]),
    ("Backend", ["Node.js", "GraphQL", "REST", "FHIR", "Maven", "Kafka"]),
    ("Data", ["PostgreSQL", "SQL", "Redis"]),
    ("Platform", ["Docker", "Kubernetes", "GitHub Actions", "Heroku", "Jenkins"]),
    ("Quality", ["Jest", "Cypress", "JUnit", "ESLint", "Prettier", "Datadog", "Grafana"]),
    ("Tools", ["Git", "GitHub", "VS Code", "Postman", "Xcode", "Android"]),
]


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def row_text(items: list[str]) -> str:
    return " · ".join(esc(item) for item in items)


def svg_height() -> int:
    return PAD + 34 + 12 + len(CATEGORIES) * 24 + PAD


def build() -> str:
    h = svg_height()
    y = PAD
    parts: list[str] = [
        f'<rect width="{SVG_W}" height="{h}" rx="{RADIUS}" fill="#ffffff" '
        f'stroke="#e5e7eb" stroke-width="1"/>',
        f'<rect x="0" y="0" width="4" height="{h}" rx="{RADIUS}" fill="#111827"/>',
        f'<text x="{PAD}" y="{y + 11}" fill="#64748b" '
        f'font-family="ui-monospace, Menlo, monospace" font-size="7.5" '
        f'letter-spacing="0.12em">CORE</text>',
        f'<text x="{CONTENT_X}" y="{y + 12}" fill="#111827" '
        f'font-family="system-ui, -apple-system, sans-serif" font-size="11" '
        f'font-weight="600">{row_text(CORE)}</text>',
    ]
    y += 34 + 12

    for label, items in CATEGORIES:
        parts.extend(
            [
                f'<text x="{PAD}" y="{y + 10}" fill="#64748b" '
                f'font-family="ui-monospace, Menlo, monospace" font-size="7.5" '
                f'letter-spacing="0.06em">{esc(label.upper())}</text>',
                f'<text x="{CONTENT_X}" y="{y + 10}" fill="#374151" '
                f'font-family="system-ui, -apple-system, sans-serif" font-size="9">'
                f"{row_text(items)}</text>",
            ]
        )
        y += 24

    body = "\n  ".join(parts)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" height="{h}" viewBox="0 0 {SVG_W} {h}" role="img" aria-label="Tech stack">
  {body}
</svg>
'''


def main() -> None:
    svg = build()
    OUT.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUT} ({SVG_W}x{svg_height()})")


if __name__ == "__main__":
    main()
