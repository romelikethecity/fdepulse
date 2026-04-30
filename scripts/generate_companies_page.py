#!/usr/bin/env python3
"""Generate the Companies landing page for FDE Pulse."""

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

COMPANIES = [
    {"name": "OpenAI", "fde_count": "50+", "category": "AI / ML", "hq": "San Francisco", "note": "Largest dedicated FDE team in AI. FDEs deploy ChatGPT Enterprise and custom models for Fortune 500 customers."},
    {"name": "Salesforce", "fde_count": "1,000 (target)", "category": "Enterprise SaaS", "hq": "San Francisco", "note": "Committed to hiring 1,000 FDEs for their Agentforce AI platform. The largest single FDE hiring initiative in history."},
    {"name": "Palantir", "fde_count": "200+", "category": "Enterprise Analytics", "hq": "Denver", "note": "Pioneered the FDE role in the 2010s. FDEs are central to Palantir's go-to-market strategy across government and commercial."},
    {"name": "Ramp", "fde_count": "15-25", "category": "Fintech", "hq": "New York", "note": "FDEs build custom financial integrations for enterprise customers adopting Ramp's corporate card and expense platform."},
    {"name": "Databricks", "fde_count": "30+", "category": "Data / AI", "hq": "San Francisco", "note": "FDEs deploy Databricks' lakehouse and ML platform inside enterprise data teams. Heavy data engineering focus."},
    {"name": "Scale AI", "fde_count": "20+", "category": "AI / ML", "hq": "San Francisco", "note": "FDEs build custom data labeling and model evaluation pipelines for AI companies and government contracts."},
    {"name": "Rippling", "fde_count": "10-20", "category": "HR Tech", "hq": "San Francisco", "note": "FDEs handle complex enterprise implementations of Rippling's unified HR, IT, and finance platform."},
    {"name": "Cohere", "fde_count": "10-15", "category": "AI / ML", "hq": "Toronto", "note": "FDEs embed with enterprise customers deploying Cohere's LLMs for search, RAG, and document processing."},
    {"name": "ServiceNow", "fde_count": "20+", "category": "Enterprise SaaS", "hq": "Santa Clara", "note": "FDEs deploy AI-powered workflow automation for enterprise IT and customer service operations."},
    {"name": "PostHog", "fde_count": "5-10", "category": "Developer Tools", "hq": "Remote", "note": "Product-adjacent FDE model. Engineers split time between customer implementations and core product development."},
    {"name": "PwC", "fde_count": "50+", "category": "Consulting", "hq": "Global", "note": "FDE-equivalent roles within PwC's technology consulting practice, deploying AI and analytics platforms for enterprise clients."},
    {"name": "Watershed", "fde_count": "5-10", "category": "Climate Tech", "hq": "San Francisco", "note": "FDEs help enterprise customers measure and reduce their carbon emissions using Watershed's climate platform."},
]

FAQS = [
    {
        "q": "Which company has the most Forward Deployed Engineers?",
        "a": "Salesforce has committed to hiring 1,000 Forward Deployed Engineers for their Agentforce AI platform, making it the largest FDE hiring initiative. Currently, Palantir has the most established FDE program with 200+ FDEs built over a decade. OpenAI's 50-person FDE team is the largest among pure AI companies. PwC and other consulting firms employ FDE-equivalent roles at similar scale but under different titles."
    },
    {
        "q": "What types of companies hire Forward Deployed Engineers?",
        "a": "FDE hiring spans four main categories. AI/ML companies (OpenAI, Anthropic, Cohere, Databricks, Scale AI) hire FDEs to deploy models and AI products. Enterprise SaaS companies (Salesforce, ServiceNow, Rippling, UiPath) hire FDEs for complex platform implementations. Startups (PostHog, Watershed, Onyx, Commure) hire FDEs as product-adjacent engineers. Consulting firms (PwC, Deloitte) hire FDE-equivalent roles for client-facing technology deployment."
    },
    {
        "q": "Are startups or large companies better for FDE careers?",
        "a": "Startups offer broader scope: you'll touch more of the stack, work directly with founders, and have more influence on the product. Large companies offer structure: defined career ladders, mentorship, larger teams, and higher base compensation. AI startups like Cohere and PostHog are strong middle ground options. The best choice depends on whether you prioritize breadth of experience (startup) or depth of resources and compensation (enterprise)."
    },
    {
        "q": "Do consulting firms hire Forward Deployed Engineers?",
        "a": "Yes. PwC, Deloitte, and Accenture all hire for FDE-equivalent roles, though they may use titles like 'Technology Consultant,' 'Solutions Engineer,' or 'Implementation Engineer.' The work is similar: deploying technology platforms at client sites. Key differences from product-company FDEs: consulting FDEs work across multiple clients and technology stacks rather than a single product, and compensation typically doesn't include equity."
    },
    {
        "q": "Which companies pay Forward Deployed Engineers the most?",
        "a": "OpenAI pays the highest base salaries for FDEs, with ranges of $185,000-$285,000. Databricks ($175,000-$260,000), Palantir ($135,000-$250,000), and Scale AI ($165,000-$245,000) follow closely. However, total compensation including equity changes the ranking significantly. Pre-IPO companies like Databricks and Scale AI may offer higher total comp than public companies when equity appreciates. Salesforce offers strong equity grants as a public company with predictable RSU value."
    },
]


