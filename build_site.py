#!/usr/bin/env python3
"""
build_site.py
Reads content.json + template.html → writes index.html

No external dependencies — uses only the Python standard library.
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent


def build_service_card(service: dict) -> str:
    """Return the HTML for a single service card."""
    return (
        '<div class="fade-in service-card p-8 rounded-2xl bg-slate-800/60 '
        'border border-slate-700/50 hover:border-cyan-600/40">\n'
        f'  <span class="text-4xl">{service["icon"]}</span>\n'
        f'  <h3 class="mt-5 text-xl font-semibold text-white">{service["title"]}</h3>\n'
        f'  <p class="mt-3 text-slate-400 leading-relaxed">{service["description"]}</p>\n'
        '</div>'
    )


def main() -> None:
    # Load data
    data = json.loads((ROOT / "content.json").read_text(encoding="utf-8"))

    # Load template
    html = (ROOT / "template.html").read_text(encoding="utf-8")

    # Simple placeholders
    html = html.replace("{{name}}", data["name"])
    html = html.replace("{{title}}", data["title"])
    html = html.replace("{{bio}}", data["bio"])
    html = html.replace("{{contact_email}}", data["contact"]["email"])
    html = html.replace("{{contact_linkedin}}", data["contact"]["linkedin"])
    html = html.replace("{{contact_github}}", data["contact"]["github"])
    html = html.replace("{{contact_location}}", data["contact"]["location"])

    # Build service cards
    cards_html = "\n".join(build_service_card(s) for s in data["services"])
    html = html.replace("{{services_cards}}", cards_html)

    # Write output
    out = ROOT / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"✅  Built {out}")


if __name__ == "__main__":
    main()
