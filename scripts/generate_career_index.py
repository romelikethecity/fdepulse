#!/usr/bin/env python3
"""Generate the Career hub index page listing all career guides."""

import os
import sys
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from nav_config import BASE_URL
from templates import (
    get_html_head, get_header_html, get_footer_html,
    get_mobile_nav_js, get_signup_js, get_cta_box, get_related_links
)

SITE_DIR = os.path.join(os.path.dirname(script_dir), 'site')

CAREER_PAGES = [
    {
        "href": "/career/what-is-a-forward-deployed-engineer/",
        "title": "What Is a Forward Deployed Engineer?",
        "desc": "The complete guide to the FDE role: what they do, who hires them, salary ranges, required skills, and why the role grew 800% in 2025.",
    },
    {
        "href": "/career/how-to-become-a-forward-deployed-engineer/",
        "title": "How to Become a Forward Deployed Engineer",
        "desc": "Step-by-step career path from SWE to FDE. Required skills, where to apply, and what companies look for in FDE candidates.",
    },
    {
        "href": "/career/forward-deployed-engineer-interview-questions/",
        "title": "FDE Interview Questions",
        "desc": "50+ real interview questions from OpenAI, Palantir, Salesforce, and more. Coding, system design, and customer scenario prep.",
    },
    {
        "href": "/career/forward-deployed-engineer-resume/",
        "title": "FDE Resume Guide",
        "desc": "How to write a resume that gets FDE interviews. Key sections, skills to highlight, and what hiring managers actually look for.",
    },
    {
        "href": "/career/forward-deployed-engineer-new-grad/",
        "title": "FDE for New Grads",
        "desc": "Which companies hire new grad FDEs, what they pay, how to prepare, and whether FDE is a good first job.",
    },
    {
        "href": "/career/forward-deployed-ai-engineer/",
        "title": "Forward Deployed AI Engineer",
        "desc": "The fastest-growing FDE specialization. LLM deployment skills, salary ($180K-$300K), and how the AI FDE role differs from standard FDE.",
    },
    {
        "href": "/career/forward-deployed-strategist/",
        "title": "Forward Deployed Strategist",
        "desc": "The business-focused counterpart to FDE. What an FDS does, salary ranges, and companies like Palantir and ElevenLabs that hire.",
    },
    {
        "href": "/career/forward-deployed-engineer-levels/",
        "title": "FDE Levels and Career Progression",
        "desc": "Career ladder from Associate to Staff/Lead FDE. Salary by level, promotion timelines, and how FDE levels compare to standard SWE.",
    },
    {
        "href": "/career/forward-deployed-engineer-work-life-balance/",
        "title": "FDE Work-Life Balance and Travel",
        "desc": "Real talk on travel expectations (20-60%), burnout risk, remote options, and how to evaluate FDE lifestyle by company.",
    },
]


def generate_career_index():
    print("  Generating career index page...")

    cards = ""
    for page in CAREER_PAGES:
        cards += f'''
                <a href="{page['href']}" style="display: block; text-decoration: none; background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 1.5rem; transition: all 0.25s ease;">
                    <h3 style="font-size: 1.15rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">{page['title']}</h3>
                    <p style="color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6; margin: 0;">{page['desc']}</p>
                </a>'''

    related = get_related_links([
        {"href": "/salaries/", "label": "FDE Salary Data"},
        {"href": "/companies/", "label": "Companies Hiring FDEs"},
        {"href": "/jobs/", "label": "Browse FDE Jobs"},
        {"href": "/insights/", "label": "Market Insights"},
    ])

    body = f'''
        <section class="section" style="max-width: 900px; margin: 0 auto; padding-top: 8rem;">
            <h1 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem;">FDE Career Guides</h1>
            <p style="font-size: 1.15rem; color: var(--text-secondary); margin-bottom: 2.5rem; line-height: 1.7;">Everything you need to start, advance, or evaluate a Forward Deployed Engineer career. Salary data, interview prep, resume tips, and role comparisons.</p>

            <div style="display: grid; gap: 1rem; margin-bottom: 2.5rem;">
{cards}
            </div>

            {related}

            {get_cta_box()}
        </section>
'''

    breadcrumb = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": "Career", "item": f"{BASE_URL}/career/"}
        ]
    }, indent=2)

    extra_head = f'<script type="application/ld+json">\n{breadcrumb}\n    </script>'

    html = get_html_head(
        title="FDE Career Guides and Resources",
        description="Forward Deployed Engineer career guides: how to become an FDE, interview prep, resume tips, salary data, and role comparisons across 50+ companies.",
        canonical_path="/career/",
        extra_head=extra_head
    )
    html += f'''
<body>
{get_header_html()}
    <main>
{body}
    </main>
{get_footer_html()}
{get_mobile_nav_js()}
{get_signup_js()}
</body>
</html>'''

    os.makedirs(os.path.join(SITE_DIR, 'career'), exist_ok=True)
    output_path = os.path.join(SITE_DIR, 'career', 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  Career index generated: {output_path}")


if __name__ == "__main__":
    generate_career_index()
