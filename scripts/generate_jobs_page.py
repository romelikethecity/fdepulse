#!/usr/bin/env python3
"""Generate the Jobs landing page for FDE Pulse with real job listings."""

import os
import sys
import json
import re
import hashlib
from datetime import datetime, date

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from nav_config import SITE_NAME, BASE_URL
from templates import (
    get_html_head, get_header_html, get_footer_html,
    get_mobile_nav_js, get_signup_js, get_cta_box
)

SITE_DIR = os.path.join(os.path.dirname(script_dir), 'site')
DATA_DIR = os.path.join(os.path.dirname(script_dir), 'data')

FAQS = [
    {
        "q": "What does a Forward Deployed Engineer do?",
        "a": "A Forward Deployed Engineer (FDE) is embedded directly with customers to build custom integrations, solve technical problems, and bridge the gap between product engineering and customer success. FDEs write production code, architect solutions specific to a customer's infrastructure, and translate customer feedback into product improvements. The role combines deep software engineering skills with strong communication and business acumen."
    },
    {
        "q": "How much do Forward Deployed Engineers make?",
        "a": "Forward Deployed Engineer salaries range from $150,000 to $300,000+ depending on company, location, and seniority. At companies like OpenAI and Palantir, senior FDEs can earn $250,000-$300,000+ in total compensation including equity. The median base salary across all FDE postings is approximately $195,000. Remote FDE roles typically pay 5-15% less than equivalent Bay Area positions."
    },
    {
        "q": "Which companies hire Forward Deployed Engineers?",
        "a": "Over 50 companies now hire Forward Deployed Engineers. Major employers include OpenAI (50-person FDE team), Salesforce (committed to hiring 1,000 FDEs), Palantir (pioneered the role), Ramp, Rippling, Databricks, Scale AI, Cohere, ServiceNow, UiPath, PostHog, and Watershed. Consulting firms like PwC and Deloitte also hire for FDE-equivalent roles."
    },
    {
        "q": "What skills do you need to become a Forward Deployed Engineer?",
        "a": "FDEs need strong full-stack software engineering skills (Python, TypeScript, SQL are most common), experience with APIs and system integration, comfort working directly with customers, and the ability to context-switch between different technical environments. Most FDE roles require 3-7 years of software engineering experience. Data engineering and ML/AI skills are increasingly valued as more AI companies adopt the FDE model."
    },
    {
        "q": "Is Forward Deployed Engineer a good career path?",
        "a": "Forward Deployed Engineering is one of the fastest-growing roles in enterprise software, with job postings growing 800% in 2025. FDEs develop a rare combination of technical depth and business context that opens paths to engineering management, solutions architecture, product management, customer engineering leadership, or founding a startup. The role's customer proximity gives FDEs insights that pure backend engineers rarely get."
    },
]

