#!/usr/bin/env python3
"""Generate the About page for FDE Pulse."""

import os
import sys
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from nav_config import BASE_URL
from templates import (
    get_html_head, get_header_html, get_footer_html,
    get_mobile_nav_js, get_signup_js, get_cta_box,
    get_scroll_cta, get_related_links
)

SITE_DIR = os.path.join(os.path.dirname(script_dir), 'site')


def generate_about():
    print("  Generating about page...")

    related = get_related_links([
        {"href": "/career/what-is-a-forward-deployed-engineer/", "label": "What Is a Forward Deployed Engineer?"},
        {"href": "/salaries/", "label": "FDE Salary Data"},
        {"href": "/companies/", "label": "Companies Hiring FDEs"},
        {"href": "/jobs/", "label": "Browse FDE Jobs"},
        {"href": "/insights/", "label": "Market Insights"},
    ])

    body = f'''
        <section class="section" style="max-width: 800px; margin: 0 auto; padding-top: 8rem;">
            <h1 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1.5rem;">About FDE Pulse</h1>

            <div style="color: var(--text-secondary); font-size: 1.05rem; line-height: 1.8;">
                <p style="margin-bottom: 1.25rem;">FDE Pulse is the first dedicated job board and market intelligence platform for Forward Deployed Engineers.</p>

                <p style="margin-bottom: 1.25rem;">The Forward Deployed Engineer role grew 800% in 2025. Companies like OpenAI, Salesforce, Palantir, Ramp, Databricks, and 50+ others are hiring FDEs to bridge the gap between product and customer. But there was no single place to track the market.</p>

                <p style="margin-bottom: 1.25rem;">FDE Pulse fills that gap. We track every FDE job posting across major boards, aggregate salary data, and publish weekly market intelligence. Whether you're an engineer considering the FDE path, a hiring manager benchmarking comp, or a recruiter sourcing candidates, FDE Pulse gives you the data you need to make informed decisions.</p>

                <p style="margin-bottom: 1.25rem;">The Forward Deployed Engineer sits at the intersection of software engineering and customer success. FDEs write production code, but they do it at customer sites, solving customer-specific problems. The role requires strong technical skills plus the communication ability to work directly with enterprise customers. Salaries range from $150,000 to $300,000+ depending on company and seniority, making it one of the highest-paying engineering specializations outside of Staff-level SWE roles at FAANG companies.</p>

                <h2 style="font-size: 1.5rem; font-weight: 700; color: var(--text-primary); margin: 2rem 0 1rem;">What We Track</h2>

                <p style="margin-bottom: 1.25rem;">FDE Pulse monitors job postings across Indeed, LinkedIn, Greenhouse, Lever, and company career pages. We collect and normalize data from 500,000+ postings to identify every Forward Deployed Engineer opportunity in the market. Here is what we track:</p>

                <ul style="margin-bottom: 1.25rem; padding-left: 1.5rem;">
                    <li style="margin-bottom: 0.5rem;">Forward Deployed Engineer job postings across all major boards</li>
                    <li style="margin-bottom: 0.5rem;">Salary benchmarks by company, location, and seniority level</li>
                    <li style="margin-bottom: 0.5rem;">Company hiring trends, team sizes, and growth trajectories</li>
                    <li style="margin-bottom: 0.5rem;">Market signals: which industries are adopting the FDE model and why</li>
                    <li style="margin-bottom: 0.5rem;">Technical skill demand (Python, LLM integration, data engineering, cloud platforms)</li>
                    <li style="margin-bottom: 0.5rem;">Location trends: remote vs. on-site, city-level salary differences, international expansion</li>
                </ul>

                <h2 style="font-size: 1.5rem; font-weight: 700; color: var(--text-primary); margin: 2rem 0 1rem;">How Data Is Collected</h2>

                <p style="margin-bottom: 1.25rem;">Our data pipeline runs weekly. We scrape and parse job postings from major job boards, company career pages, and applicant tracking systems. Each posting is normalized into a common schema: title, company, location, salary range, seniority level, remote status, and required skills. Salary data is extracted from posted ranges where available and cross-referenced with reported compensation data. All data points go through validation before appearing on the site or in the FDE Pulse Brief newsletter.</p>

                <p style="margin-bottom: 1.25rem;">We track 50+ companies that hire Forward Deployed Engineers. Each company profile includes salary ranges, team sizes, tech stacks, interview processes, and culture details sourced from job postings, company announcements, and verified candidate reports. Company data is refreshed monthly.</p>

                <h2 style="font-size: 1.5rem; font-weight: 700; color: var(--text-primary); margin: 2rem 0 1rem;">Who Runs FDE Pulse</h2>

                <p style="margin-bottom: 1.25rem;">FDE Pulse is built by Provyx, a data intelligence company that operates specialized job market platforms across high-growth roles. We run similar platforms tracking fractional executives, CROs, RevOps leaders, and AI market roles. Our approach is the same across all platforms: collect better data than anyone else, present it clearly, and deliver insights that help people make career and hiring decisions.</p>

                <p style="margin-bottom: 1.25rem;">We're not recruiters and we don't sell candidate data. FDE Pulse is a market intelligence platform. We publish the data so engineers, hiring managers, and recruiters can make informed decisions without relying on anecdotes or outdated salary surveys.</p>

                <h2 style="font-size: 1.5rem; font-weight: 700; color: var(--text-primary); margin: 2rem 0 1rem;">Why Forward Deployed Engineers Specifically</h2>

                <p style="margin-bottom: 1.25rem;">The FDE role is one of the most important and least understood positions in enterprise software. It grew 800% in a single year but still doesn't have a Wikipedia page. Engineers considering the path can't find reliable salary data. Hiring managers building FDE teams don't have benchmarks for compensation or team structure. Recruiters sourcing FDE candidates don't know which companies are hiring or what they pay.</p>

                <p style="margin-bottom: 1.25rem;">FDE Pulse exists because this information gap creates real problems. Engineers accept below-market offers because they don't know what FDEs earn at competing companies. Hiring managers lose candidates because their job descriptions don't match what FDEs are actually looking for. Recruiters waste time pitching roles that don't match candidate expectations. Better data fixes all of these problems.</p>

                <h2 style="font-size: 1.5rem; font-weight: 700; color: var(--text-primary); margin: 2rem 0 1rem;">What You'll Find on FDE Pulse</h2>

                <p style="margin-bottom: 1.25rem;">FDE Pulse publishes detailed profiles for every major company hiring Forward Deployed Engineers. Each profile covers salary ranges, interview processes, tech stacks, team sizes, and culture. We currently cover 15+ companies in depth, from Palantir (the company that invented the FDE role) to OpenAI, Anthropic, Salesforce, Databricks, Ramp, and others. New profiles are added as companies start FDE hiring programs.</p>

                <p style="margin-bottom: 1.25rem;">Our career section includes guides on how to become an FDE, interview preparation with 50+ real questions reported by candidates, resume templates, and specialized guides for AI-focused FDE roles, FDE career levels and promotion timelines, and work-life balance considerations. The comparison pages break down FDE versus related roles: Solutions Engineer, Software Engineer, Consultant, Sales Engineer, Customer Engineer, and Product Manager.</p>

                <p style="margin-bottom: 1.25rem;">Location pages cover the major FDE job markets: San Francisco, New York, London, Toronto, Seattle, Austin, India, and Europe. Each page includes local salary data, companies hiring in that location, and market-specific advice for candidates.</p>

                <h2 style="font-size: 1.5rem; font-weight: 700; color: var(--text-primary); margin: 2rem 0 1rem;">The FDE Pulse Brief</h2>

                <p style="margin-bottom: 1.25rem;">Our free weekly newsletter delivers the most important FDE market data to your inbox. New job postings, salary movements, company announcements, and career insights. No fluff. Each issue takes 5 minutes to read and covers what changed in the FDE market that week.</p>

                <p style="margin-bottom: 1.25rem;">Subscribers get salary benchmarks, hiring trend analysis, and new postings before they appear on aggregator sites. The Brief is the fastest way to stay current on the FDE job market without spending hours browsing job boards.</p>

                <h2 style="font-size: 1.5rem; font-weight: 700; color: var(--text-primary); margin: 2rem 0 1rem;">Frequently Asked Questions</h2>

                <div style="margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border);">
                    <h3 style="font-size: 1.15rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">How often is FDE Pulse data updated?</h3>
                    <p style="color: var(--text-secondary); line-height: 1.7;">Job posting data is refreshed weekly. Company profiles and salary benchmarks are updated monthly. The FDE Pulse Brief newsletter goes out every week with the latest market changes. Major market events (like Salesforce's 1,000-FDE announcement) are covered as they happen.</p>
                </div>

                <div style="margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border);">
                    <h3 style="font-size: 1.15rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">Is FDE Pulse free?</h3>
                    <p style="color: var(--text-secondary); line-height: 1.7;">Yes. All content on FDE Pulse is free, including the weekly newsletter. We believe market transparency benefits everyone: engineers make better career decisions, companies attract better candidates, and the FDE ecosystem grows faster when information flows freely.</p>
                </div>

                <div style="margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border);">
                    <h3 style="font-size: 1.15rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">How does FDE Pulse make money?</h3>
                    <p style="color: var(--text-secondary); line-height: 1.7;">We plan to offer premium job posting features for companies hiring FDEs and sponsored placements in the newsletter. All editorial content and salary data remain independent of any commercial relationships.</p>
                </div>

                <div style="margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border);">
                    <h3 style="font-size: 1.15rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">Can I submit a correction or update?</h3>
                    <p style="color: var(--text-secondary); line-height: 1.7;">Yes. If you notice incorrect salary data, outdated company information, or missing FDE-hiring companies, email us at hello@fdepulse.com. We verify all submissions before publishing updates. Corrections from current or former FDEs are particularly valuable.</p>
                </div>

                <div style="margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border);">
                    <h3 style="font-size: 1.15rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">Does FDE Pulse sell my data if I subscribe?</h3>
                    <p style="color: var(--text-secondary); line-height: 1.7;">No. We don't sell subscriber email addresses or personal data to anyone. Your email is used only to send the FDE Pulse Brief newsletter. You can unsubscribe at any time.</p>
                </div>
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
            {"@type": "ListItem", "position": 2, "name": "About", "item": f"{BASE_URL}/about/"}
        ]
    }, indent=2)

    faq_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": "How often is FDE Pulse data updated?", "acceptedAnswer": {"@type": "Answer", "text": "Job posting data is refreshed weekly. Company profiles and salary benchmarks are updated monthly. The FDE Pulse Brief newsletter goes out every week with the latest market changes."}},
            {"@type": "Question", "name": "Is FDE Pulse free?", "acceptedAnswer": {"@type": "Answer", "text": "Yes. All content on FDE Pulse is free, including the weekly newsletter."}},
            {"@type": "Question", "name": "How does FDE Pulse make money?", "acceptedAnswer": {"@type": "Answer", "text": "We plan to offer premium job posting features for companies hiring FDEs and sponsored placements in the newsletter."}},
            {"@type": "Question", "name": "Can I submit a correction or update?", "acceptedAnswer": {"@type": "Answer", "text": "Yes. Email hello@fdepulse.com with corrections. We verify all submissions before publishing."}},
            {"@type": "Question", "name": "Does FDE Pulse sell my data if I subscribe?", "acceptedAnswer": {"@type": "Answer", "text": "No. We don't sell subscriber email addresses or personal data to anyone."}},
        ]
    }, indent=2)

    extra_head = f'<script type="application/ld+json">\n{breadcrumb}\n    </script>\n    <script type="application/ld+json">\n{faq_schema}\n    </script>'

    # Manually assemble HTML like homepage does, so signup JS and scroll CTA are included
    html = get_html_head(
        title="About FDE Pulse",
        description="FDE Pulse tracks Forward Deployed Engineer jobs, salaries, and market trends across 50+ companies. The first dedicated FDE career platform.",
        canonical_path="/about/",
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
{get_scroll_cta()}
</body>
</html>'''

    os.makedirs(os.path.join(SITE_DIR, 'about'), exist_ok=True)
    output_path = os.path.join(SITE_DIR, 'about', 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  About page generated: {output_path}")


if __name__ == "__main__":
    generate_about()
