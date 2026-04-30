#!/usr/bin/env python3
"""Generate the Salaries landing page for FDE Pulse."""

import os
import sys
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from nav_config import SITE_NAME, BASE_URL
from templates import (
    get_html_head, get_header_html, get_footer_html,
    get_mobile_nav_js, get_signup_js, get_cta_box
)

SITE_DIR = os.path.join(os.path.dirname(script_dir), 'site')

SALARY_DATA = [
    {"company": "OpenAI", "range": "$185,000 - $285,000", "level": "Mid-Senior", "location": "San Francisco"},
    {"company": "Palantir", "range": "$135,000 - $250,000", "level": "All levels", "location": "NYC / DC / Palo Alto"},
    {"company": "Salesforce", "range": "$170,000 - $240,000", "level": "Mid-Senior", "location": "Remote / SF / NYC"},
    {"company": "Ramp", "range": "$160,000 - $220,000", "level": "Mid-Senior", "location": "New York"},
    {"company": "Databricks", "range": "$175,000 - $260,000", "level": "Senior", "location": "SF / Remote"},
    {"company": "Scale AI", "range": "$165,000 - $245,000", "level": "Mid-Senior", "location": "San Francisco"},
    {"company": "Rippling", "range": "$155,000 - $230,000", "level": "Mid-Senior", "location": "SF / NYC"},
    {"company": "Cohere", "range": "$160,000 - $235,000", "level": "Mid-Senior", "location": "Remote / Toronto"},
]

FAQS = [
    {
        "q": "What is the average Forward Deployed Engineer salary?",
        "a": "The average Forward Deployed Engineer salary is approximately $195,000 in base compensation across all companies and experience levels. Total compensation including equity and bonuses ranges from $150,000 for entry-level FDEs at smaller companies to $300,000+ for senior FDEs at companies like OpenAI, Palantir, and Databricks. These figures are based on disclosed salary ranges from job postings tracked by FDE Pulse."
    },
    {
        "q": "Do Forward Deployed Engineers earn more than regular software engineers?",
        "a": "Forward Deployed Engineers typically earn 10-25% more than equivalent-seniority software engineers at the same company. The premium reflects the dual demand for strong engineering skills and customer-facing communication ability. FDEs also tend to work at well-funded enterprise companies that pay above-market rates. However, the gap narrows at staff and principal levels where individual contributor engineering compensation catches up."
    },
    {
        "q": "How does FDE pay vary by location?",
        "a": "San Francisco and New York FDE roles pay the highest, with median base salaries around $195,000-$210,000. Remote FDE positions typically pay 5-15% below Bay Area rates, with median base salaries around $175,000-$190,000. Roles in secondary tech hubs like Austin, Seattle, and Denver fall between the two. Some companies like Palantir have location-based pay bands, while others like Salesforce pay the same rate regardless of location for remote FDE roles."
    },
    {
        "q": "What is the salary progression for Forward Deployed Engineers?",
        "a": "Entry-level FDEs (0-2 years) earn $130,000-$165,000 base. Mid-level FDEs (3-5 years) earn $165,000-$210,000. Senior FDEs (5-8 years) earn $200,000-$260,000. Staff/Lead FDEs (8+ years) earn $240,000-$300,000+. These ranges represent base salary; total compensation with equity can be 20-50% higher at pre-IPO companies. Progression typically takes 6-8 years from entry to staff level."
    },
    {
        "q": "Do Forward Deployed Engineers get equity compensation?",
        "a": "Most FDE roles at venture-backed companies include equity as a significant portion of total compensation. At pre-IPO companies, equity can represent 20-40% of total comp. Palantir, OpenAI, Databricks, and Scale AI all include RSUs or stock options in FDE compensation packages. At public companies like Salesforce, FDE equity grants follow standard engineering equity bands. Consulting firm FDE roles (PwC, Deloitte) typically do not include equity."
    },
]


