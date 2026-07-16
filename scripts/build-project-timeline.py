#!/usr/bin/env python3
"""Build combined featured-work timeline SVG for GitHub README."""

from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets" / "project-timeline.svg"

PROJECTS = [
    {
        "id": "a",
        "x": 24,
        "w": 288,
        "tower_h": 128,
        "tower_y": 52,
        "grad": "towerA",
        "accent": "#c4b5fd",
        "accent2": "#e9d5ff",
        "icon": "B.well",
        "hero": "65M+",
        "hero_sub": "users",
        "title": "Connected Health",
        "subtitle": "Enterprise healthcare platform",
        "dates": "2021 – 2025",
        "stats": [
            ("75% faster", "delivery"),
            ("85%+", "test coverage"),
            ("2hr → 20min", "releases"),
            ("Walgreens", "Samsung"),
        ],
        "tech": [
            "React", "TypeScript", "NestJS", "Kafka", "Redis", "GraphQL",
            "AWS", "Docker", "K8s", "Storybook", "Jest", "Cypress",
            "GH Actions", "Datadog", "Grafana",
        ],
        "footer": "Monolith → micro-frontends · HIPAA Cognito/SSO · Kafka events",
        "year_x": 156,
    },
    {
        "id": "c",
        "x": 336,
        "w": 288,
        "tower_h": 82,
        "tower_y": 98,
        "grad": "towerC",
        "accent": "#ddd6fe",
        "accent2": "#f3e8ff",
        "icon": "Biz Portal",
        "hero": "End-to-end",
        "hero_sub": "operations",
        "title": "Business Portal",
        "subtitle": "Invoicing, maps & vendor coordination",
        "dates": "2023 – 2024 · Contract",
        "stats": [
            ("Invoices", "work orders"),
            ("Maps", "messaging"),
            ("Office", "field teams"),
            ("Secure", "REST APIs"),
        ],
        "tech": [
            "Java", "Spring Boot", "PostgreSQL", "JavaScript", "Bootstrap",
            "jQuery", "Maven", "Heroku", "Jenkins", "Postman",
        ],
        "footer": "github.com/hannahpaterka/busines-portal-readme",
        "year_x": 468,
    },
    {
        "id": "b",
        "x": 648,
        "w": 288,
        "tower_h": 108,
        "tower_y": 72,
        "grad": "towerB",
        "accent": "#c4b5fd",
        "accent2": "#ede9fe",
        "icon": "Kronos",
        "hero": "85%",
        "hero_sub": "fewer errors",
        "title": "Business Management",
        "subtitle": "Spring Boot portals · office & field",
        "dates": "2025 – Present",
        "stats": [
            ("Zero", "downtime deploys"),
            ("Desktop", "+ mobile"),
            ("Invoicing", "scheduling"),
            ("Role-based", "permissions"),
        ],
        "tech": [
            "Java", "Spring Boot", "PostgreSQL", "JavaScript", "Bootstrap",
            "Heroku", "Maven", "Jenkins", "JUnit", "Git",
        ],
        "footer": "Automation · payments · job tracking · production ops",
        "year_x": 780,
    },
]


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def tech_pills(x: int, y: int, w: int, tech: list[str], fill: str) -> tuple[str, int]:
    lines: list[str] = []
    cx = x
    cy = y
    max_x = x + w - 8
    for label in tech:
        tw = len(label) * 5.6 + 14
        if cx + tw > max_x:
            cx = x
            cy += 18
        lines.append(
            f'<rect x="{cx:.0f}" y="{cy}" width="{tw:.0f}" height="14" rx="3" fill="#161b22" stroke="{fill}" stroke-width="0.6" opacity="0.95"/>'
        )
        lines.append(
            f'<text x="{cx + tw / 2:.0f}" y="{cy + 10}" text-anchor="middle" fill="#cbd5e1" font-family="ui-monospace, Menlo, monospace" font-size="6.5">{esc(label)}</text>'
        )
        cx += tw + 5
    return "\n    ".join(lines), cy + 22


def stat_grid(x: int, y: int, w: int, stats: list[tuple[str, str]], accent: str) -> str:
    parts: list[str] = []
    col_w = (w - 8) / 2
    for i, (big, small) in enumerate(stats):
        col = i % 2
        row = i // 2
        sx = x + col * (col_w + 8)
        sy = y + row * 34
        parts.append(
            f'<rect x="{sx:.0f}" y="{sy}" width="{col_w:.0f}" height="28" rx="4" fill="#161b22" opacity="0.9"/>'
        )
        parts.append(
            f'<text x="{sx + col_w / 2:.0f}" y="{sy + 13}" text-anchor="middle" fill="{accent}" font-family="ui-monospace, Menlo, monospace" font-size="9" font-weight="bold">{esc(big)}</text>'
        )
        parts.append(
            f'<text x="{sx + col_w / 2:.0f}" y="{sy + 23}" text-anchor="middle" fill="#9898a6" font-family="ui-monospace, Menlo, monospace" font-size="6.5">{esc(small)}</text>'
        )
    return "\n    ".join(parts)


