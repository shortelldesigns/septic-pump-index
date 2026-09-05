#!/usr/bin/env python3
from __future__ import annotations

import html
from pathlib import Path

ROOT = Path("/workspace/septic-pump-index")
SITE = "Septic Pump Index"
TAG = "County-licensed septic pumpers and inspectors, transcribed from official state and county lists."
UPDATED = "29 August 2026 (US/Pacific)"

NAV = [
    ("index.html", "Home"),
    ("when-to-pump.html", "When to pump"),
    ("inspection.html", "Inspection vs pump"),
    ("montana.html", "Montana"),
    ("north-dakota.html", "North Dakota"),
    ("clallam-county-wa.html", "Clallam County"),
    ("verify.html", "Verify a license"),
    ("about.html", "About"),
]


def e(s) -> str:
    if s is None:
        return ""
    return html.escape(str(s), quote=True)


def unknown_cell(val) -> str:
    if val is None or str(val).strip() == "" or str(val).strip().lower() == "unknown":
        return '<td class="unknown">unknown</td>'
    return f"<td>{e(val)}</td>"


def header(current: str) -> str:
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'        <li><a href="{href}"{cur}>{e(label)}</a></li>')
    nav = "\n".join(items)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{title}}</title>
  <meta name="description" content="{{description}}">
  <link rel="stylesheet" href="css/site.css">
</head>
<body>
  <a class="skip" href="#content">Skip to content</a>
  <header class="site">
    <div class="brand">
      <h1><a href="index.html">{e(SITE)}</a></h1>
      <p class="tag">{e(TAG)}</p>
    </div>
    <nav class="primary" aria-label="Primary">
      <ul>
{nav}
      </ul>
    </nav>
  </header>
"""


def footer() -> str:
    return f"""  <footer class="site">
    <div class="inner">
      <p><strong>{e(SITE)}</strong> is a project by Shortell Designs. Last updated {e(UPDATED)}.</p>
      <p><a href="about.html">Methodology and disclosure</a> · <a href="verify.html">Verify a license</a></p>
      <div class="disclaimer">
        <p>This site is not a government agency and does not license pumpers, inspectors, or designers. Listings are transcribed from the official state and county sources cited on each page. Licenses expire and lists change. Confirm with the issuing agency before you hire.</p>
        <p>A pump is not an inspection. We do not rank companies. There are no live affiliate links and no click-to-call numbers on this version. We may earn a commission on future product or service links; roster names do not carry tracking numbers. This site is educational, not engineering, legal, or real-estate advice.</p>
      </div>
    </div>
  </footer>
</body>
</html>
"""


def wrap(title: str, description: str, current: str, main: str, wide: bool = False) -> str:
    head = header(current).replace("{title}", e(title)).replace("{description}", e(description))
    cls = ' class="wide"' if wide else ""
    return head + f'  <main id="content"{cls}>\n{main}\n  </main>\n' + footer()


def table(caption: str, headers: list[str], rows: list[list[str]]) -> str:
    th = "".join(f"<th>{h}</th>" for h in headers)
    body = "\n".join("".join(cells) if cells and cells[0].startswith("<tr") else ("<tr>" + "".join(cells) + "</tr>") for cells in rows)
    # rows are lists of <td> html
    trs = []
    for cells in rows:
        trs.append("<tr>" + "".join(cells) + "</tr>")
    return f"""    <div class="table-wrap">
      <table>
        <caption>{caption}</caption>
        <thead>
          <tr>{th}</tr>
        </thead>
        <tbody>
{chr(10).join(trs)}
        </tbody>
      </table>
    </div>
"""