JOB_BOARD_CSS = """
/* Job Board Specific Styles */
.page-header {
    padding: 8rem 0 3rem;
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border);
}
.page-header__inner {
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 var(--space-lg);
}
.page-header__title {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: var(--space-sm);
}
.page-header__subtitle {
    color: var(--text-secondary);
    font-size: 1.1rem;
}

/* Stats bar */
.job-stats-bar {
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border);
    padding: 1rem var(--space-lg);
}
.job-stats-bar__inner {
    max-width: 1100px;
    margin: 0 auto;
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
    align-items: center;
}
.job-stat-item {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.9rem;
    color: var(--text-secondary);
}
.job-stat-item strong {
    color: var(--amber-light);
    font-weight: 600;
}

/* Job list layout */
.jobs-list {
    max-width: 1100px;
    margin: 0 auto;
    padding: var(--space-xl) var(--space-lg);
}
.jobs-list__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--space-lg);
    flex-wrap: wrap;
    gap: var(--space-sm);
}
.jobs-list__count {
    color: var(--text-secondary);
    font-size: 0.95rem;
}

/* Job card (list row style) */
.job-item {
    display: block;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    margin-bottom: var(--space-md);
    transition: all var(--transition-fast);
    text-decoration: none;
}
.job-item:hover {
    background: var(--bg-card-hover);
    border-color: var(--amber);
    transform: translateY(-1px);
    box-shadow: var(--shadow-glow);
}
.job-item__header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: var(--space-md);
    gap: var(--space-md);
}
.job-item__left { flex: 1; min-width: 0; }
.job-item__company {
    font-size: 0.875rem;
    color: var(--amber-light);
    font-weight: 500;
    margin-bottom: 0.25rem;
}
.job-item__title {
    font-size: 1.15rem;
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1.3;
}
.job-item__salary {
    background: rgba(74, 222, 128, 0.1);
    border: 1px solid rgba(74, 222, 128, 0.25);
    padding: 0.3rem 0.75rem;
    border-radius: var(--radius-full);
    font-size: 0.875rem;
    font-weight: 600;
    color: #4ade80;
    white-space: nowrap;
    flex-shrink: 0;
}
.job-item__meta {
    display: flex;
    gap: var(--space-sm);
    flex-wrap: wrap;
    align-items: center;
}
.job-item__tag {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 10px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: var(--radius-full);
    font-size: 0.8rem;
    color: var(--text-muted);
}
.job-item__tag--remote {
    background: rgba(74, 222, 128, 0.12);
    color: var(--success);
    font-weight: 500;
}
.job-item__tag--seniority {
    background: rgba(245, 158, 11, 0.12);
    color: var(--amber-light);
}
.job-item__cta {
    margin-left: auto;
    font-size: 0.85rem;
    color: var(--amber-light);
    font-weight: 500;
    white-space: nowrap;
}
.job-item__date {
    font-size: 0.8rem;
    color: var(--text-muted);
}

/* Prose content below listings */
.jobs-prose {
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 var(--space-lg) var(--space-3xl);
    color: var(--text-secondary);
    font-size: 1.05rem;
    line-height: 1.8;
}
.jobs-prose h2 {
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 2.5rem 0 1rem;
}
.jobs-prose p { margin-bottom: 1.25rem; }
.jobs-prose ul { margin-bottom: 1.25rem; padding-left: 1.5rem; }
.jobs-prose li { margin-bottom: 0.5rem; }
.jobs-prose strong { color: var(--text-primary); }

@media (max-width: 768px) {
    .page-header { padding: 6rem 0 2rem; }
    .page-header__title { font-size: 2rem; }
    .job-item__header { flex-direction: column; }
    .job-item__salary { align-self: flex-start; }
    .job-stats-bar__inner { gap: 1rem; }
}
"""


def escape_html(text):
    if not text:
        return ''
    return str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def make_slug(company, title, source_url):
    text = company + '-' + title
    base = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')[:80]
    hash_input = source_url or (company + title)
    hash6 = hashlib.md5(hash_input.encode()).hexdigest()[:6]
    return base + '-' + hash6


def format_salary(min_amt, max_amt):
    """Format salary as '$165K - $250K'."""
    if not min_amt or not max_amt or min_amt <= 0 or max_amt <= 0:
        return None
    min_k = int(round(min_amt / 1000))
    max_k = int(round(max_amt / 1000))
    return f'${min_k}K - ${max_k}K'


def format_date_short(date_str):
    if not date_str:
        return ''
    try:
        dt = datetime.strptime(date_str[:10], '%Y-%m-%d')
        return dt.strftime('%b %d')
    except Exception:
        return date_str