def column(p: dict) -> str:
    cx = p["x"] + p["w"] / 2
    ty = p["tower_y"]
    th = p["tower_h"]
    panel_y = ty + th + 10

    parts = [
        f'<!-- {esc(p["icon"])} -->',
        f'<rect x="{p["x"]}" y="{ty}" width="{p["w"]}" height="{th}" rx="6" fill="url(#{p["grad"]})" opacity="0.95"/>',
        f'<rect x="{p["x"] + 8}" y="{ty + 8}" width="{p["w"] - 16}" height="20" rx="3" fill="#0d0820" opacity="0.55"/>',
        f'<text x="{cx}" y="{ty + 22}" text-anchor="middle" fill="{p["accent2"]}" font-family="ui-monospace, Menlo, monospace" font-size="9" font-weight="bold">{esc(p["icon"])}</text>',
        f'<text x="{cx}" y="{ty + th * 0.55:.0f}" text-anchor="middle" fill="#ffffff" font-family="ui-monospace, Menlo, monospace" font-size="20" font-weight="bold">{esc(p["hero"])}</text>',
        f'<text x="{cx}" y="{ty + th * 0.55 + 16:.0f}" text-anchor="middle" fill="{p["accent2"]}" font-family="ui-monospace, Menlo, monospace" font-size="8">{esc(p["hero_sub"])}</text>',
        f'<rect x="{p["x"]}" y="{panel_y}" width="{p["w"]}" height="248" rx="6" fill="#161b22" opacity="0.85"/>',
        f'<text x="{p["x"] + 12}" y="{panel_y + 18}" fill="{p["accent"]}" font-family="ui-monospace, Menlo, monospace" font-size="10" font-weight="bold">{esc(p["title"])}</text>',
        f'<text x="{p["x"] + 12}" y="{panel_y + 32}" fill="#9898a6" font-family="ui-monospace, Menlo, monospace" font-size="7">{esc(p["subtitle"])}</text>',
        f'<text x="{p["x"] + 12}" y="{panel_y + 46}" fill="#6b7280" font-family="ui-monospace, Menlo, monospace" font-size="7">{esc(p["dates"])}</text>',
        stat_grid(p["x"] + 10, panel_y + 54, p["w"] - 20, p["stats"], p["accent"]),
    ]

    tech_y = panel_y + 130
    pills, end_y = tech_pills(p["x"] + 10, tech_y, p["w"] - 20, p["tech"], p["accent"])
    parts.append(pills)
    parts.append(
        f'<text x="{p["x"] + 12}" y="{min(end_y + 8, panel_y + 238)}" fill="#6b7280" font-family="ui-monospace, Menlo, monospace" font-size="6">{esc(p["footer"])}</text>'
    )
    return "\n  ".join(parts)


def main() -> None:
    cols = "\n  ".join(column(p) for p in PROJECTS)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="620" viewBox="0 0 960 620" role="img" aria-label="Featured work timeline">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0a0618"/>
      <stop offset="100%" stop-color="#151028"/>
    </linearGradient>
    <linearGradient id="towerA" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ad5afc"/>
      <stop offset="100%" stop-color="#6025a5"/>
    </linearGradient>
    <linearGradient id="towerB" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#a78bfa"/>
      <stop offset="100%" stop-color="#5b21b6"/>
    </linearGradient>
    <linearGradient id="towerC" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#c084fc"/>
      <stop offset="100%" stop-color="#7e22ce"/>
    </linearGradient>
  </defs>

  <rect width="960" height="620" fill="url(#bg)" rx="12"/>

  <text x="480" y="30" text-anchor="middle" fill="#c4b5fd" font-family="ui-monospace, Menlo, monospace" font-size="14" letter-spacing="0.12em" font-weight="bold">FEATURED WORK</text>
  <text x="480" y="46" text-anchor="middle" fill="#6b7280" font-family="ui-monospace, Menlo, monospace" font-size="8">Building heights reflect project scale · 2021 – Present</text>

  {cols}

  <!-- timeline rail -->
  <line x1="40" y1="582" x2="920" y2="582" stroke="#4c1d95" stroke-width="2"/>
  <circle cx="156" cy="582" r="5" fill="#a855f7"/>
  <circle cx="480" cy="582" r="5" fill="#a855f7"/>
  <circle cx="780" cy="582" r="5" fill="#a855f7"/>
  <text x="156" y="602" text-anchor="middle" fill="#9898a6" font-family="ui-monospace, Menlo, monospace" font-size="10">2021</text>
  <text x="480" y="602" text-anchor="middle" fill="#9898a6" font-family="ui-monospace, Menlo, monospace" font-size="10">2023</text>
  <text x="780" y="602" text-anchor="middle" fill="#9898a6" font-family="ui-monospace, Menlo, monospace" font-size="10">2025</text>

  <!-- connection arcs -->
  <path d="M 312 170 Q 420 120 336 140" fill="none" stroke="#7c3aed" stroke-width="1" opacity="0.3" stroke-dasharray="4 3"/>
  <path d="M 624 155 Q 700 115 648 130" fill="none" stroke="#7c3aed" stroke-width="1" opacity="0.3" stroke-dasharray="4 3"/>
</svg>
'''
    OUT.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
