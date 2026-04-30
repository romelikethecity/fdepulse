#!/usr/bin/env python3
"""Generate the Insights landing page for FDE Pulse."""

import os
import sys
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from nav_config import SITE_NAME, BASE_URL
from templates import (
    get_html_head, get_header_html, get_footer_html,
    get_mobile_nav_js, get_signup_js, get_cta_box, get_article_schema
)

SITE_DIR = os.path.join(os.path.dirname(script_dir), 'site')

FAQS = [
    {
        "q": "How fast is the Forward Deployed Engineer job market growing?",
        "a": "FDE job postings grew 800% in 2025 according to FDE Pulse tracking data. The growth is driven by AI company expansion (OpenAI, Anthropic, Cohere), enterprise platform adoption (Salesforce Agentforce committing to 1,000 FDEs), and the broader realization that enterprise AI requires customer-embedded engineers for successful deployment. LinkedIn now shows 136,000+ results for 'forward deployed engineer' in the US alone."
    },
    {
        "q": "Is the FDE role a fad or a lasting career?",
        "a": "The FDE role addresses a structural problem in enterprise software: AI products require more customization than traditional SaaS. As long as enterprise AI deployments need human engineers to integrate, customize, and maintain, FDEs will be in demand. Palantir has employed FDEs for over a decade, proving the model's durability. The risk isn't that the role disappears, but that the title gets absorbed into existing functions like solutions engineering or customer engineering at companies that don't adopt Palantir's terminology."
    },
    {
        "q": "What skills are most in-demand for FDEs in 2026?",
        "a": "Python and TypeScript remain the most requested languages in FDE job postings. Beyond coding, the highest-signal skills in 2026 are: LLM integration and prompt engineering (requested in 45% of AI-company FDE postings), data pipeline architecture (Spark, dbt, Airflow), API design and system integration, and Kubernetes/cloud infrastructure. Soft skills matter equally: customer communication, technical writing, and the ability to translate business problems into engineering solutions separate strong FDE candidates from pure backend engineers."
    },
    {
        "q": "Which industries are hiring the most FDEs?",
        "a": "AI/ML companies lead FDE hiring with approximately 35% of all postings. Enterprise SaaS follows at 25%, driven by Salesforce's massive Agentforce expansion. Healthcare technology (Commure, Olive AI) and financial services (Ramp, Stripe) each account for 10-12% of FDE postings. Climate tech (Watershed), defense/government (Palantir, Anduril), and developer tools (PostHog, LaunchDarkly) make up the remainder. The fastest-growing segment is healthcare, where AI regulatory requirements create strong demand for customer-embedded engineers."
    },
    {
        "q": "How does FDE Pulse collect market intelligence?",
        "a": "FDE Pulse tracks 500,000+ job postings weekly across Indeed, LinkedIn, Greenhouse, Lever, and direct company career pages. We monitor search terms including 'Forward Deployed Engineer,' 'Forward Deployed Software Engineer,' 'Customer Engineer,' and 'Field Engineer.' Data is normalized for salary, seniority, location, and company metadata. Market intelligence reports are generated weekly and delivered through the FDE Pulse Brief newsletter."
    },
]