def generate_jobs_page():
    print("  Generating jobs page...")

    jobs_file = os.path.join(DATA_DIR, 'jobs.json')
    if not os.path.exists(jobs_file):
        print(f"  ERROR: {jobs_file} not found")
        return

    with open(jobs_file, encoding='utf-8') as f:
        data = json.load(f)

    jobs = data.get('jobs', [])
    total_jobs = len(jobs)
    remote_count = sum(1 for j in jobs if j.get('is_remote'))
    with_salary = sum(1 for j in jobs if (j.get('min_amount') or 0) > 0 and (j.get('max_amount') or 0) > 0)
    pct_remote = int(round(100 * remote_count / total_jobs)) if total_jobs else 0

    # Salary range across all jobs with salary
    sal_mins = [j['min_amount'] for j in jobs if (j.get('min_amount') or 0) > 0]
    sal_maxs = [j['max_amount'] for j in jobs if (j.get('max_amount') or 0) > 0]
    global_min_k = int(round(min(sal_mins) / 1000)) if sal_mins else 0
    global_max_k = int(round(max(sal_maxs) / 1000)) if sal_maxs else 0

    # Stats bar
    stats_bar = f'''
    <div class="job-stats-bar">
        <div class="job-stats-bar__inner">
            <span class="job-stat-item"><strong>{total_jobs}</strong> FDE roles tracked</span>
            <span class="job-stat-item"><strong>{pct_remote}%</strong> remote-eligible</span>
            <span class="job-stat-item"><strong>${global_min_k}K&ndash;${global_max_k}K</strong> salary range</span>
            <span class="job-stat-item"><strong>{with_salary}</strong> with salary disclosed</span>
        </div>
    </div>'''

    # Job cards
    job_cards_html = ""
    for job in jobs:
        company = escape_html(job.get('company', 'Confidential'))
        title = escape_html(job.get('title', 'Forward Deployed Engineer'))
        location = job.get('location', '')
        is_remote = job.get('is_remote', False)
        seniority = job.get('seniority', '')
        date_posted = format_date_short(job.get('date_posted', ''))
        source_url = job.get('source_url', '')
        slug = make_slug(job.get('company', ''), job.get('title', ''), source_url)

        salary_html = ''
        sal_fmt = format_salary(job.get('min_amount', 0), job.get('max_amount', 0))
        if sal_fmt:
            salary_html = f'<span class="job-item__salary">{sal_fmt}</span>'

        # Meta tags
        meta_parts = []
        if is_remote:
            meta_parts.append('<span class="job-item__tag job-item__tag--remote">Remote</span>')
        elif location:
            meta_parts.append(f'<span class="job-item__tag">{escape_html(location)}</span>')

        if seniority:
            meta_parts.append(f'<span class="job-item__tag job-item__tag--seniority">{escape_html(seniority)}</span>')

        if date_posted:
            meta_parts.append(f'<span class="job-item__date">{date_posted}</span>')

        meta_parts.append('<span class="job-item__cta">View role &rarr;</span>')

        meta_html = '\n                    '.join(meta_parts)

        job_cards_html += f'''
        <a href="/jobs/{slug}/" class="job-item">
            <div class="job-item__header">
                <div class="job-item__left">
                    <div class="job-item__company">{company}</div>
                    <div class="job-item__title">{title}</div>
                </div>
                {salary_html}
            </div>
            <div class="job-item__meta">
                {meta_html}
            </div>
        </a>'''

    # FAQ section
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
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["a"]
            }
        })

    body = f'''
{stats_bar}

        <div class="page-header">
            <div class="page-header__inner">
                <h1 class="page-header__title">Forward Deployed Engineer Jobs</h1>
                <p class="page-header__subtitle">{total_jobs} FDE roles tracked across major job boards. Updated weekly.</p>
            </div>
        </div>

        <div class="jobs-list">
            <div class="jobs-list__header">
                <span class="jobs-list__count">{total_jobs} jobs found</span>
            </div>
            <div class="jobs-list__items">
                {job_cards_html}
            </div>
        </div>

        <div class="jobs-prose">
            <h2>The FDE Job Market in 2026</h2>

            <p>Forward Deployed Engineer hiring grew 800% in 2025. That growth hasn't slowed. Salesforce alone committed to hiring 1,000 FDEs. OpenAI runs a 50-person FDE team. Ramp, Rippling, Databricks, and dozens of startups are building FDE organizations from scratch.</p>

            <p>The role didn't exist at most companies three years ago. Palantir pioneered it in the 2010s as a way to deploy their analytics platform inside government agencies and Fortune 500 companies. The model worked: customers got custom solutions, product teams got direct feedback loops, and Palantir built one of the stickiest enterprise software businesses in history.</p>

            <p>Now every enterprise AI company is copying the playbook. AI products require more customization than traditional SaaS. You can't ship a one-size-fits-all AI agent to a hospital system and a logistics company and expect the same results. Someone has to sit with the customer, understand their data, build the integrations, and make the product work in their specific environment. That's the FDE.</p>

            <h2>Types of FDE Roles</h2>

            <p>Not all Forward Deployed Engineer positions are identical. The title spans several distinct flavors depending on the company and their customer base:</p>

            <p><strong>Customer-Embedded FDEs</strong> work on-site or virtually embedded with a single customer for weeks or months at a time. This is the original Palantir model. You become an extension of the customer's engineering team, building solutions on top of the company's platform that solve that customer's specific problems.</p>

            <p><strong>Integration FDEs</strong> focus on technical implementation and data pipeline work. They connect the product to the customer's existing infrastructure: EHR systems at hospitals, ERP platforms at manufacturers, trading systems at financial firms. These roles lean more data engineering than full-stack.</p>

            <p><strong>Product-Adjacent FDEs</strong> split time between customer work and product development. They build customer-specific solutions but also contribute features and improvements back to the core product. Companies like PostHog and Ramp use this model, where FDEs are effectively product engineers with a customer-facing mandate.</p>

            <p><strong>Pre-Sales FDEs</strong> focus on technical proof-of-concepts and pilot deployments. They work with prospects rather than existing customers, building custom demos and integrations that close deals. Compensation for these roles often includes commission or deal-based bonuses.</p>

            <h2>What FDE Pulse Tracks</h2>

            <p>FDE Pulse monitors job postings across Indeed, LinkedIn, Greenhouse, Lever, and company career pages. We track:</p>

            <ul>
                <li>Job title, company, location, and remote status</li>
                <li>Salary ranges (when disclosed) normalized to annual compensation</li>
                <li>Seniority level and required experience</li>
                <li>Technical skills mentioned in job descriptions</li>
                <li>Company stage, size, and industry vertical</li>
                <li>Posting frequency and hiring velocity per company</li>
            </ul>

            <p>All data feeds into weekly market intelligence reports delivered through the FDE Pulse Brief newsletter. Subscribers get salary benchmarks, hiring trend analysis, and new postings before they hit the aggregators.</p>

            <h2>Frequently Asked Questions</h2>

            {faq_html}

            {get_cta_box()}
        </div>
'''

    faq_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_schema_items
    }, indent=2)

    breadcrumb_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": "Jobs", "item": f"{BASE_URL}/jobs/"}
        ]
    }, indent=2)

    extra_head = f'''<style>{JOB_BOARD_CSS}</style>
    <script type="application/ld+json">
{faq_schema}
    </script>
    <script type="application/ld+json">
{breadcrumb_schema}
    </script>'''

    html = get_html_head(
        title=f"Forward Deployed Engineer Jobs ({total_jobs} Roles)",
        description=f"Browse {total_jobs} Forward Deployed Engineer jobs at OpenAI, Salesforce, Palantir, Ramp, and 50+ companies. Salary data, remote options, updated weekly.",
        canonical_path="/jobs/",
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

    os.makedirs(os.path.join(SITE_DIR, 'jobs'), exist_ok=True)
    output_path = os.path.join(SITE_DIR, 'jobs', 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  Jobs page generated: {output_path} ({len(html):,} bytes)")
    print(f"  Stats: {total_jobs} jobs, {remote_count} remote ({pct_remote}%), {with_salary} with salary")


if __name__ == "__main__":
    generate_jobs_page()
