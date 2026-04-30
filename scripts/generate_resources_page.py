#!/usr/bin/env python3
"""
Generate the FDE resources page with native FDE Pulse branding (dark + amber).
Canonical points to thegtmindex.com/fde/.
"""

import os
import sys
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from templates import (
    get_html_head, get_header_html, get_footer_html,
    get_mobile_nav_js, get_signup_js, get_cta_box, get_all_css,
    SITE_NAME, BASE_URL
)
try:
    from nav_config import SITE_NAME, BASE_URL
except ImportError:
    pass

PROJECT_ROOT = os.path.dirname(script_dir)

CANONICAL_URL = "https://thegtmindex.com/fde/"
TITLE = "Best Resources for Forward Deployed Engineers in 2026"
DESCRIPTION = "Curated list of the best job boards, communities, blogs, and career resources for forward deployed engineers and field engineers."
INTRO = """Forward deployed engineering started at Palantir and has spread to 50+ companies. The role sits between product engineering and customer success, with FDEs embedded directly with customers to build custom solutions.

This list covers what exists today. Job boards, engineering blogs, communities, and career resources for people who build software at the customer's site, not in the home office."""

SECTIONS = [
    {"title": "Newsletters", "items": [
        {"name": "The Pragmatic Engineer", "url": "https://newsletter.pragmaticengineer.com/", "desc": "Gergely Orosz's 1.1M+ subscriber newsletter. Published a deep-dive on forward deployed engineers."},
        {"name": "Next Play Strategy", "url": "https://nextplayso.substack.com/", "desc": "Substack newsletter with 'The Definitive Guide to Forward Deployed Engineering.'"},
    ]},
    {"title": "Blogs & Websites", "items": [
        {"name": "Palantir Engineering Blog", "url": "https://blog.palantir.com/", "desc": "Original FDE content from the company that invented the role, including 'Day in the Life' posts."},
        {"name": "SVPG - Forward Deployed Engineers", "url": "https://www.svpg.com/forward-deployed-engineers/", "desc": "Marty Cagan's Silicon Valley Product Group analysis of the FDE model."},
        {"name": "FDE Pulse", "url": "https://fdepulse.com/", "desc": "Job board and market intelligence platform for forward deployed engineers.", "owned": True},
        {"name": "Bloomberry FDE Analysis", "url": "https://bloomberry.com/blog/i-analyzed-1000-forward-deployed-engineer-jobs-what-i-learned/", "desc": "Data analysis of 1,000+ FDE job postings showing skills demand and salary trends."},
    ]},
    {"title": "Tools Worth Knowing", "items": [
        {"name": "fwddeploy.com", "url": "https://www.fwddeploy.com/", "desc": "Dedicated FDE job board aggregating forward deployed engineer roles across companies."},
        {"name": "AI Market Pulse", "url": "https://theaimarketpulse.com/", "desc": "AI career intelligence with job boards and salary data relevant to AI-focused FDE roles.", "owned": True},
    ]},
    {"title": "Courses & Training", "items": [
        {"name": "FDE Academy", "url": "https://fde.academy/", "desc": "World's first structured 32-week PGP program to become a Forward Deployed Engineer, by Futurense."},
    ]},
]