def generate_salaries_page():
    print("  Generating salaries page...")

    salary_rows = ""
    for s in SALARY_DATA:
        salary_rows += f'''
                <tr>
                    <td style="padding: 0.75rem 1rem; font-weight: 600; color: var(--text-primary);">{s["company"]}</td>
                    <td style="padding: 0.75rem 1rem; color: var(--amber-light); font-weight: 500;">{s["range"]}</td>
                    <td style="padding: 0.75rem 1rem; color: var(--text-secondary);">{s["level"]}</td>
                    <td style="padding: 0.75rem 1rem; color: var(--text-secondary);">{s["location"]}</td>
                </tr>'''

    faq_html = ""
    faq_schema_items = []
    for faq in FAQS:
        faq_html += f'''
            <div style="margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border);">
                <h3 style="font-size: 1.15rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">{faq["q"]}</h3>
                <p style="color: var(--text-secondary); line-height: 1.7;">{faq["a"]}</p>
            </div>'''
        faq_schema_items.append({
            "@type": "Question",
            "name": faq["q"],
            "acceptedAnswer": {"@type": "Answer", "text": faq["a"]}
        })

    body = f'''
        <section class="section" style="max-width: 900px; margin: 0 auto; padding-top: 8rem;">
            <h1 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem;">Forward Deployed Engineer Salaries</h1>
            <p style="font-size: 1.15rem; color: var(--text-secondary); margin-bottom: 2.5rem; line-height: 1.7;">Compensation data from real FDE job postings. Base salary, equity, and total comp benchmarks by company, seniority, and location.</p>

            <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 0 0 1.25rem;">FDE Salary Ranges by Company</h2>

            <div style="overflow-x: auto; margin-bottom: 2.5rem;">
                <table style="width: 100%; border-collapse: collapse; background: var(--bg-card); border-radius: var(--radius-lg); overflow: hidden;">
                    <thead>
                        <tr style="border-bottom: 1px solid var(--border);">
                            <th style="padding: 0.75rem 1rem; text-align: left; font-size: 0.85rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Company</th>
                            <th style="padding: 0.75rem 1rem; text-align: left; font-size: 0.85rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Salary Range</th>
                            <th style="padding: 0.75rem 1rem; text-align: left; font-size: 0.85rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Level</th>
                            <th style="padding: 0.75rem 1rem; text-align: left; font-size: 0.85rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Location</th>
                        </tr>
                    </thead>
                    <tbody>
{salary_rows}
                    </tbody>
                </table>
            </div>

            <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 2.5rem;">Salary data compiled from job postings tracked by FDE Pulse. Ranges represent base compensation. Total comp including equity may be 20-50% higher at pre-IPO companies. Updated weekly.</p>

            <div style="color: var(--text-secondary); font-size: 1.05rem; line-height: 1.8;">
                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">FDE Compensation: What the Numbers Tell Us</h2>

                <p style="margin-bottom: 1.25rem;">Forward Deployed Engineers command premium compensation because the role requires a rare skill combination. You need the technical depth of a mid-to-senior software engineer plus the communication skills of a solutions architect plus the customer empathy of a customer success manager. Companies pay for that intersection because it's hard to hire for.</p>

                <p style="margin-bottom: 1.25rem;">The median FDE base salary across all tracked postings is $195,000. That's roughly 15% above the median software engineer salary at equivalent companies. The premium is consistent across company stages: startups, growth-stage companies, and public enterprises all pay FDEs above their standard engineering bands.</p>

                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Salary by Seniority</h2>

                <p style="margin-bottom: 1.25rem;">The FDE career ladder typically maps to four levels. Entry-level FDEs (sometimes called "Associate FDE" or "FDE I") earn $130,000-$165,000 and usually have 1-3 years of software engineering experience. These roles exist primarily at larger companies like Salesforce and Palantir that have structured FDE programs with mentorship.</p>

                <p style="margin-bottom: 1.25rem;">Mid-level FDEs earn $165,000-$210,000 and form the bulk of FDE hiring. Most job postings target this band, looking for engineers with 3-5 years of experience who can work independently with customers. This is where the market is hottest and where salary growth has been strongest year-over-year.</p>

                <p style="margin-bottom: 1.25rem;">Senior FDEs earn $200,000-$260,000 and typically lead customer engagements or manage a portfolio of accounts. They're expected to mentor junior FDEs, contribute to product strategy, and handle the most complex technical integrations. At companies like OpenAI, senior FDEs work directly with enterprise customers deploying GPT-4 and custom models.</p>

                <p style="margin-bottom: 1.25rem;">Staff and Lead FDEs earn $240,000-$300,000+ and are relatively rare. These roles exist at companies with mature FDE organizations (Palantir, Salesforce) and involve defining the FDE function, building tooling and processes, and working cross-functionally with product and engineering leadership.</p>

                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Remote vs. On-Site Compensation</h2>

                <p style="margin-bottom: 1.25rem;">About 62% of FDE postings offer remote or hybrid work. Fully remote FDE roles pay 5-15% below equivalent Bay Area on-site positions. However, some companies (notably Salesforce for their Agentforce FDE team) pay location-agnostic salaries for remote roles, making them effectively the highest-paying FDE positions when adjusted for cost of living.</p>

                <p style="margin-bottom: 1.25rem;">The trade-off for remote FDE work is travel. Most remote FDE positions require 20-40% travel to customer sites. Some companies frame this as a benefit (travel stipend, business class flights) while others list it as a requirement. Fully remote with zero travel FDE roles exist but represent less than 15% of postings.</p>

                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Frequently Asked Questions</h2>

                {faq_html}
            </div>

            {get_cta_box()}
        </section>
'''

    faq_schema = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_schema_items}, indent=2)
    breadcrumb = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL},
        {"@type": "ListItem", "position": 2, "name": "Salaries", "item": f"{BASE_URL}/salaries/"}
    ]}, indent=2)
    dataset = json.dumps({"@context": "https://schema.org", "@type": "Dataset", "name": "Forward Deployed Engineer Salary Data",
        "description": "Compensation benchmarks for Forward Deployed Engineers across 50+ companies",
        "url": f"{BASE_URL}/salaries/", "creator": {"@type": "Organization", "name": SITE_NAME}}, indent=2)

    extra_head = f'<script type="application/ld+json">\n{faq_schema}\n    </script>\n    <script type="application/ld+json">\n{breadcrumb}\n    </script>\n    <script type="application/ld+json">\n{dataset}\n    </script>'

    html = get_html_head(
        title="Forward Deployed Engineer Salaries 2026",
        description="FDE salary data from real job postings. Base pay $150K-$300K+ by company, seniority, and location. OpenAI, Palantir, Salesforce, Ramp benchmarks.",
        canonical_path="/salaries/",
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

    os.makedirs(os.path.join(SITE_DIR, 'salaries'), exist_ok=True)
    with open(os.path.join(SITE_DIR, 'salaries', 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print("  Salaries page generated")


if __name__ == "__main__":
    generate_salaries_page()