def generate_companies_page():
    print("  Generating companies page...")

    company_cards = ""
    for c in COMPANIES:
        company_cards += f'''
            <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 1.5rem; transition: all 250ms ease;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem;">
                    <h3 style="font-size: 1.15rem; font-weight: 600; color: var(--text-primary);">{c["name"]}</h3>
                    <span style="background: var(--bg-secondary); padding: 0.25rem 0.75rem; border-radius: var(--radius-full); font-size: 0.8rem; color: var(--amber-light); font-weight: 600; white-space: nowrap;">{c["fde_count"]} FDEs</span>
                </div>
                <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.5rem;">{c["category"]} &middot; {c["hq"]}</div>
                <p style="font-size: 0.95rem; color: var(--text-secondary); line-height: 1.6;">{c["note"]}</p>
            </div>'''

    faq_html = ""
    faq_items = []
    for faq in FAQS:
        faq_html += f'''
            <div style="margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border);">
                <h3 style="font-size: 1.15rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">{faq["q"]}</h3>
                <p style="color: var(--text-secondary); line-height: 1.7;">{faq["a"]}</p>
            </div>'''
        faq_items.append({"@type": "Question", "name": faq["q"], "acceptedAnswer": {"@type": "Answer", "text": faq["a"]}})

    body = f'''
        <section class="section" style="max-width: 900px; margin: 0 auto; padding-top: 8rem;">
            <h1 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem;">Companies Hiring Forward Deployed Engineers</h1>
            <p style="font-size: 1.15rem; color: var(--text-secondary); margin-bottom: 2.5rem; line-height: 1.7;">50+ companies now hire FDEs. Here are the biggest employers, what their FDE teams do, and how they're structured.</p>

            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 1rem; margin-bottom: 3rem;">
{company_cards}
            </div>

            <div style="color: var(--text-secondary); font-size: 1.05rem; line-height: 1.8;">
                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">The FDE Hiring Landscape</h2>

                <p style="margin-bottom: 1.25rem;">Three years ago, Palantir was one of the only companies with "Forward Deployed Engineer" in their job titles. Today, the role exists at 50+ companies across AI, enterprise SaaS, fintech, climate tech, healthcare, and consulting. The expansion accelerated in 2025 when AI companies realized they couldn't sell enterprise AI products the same way they sold traditional SaaS.</p>

                <p style="margin-bottom: 1.25rem;">AI products require deep customization. A hospital deploying an AI clinical decision support system needs different integrations, data pipelines, and compliance guardrails than a logistics company deploying an AI routing optimizer. FDEs bridge that gap: they sit with the customer, understand their technical environment, and make the product work in practice.</p>

                <p style="margin-bottom: 1.25rem;">Salesforce's 1,000-FDE hiring target for Agentforce validated the model at enterprise scale. When the world's largest enterprise software company restructures their go-to-market around Forward Deployed Engineers, it signals that the role isn't a niche experiment. It's becoming a standard function in enterprise software companies.</p>

                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">How FDE Teams Are Structured</h2>

                <p style="margin-bottom: 1.25rem;">FDE team structures vary by company maturity and size. Palantir runs the most structured program: FDEs are organized by vertical (government, healthcare, finance, energy) with dedicated mentors and career progression from FDSE to FDE to Lead FDE. New hires go through a multi-week deployment bootcamp before their first customer engagement.</p>

                <p style="margin-bottom: 1.25rem;">Startups tend to have flatter structures. At PostHog, FDEs are effectively product engineers who spend 40-60% of their time on customer-facing work. At Watershed, FDEs report to engineering leadership but are paired with specific customer accounts managed by customer success teams. There's no separate "FDE organization" at most companies under 500 employees.</p>

                <p style="margin-bottom: 1.25rem;">AI companies fall somewhere in between. OpenAI's 50-person FDE team has its own leadership and operates semi-independently from the research and product engineering organizations. They've built internal tooling specifically for customer deployments, and FDEs contribute to shared libraries that accelerate future customer onboarding.</p>

                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Frequently Asked Questions</h2>

                {faq_html}
            </div>

            {get_cta_box()}
        </section>
'''

    faq_schema = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_items}, indent=2)
    breadcrumb = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL},
        {"@type": "ListItem", "position": 2, "name": "Companies", "item": f"{BASE_URL}/companies/"}
    ]}, indent=2)

    extra_head = f'<script type="application/ld+json">\n{faq_schema}\n    </script>\n    <script type="application/ld+json">\n{breadcrumb}\n    </script>'

    html = get_html_head(
        title="Companies Hiring Forward Deployed Engineers",
        description="50+ companies hire FDEs: OpenAI, Salesforce, Palantir, Ramp, Databricks. Team sizes, structures, and what FDE teams do at each company.",
        canonical_path="/companies/",
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

    os.makedirs(os.path.join(SITE_DIR, 'companies'), exist_ok=True)
    with open(os.path.join(SITE_DIR, 'companies', 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print("  Companies page generated")


if __name__ == "__main__":
    generate_companies_page()