def build_body():
    """Build the body HTML for the resource page."""
    amber = "var(--amber, #F59E0B)"
    amber_light = "var(--amber-light, #FBBF24)"
    text_sec = "var(--text-secondary, rgba(255,255,255,0.6))"
    bg_card = "var(--bg-card, #162232)"
    border = "var(--border, rgba(255,255,255,0.08))"

    html = []

    # Breadcrumb + Hero
    html.append(f'''
<div class="container" style="max-width:800px;padding-top:6rem;">
  <nav style="font-size:0.85rem;color:var(--text-muted,rgba(255,255,255,0.4));margin-bottom:1rem;">
    <a href="/" style="color:{amber};text-decoration:none;">Home</a>
    <span style="margin:0 0.5rem;">/</span>
    <span>{TITLE}</span>
  </nav>
  <h1 style="font-size:2.25rem;font-weight:700;margin-bottom:1rem;line-height:1.15;">{TITLE}</h1>
''')
    for para in INTRO.strip().split("\n\n"):
        html.append(f'  <p style="color:{text_sec};font-size:1.05rem;line-height:1.7;margin-bottom:1rem;">{para}</p>')
    html.append('</div>')

    # Sections
    for section in SECTIONS:
        html.append(f'''
<div class="container" style="max-width:800px;padding:1rem 0 2rem;">
  <h2 style="font-size:1.5rem;font-weight:700;margin-bottom:1.25rem;padding-bottom:0.5rem;border-bottom:2px solid rgba(245,158,11,0.3);">{section["title"]}</h2>
  <ol style="list-style:none;padding:0;margin:0;">
''')
        for i, item in enumerate(section["items"], 1):
            owned_badge = f' <span style="display:inline-block;background:var(--amber-glow,rgba(245,158,11,0.15));color:{amber_light};font-size:0.7rem;font-weight:700;padding:2px 8px;border-radius:var(--radius-sm,4px);margin-left:8px;vertical-align:middle;letter-spacing:0.5px;">OUR PICK</span>' if item.get("owned") else ""
            html.append(f'''    <li style="margin-bottom:1.25rem;padding:1rem;background:{bg_card};border:1px solid {border};border-radius:var(--radius-md,8px);">
      <span style="color:{amber_light};font-weight:700;margin-right:0.5rem;">{i}.</span>
      <a href="{item["url"]}" target="_blank" rel="noopener" style="color:{amber_light};font-weight:600;text-decoration:none;">{item["name"]}</a>{owned_badge}
      <p style="color:{text_sec};font-size:0.95rem;margin:0.5rem 0 0;line-height:1.6;">{item["desc"]}</p>
    </li>''')
        html.append('  </ol>\n</div>')

    # How We Curated
    html.append(f'''
<div class="container" style="max-width:800px;padding:1rem 0 2rem;">
  <div style="background:var(--amber-ghost,rgba(245,158,11,0.06));border:1px solid rgba(245,158,11,0.2);border-radius:var(--radius-lg,12px);padding:1.5rem 2rem;">
    <h3 style="font-size:1.1rem;font-weight:700;margin-bottom:0.75rem;">How We Curated This List</h3>
    <p style="color:{text_sec};font-size:0.95rem;line-height:1.7;margin-bottom:0.75rem;">Every resource on this page was evaluated based on editorial independence, content depth, community engagement, and practitioner recommendations. We prioritize sources that provide original analysis over aggregated content.</p>
    <p style="color:{text_sec};font-size:0.95rem;line-height:1.7;">This page is part of <a href="https://thegtmindex.com/" target="_blank" rel="noopener" style="color:{amber_light};">The GTM Index</a>, a curated directory of the best resources across go-to-market disciplines.</p>
  </div>
</div>
''')

    return "\n".join(html)


def main():
    output_dir = os.path.join(PROJECT_ROOT, "site")

    head = get_html_head(TITLE, DESCRIPTION, "/best-fde-resources/")
    # Replace auto-generated canonical with our canonical
    head = re.sub(
        r'<link rel="canonical" href="[^"]*">',
        f'<link rel="canonical" href="{CANONICAL_URL}">',
        head
    )

    header = get_header_html()
    body = build_body()
    cta = get_cta_box()
    footer = get_footer_html()
    mobile_js = get_mobile_nav_js()
    signup_js = get_signup_js()
    all_css = get_all_css()

    page = f'''{head}
<body>
    <style>{all_css}</style>
{header}
    <main>
{body}
{cta}
    </main>
{footer}
{mobile_js}
{signup_js}
</body>
</html>'''

    out_path = os.path.join(output_dir, "best-fde-resources", "index.html")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"  Wrote {out_path}")
    print("Done: FDE Pulse resource page generated.")


if __name__ == "__main__":
    main()