def generate_insights_page():
    print("  Generating insights page...")

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
            <h1 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">FDE Market Insights</h1>
            <div style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 1.5rem;">By <a href="https://www.linkedin.com/in/romethorndike/" target="_blank" rel="noopener" style="color: var(--amber); text-decoration: none;">Rome Thorndike</a></div>
            <p style="font-size: 1.15rem; color: var(--text-secondary); margin-bottom: 2.5rem; line-height: 1.7;">Market intelligence on the Forward Deployed Engineer role. Hiring trends, salary movements, skill demand, and industry analysis.</p>

            <div style="color: var(--text-secondary); font-size: 1.05rem; line-height: 1.8;">
                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 0 0 1rem;">The State of FDE Hiring: April 2026</h2>

                <p style="margin-bottom: 1.25rem;">The Forward Deployed Engineer market is in its third straight quarter of growth. FDE Pulse tracks 154+ active postings across 50+ companies, up from fewer than 20 postings a year ago. The role has moved from niche Palantir terminology to an established engineering function at AI companies, enterprise SaaS platforms, and consulting firms.</p>

                <p style="margin-bottom: 1.25rem;">Three trends define the current market:</p>

                <h3 style="font-size: 1.25rem; font-weight: 600; color: var(--text-primary); margin: 2rem 0 0.75rem;">1. AI Companies Are the Primary Demand Driver</h3>

                <p style="margin-bottom: 1.25rem;">OpenAI, Anthropic, Cohere, Databricks, and Scale AI collectively account for approximately 35% of all FDE job postings. The pattern is consistent: AI companies build powerful models, enterprise customers want to deploy those models, and FDEs bridge the gap between a general-purpose model and a customer-specific production system.</p>

                <p style="margin-bottom: 1.25rem;">The technical requirements for AI-company FDEs are shifting. Early FDE roles focused on data integration and pipeline work. Current postings increasingly require LLM-specific skills: prompt engineering, retrieval-augmented generation (RAG) architecture, model evaluation, and AI safety/guardrail implementation. This specialization will likely accelerate as AI products become more complex.</p>

                <h3 style="font-size: 1.25rem; font-weight: 600; color: var(--text-primary); margin: 2rem 0 0.75rem;">2. Salesforce's Agentforce Is a Watershed Moment</h3>

                <p style="margin-bottom: 1.25rem;">Salesforce's commitment to hiring 1,000 FDEs for their Agentforce AI platform is the single largest FDE hiring initiative in history. It validates the model at a scale that smaller companies can't match. When Salesforce structures their AI go-to-market around Forward Deployed Engineers, every enterprise software CEO notices.</p>

                <p style="margin-bottom: 1.25rem;">The Agentforce FDE program also legitimizes the FDE career path within large enterprise organizations. Salesforce offers structured career progression, competitive compensation ($170,000-$240,000 base), and the training infrastructure that comes with a 70,000-person company. For engineers who want FDE work without startup risk, Salesforce is becoming the default choice.</p>

                <h3 style="font-size: 1.25rem; font-weight: 600; color: var(--text-primary); margin: 2rem 0 0.75rem;">3. The Title Is Spreading Beyond Tech</h3>

                <p style="margin-bottom: 1.25rem;">PwC, Deloitte, and Accenture now use FDE-equivalent titles for client-facing technology deployment roles. Healthcare companies (Commure, Olive AI) hire FDEs to deploy clinical AI systems inside hospital networks. Defense contractors (Anduril, alongside Palantir) hire FDEs for military and intelligence deployments. Climate tech companies (Watershed) hire FDEs to deploy emissions measurement platforms.</p>

                <p style="margin-bottom: 1.25rem;">This cross-industry expansion means the FDE career path isn't tied to any single sector. Engineers can move between AI, healthcare, fintech, and climate tech without changing their core skill set. That versatility is rare in software engineering, where most specializations are industry-specific.</p>

                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Skills in Demand</h2>

                <p style="margin-bottom: 1.25rem;">FDE Pulse analyzes job descriptions to track which skills appear most frequently in FDE postings. The current top 10:</p>

                <ol style="margin-bottom: 1.25rem; padding-left: 1.5rem;">
                    <li style="margin-bottom: 0.4rem;"><strong style="color: var(--text-primary);">Python</strong> (78% of postings)</li>
                    <li style="margin-bottom: 0.4rem;"><strong style="color: var(--text-primary);">SQL</strong> (65%)</li>
                    <li style="margin-bottom: 0.4rem;"><strong style="color: var(--text-primary);">TypeScript/JavaScript</strong> (52%)</li>
                    <li style="margin-bottom: 0.4rem;"><strong style="color: var(--text-primary);">API Design & Integration</strong> (48%)</li>
                    <li style="margin-bottom: 0.4rem;"><strong style="color: var(--text-primary);">LLM/AI Integration</strong> (45%)</li>
                    <li style="margin-bottom: 0.4rem;"><strong style="color: var(--text-primary);">AWS/GCP/Azure</strong> (42%)</li>
                    <li style="margin-bottom: 0.4rem;"><strong style="color: var(--text-primary);">Data Pipelines</strong> (38%)</li>
                    <li style="margin-bottom: 0.4rem;"><strong style="color: var(--text-primary);">Customer Communication</strong> (35%)</li>
                    <li style="margin-bottom: 0.4rem;"><strong style="color: var(--text-primary);">Kubernetes/Docker</strong> (32%)</li>
                    <li style="margin-bottom: 0.4rem;"><strong style="color: var(--text-primary);">Technical Writing</strong> (28%)</li>
                </ol>

                <p style="margin-bottom: 1.25rem;">The biggest year-over-year change is LLM/AI integration moving from unmentioned to the #5 most-requested skill. A year ago, FDE roles focused on traditional software engineering. Today, nearly half of postings want experience deploying large language models in production environments.</p>

                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">What to Watch</h2>

                <p style="margin-bottom: 1.25rem;">Three things FDE Pulse is tracking for Q2 2026:</p>

                <p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Salesforce Agentforce hiring velocity.</strong> They announced 1,000 FDEs. How fast are they actually hiring? The ramp rate will signal whether other enterprise companies follow suit or if the commitment was aspirational.</p>

                <p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Title consolidation.</strong> "Forward Deployed Engineer," "Customer Engineer," "Solutions Engineer," and "Field Engineer" all describe overlapping roles. Whether the market converges on a single title or fragments further will shape how FDEs build career identity and compensation benchmarks.</p>

                <p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Remote vs. on-site split.</strong> Currently 62% of FDE postings offer remote or hybrid work. If that number drops below 50%, it signals that companies are pulling FDEs back to customer sites, which changes the value proposition for engineers who chose the role partly for location flexibility.</p>

                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Frequently Asked Questions</h2>

                {faq_html}
            </div>

            {get_cta_box()}
        </section>
'''

    faq_schema = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_items}, indent=2)
    breadcrumb = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL},
        {"@type": "ListItem", "position": 2, "name": "Insights", "item": f"{BASE_URL}/insights/"}
    ]}, indent=2)

    article = get_article_schema("FDE Market Insights & Hiring Trends", "Forward Deployed Engineer market intelligence. Hiring trends, salary movements, in-demand skills, and industry analysis.", "/insights/", "2026-04-10")
    extra_head = f'<script type="application/ld+json">\n{faq_schema}\n    </script>\n    <script type="application/ld+json">\n{breadcrumb}\n    </script>\n    {article}'

    html = get_html_head(
        title="FDE Market Insights & Hiring Trends",
        description="Forward Deployed Engineer market intelligence. Hiring trends, salary movements, in-demand skills, and industry analysis. Updated weekly.",
        canonical_path="/insights/",
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

    os.makedirs(os.path.join(SITE_DIR, 'insights'), exist_ok=True)
    with open(os.path.join(SITE_DIR, 'insights', 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print("  Insights page generated")


if __name__ == "__main__":
    generate_insights_page()
