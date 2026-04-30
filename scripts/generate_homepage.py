#!/usr/bin/env python3
"""
Generate homepage for FDE Pulse.
Creates site/index.html with market stats, featured jobs, and company categories.
"""

import os
import sys
import json
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from nav_config import SITE_NAME, BASE_URL, COMPANY_CATEGORIES
from templates import (
    get_html_head, get_header_html, get_footer_html,
    get_mobile_nav_js, get_signup_js, get_cta_box, get_scroll_cta
)

SITE_DIR = os.path.join(os.path.dirname(script_dir), 'site')

# Load dynamic stats if available
_mi_path = os.path.join(os.path.dirname(script_dir), 'data', 'market_intelligence.json')
if os.path.exists(_mi_path):
    with open(_mi_path) as _f:
        _mi = json.load(_f)
    STATS = {
        'total_jobs': _mi.get('total_jobs', 0),
        'avg_salary': _mi.get('avg_salary', '$195K'),
        'remote_pct': _mi.get('remote_pct', '62%'),
        'companies': _mi.get('companies_hiring', 50),
    }
else:
    STATS = {
        'total_jobs': 154,
        'avg_salary': '$195K',
        'remote_pct': '62%',
        'companies': 50,
    }

# Load featured jobs if available
_jobs_path = os.path.join(os.path.dirname(script_dir), 'data', 'jobs.json')
if os.path.exists(_jobs_path):
    with open(_jobs_path) as _f:
        _jd = json.load(_f)
    FEATURED_JOBS = _jd.get('jobs', [])[:4]
else:
    FEATURED_JOBS = [
        {
            'company': 'OpenAI',
            'slug': 'openai',
            'title': 'Forward Deployed Engineer',
            'salary': '$185,000 - $285,000',
            'location': 'San Francisco, CA',
            'is_remote': False,
            'seniority': 'Mid-Senior',
        },
        {
            'company': 'Salesforce',
            'slug': 'salesforce',
            'title': 'Forward Deployed Software Engineer',
            'salary': '$170,000 - $240,000',
            'location': 'Remote, US',
            'is_remote': True,
            'seniority': 'Senior',
        },
        {
            'company': 'Palantir',
            'slug': 'palantir',
            'title': 'Senior Forward Deployed Engineer',
            'salary': '$165,000 - $250,000',
            'location': 'New York, NY',
            'is_remote': False,
            'seniority': 'Senior',
        },
        {
            'company': 'Ramp',
            'slug': 'ramp',
            'title': 'Forward Deployed Engineer',
            'salary': '$160,000 - $220,000',
            'location': 'New York, NY',
            'is_remote': False,
            'seniority': 'Mid-Senior',
        },
    ]


def generate_hero():
    return '''
        <section class="hero">
            <div class="hero__badge">
                <span class="hero__badge-dot"></span>
                Tracking 50+ companies hiring FDEs
            </div>
            <h1 class="hero__title">
                The <span class="hero__title-accent">Forward Deployed Engineer</span> Job Market
            </h1>
            <p class="hero__subtitle">
                Jobs, salaries, and market intelligence for the fastest-growing role in enterprise software. Updated weekly.
            </p>
            <div class="hero__buttons">
                <a href="#subscribe" class="btn btn--primary">Get the FDE Brief</a>
                <a href="/jobs/" class="btn btn--secondary">Browse Jobs</a>
            </div>
        </section>
'''


def generate_stats(stats):
    return f'''
        <section class="stats">
            <div class="stats__inner">
                <div class="stat">
                    <div class="stat__value">{stats['total_jobs']}+</div>
                    <div class="stat__label">Open Positions</div>
                </div>
                <div class="stat">
                    <div class="stat__value">{stats['avg_salary']}</div>
                    <div class="stat__label">Avg. Salary</div>
                </div>
                <div class="stat">
                    <div class="stat__value">{stats['remote_pct']}</div>
                    <div class="stat__label">Remote Friendly</div>
                </div>
                <div class="stat">
                    <div class="stat__value">{stats['companies']}+</div>
                    <div class="stat__label">Companies Hiring</div>
                </div>
            </div>
        </section>
'''


def generate_logo_bar():
    """Company logo strip with real PNG logos, RevOps Report style."""
    companies = [
        ('Palantir', 'palantir'),
        ('OpenAI', 'openai'),
        ('Salesforce', 'salesforce'),
        ('Anthropic', 'anthropic'),
        ('Databricks', 'databricks'),
        ('Ramp', 'ramp'),
        ('Scale AI', 'scale'),
        ('Rippling', 'rippling'),
        ('Cohere', 'cohere'),
        ('ServiceNow', 'servicenow'),
        ('PostHog', 'posthog'),
        ('UiPath', 'uipath'),
    ]

    items = ''
    for name, slug in companies:
        items += f'\n                <img src="/assets/logos/companies/{slug}.png" alt="{name}" class="logo-icon" title="{name}">'

    return f'''
        <section class="logo-strip">
            <div class="container">
                <p class="logo-strip-label">Companies hiring Forward Deployed Engineers</p>
                <div class="logo-strip-row">{items}
                </div>
            </div>
        </section>
'''


def generate_categories(categories):
    cards = ""
    for cat in categories:
        cards += f'''
                <a href="/jobs/?industry={cat['id']}" class="card category-card">
                    <div class="category-card__icon">{cat['icon']}</div>
                    <div class="category-card__title">{cat['title']}</div>
                    <div class="category-card__examples">{cat['examples']}</div>
                </a>'''

    return f'''
        <section class="section" style="max-width: 1200px; margin: 0 auto;">
            <div class="section__header">
                <h2 class="section__title">Browse by Company Type</h2>
                <p class="section__subtitle">Forward Deployed Engineers work across AI, enterprise SaaS, startups, and consulting</p>
            </div>
            <div class="categories-grid">
{cards}
            </div>
        </section>
'''


def generate_featured_jobs(jobs):
    cards = ""
    for job in jobs:
        is_remote = job.get('is_remote', False)
        remote_class = 'job-card__tag--remote' if is_remote else ''
        location = 'Remote' if is_remote else job.get('location', '')
        salary = job.get('salary', job.get('compensation', {}).get('display', ''))
        slug = job.get('slug', job.get('company', '').lower().replace(' ', '-'))

        cards += f'''
                <a href="/companies/{slug}/" class="card job-card" style="text-decoration: none; color: inherit; display: block;">
                    <div class="job-card__header">
                        <div>
                            <div class="job-card__company">{job.get('company', '')}</div>
                            <div class="job-card__title">{job.get('title', '')}</div>
                        </div>
                        {f'<div class="job-card__salary">{salary}</div>' if salary else ''}
                    </div>
                    <div class="job-card__meta">
                        <span class="job-card__tag {remote_class}">{location}</span>
                        <span class="job-card__tag">{job.get('seniority', '')}</span>
                    </div>
                </a>'''

    return f'''
        <section class="section" style="max-width: 1200px; margin: 0 auto;">
            <div class="section__header">
                <h2 class="section__title">Featured FDE Positions</h2>
                <p class="section__subtitle">Hand-picked Forward Deployed Engineer opportunities</p>
            </div>
            <div class="jobs-grid">
{cards}
            </div>
        </section>
'''


def generate_what_is_fde():
    """Explainer section for SEO and first-time visitors."""
    return '''
        <section class="section" style="max-width: 800px; margin: 0 auto;">
            <div class="section__header">
                <h2 class="section__title">What is a Forward Deployed Engineer?</h2>
            </div>
            <div style="color: var(--text-secondary); font-size: 1.05rem; line-height: 1.8;">
                <p style="margin-bottom: 1.25rem;">A Forward Deployed Engineer (FDE) is embedded directly with customers to build custom solutions, integrate products, and bridge the gap between product engineering and customer success. Originally pioneered by Palantir, the role has spread to 50+ companies including OpenAI, Salesforce, Ramp, and Databricks.</p>
                <p style="margin-bottom: 1.25rem;">FDEs combine deep technical skills with customer-facing communication. They write production code, build integrations, and translate customer problems into product improvements. Salaries range from $150,000 to $300,000+ depending on company and seniority.</p>
                <p>Job postings for Forward Deployed Engineers grew 800% in 2025. FDE Pulse tracks every posting, salary data point, and hiring trend so you don't miss the opportunity.</p>
            </div>
        </section>
'''


def generate_cta():
    return f'''
        <section style="padding: 0 var(--space-lg) var(--space-2xl);">
            {get_cta_box()}
        </section>
'''


def generate_homepage():
    print("=" * 70)
    print("  FDE PULSE - GENERATING HOMEPAGE")
    print("=" * 70)

    body = (
        generate_hero() +
        generate_stats(STATS) +
        generate_logo_bar() +
        generate_categories(COMPANY_CATEGORIES) +
        generate_featured_jobs(FEATURED_JOBS) +
        generate_what_is_fde() +
        generate_cta()
    )

    # Schema.org structured data
    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE_NAME,
        "url": BASE_URL,
        "description": "Jobs, salaries, and market intelligence for Forward Deployed Engineers",
        "publisher": {
            "@type": "Organization",
            "name": SITE_NAME,
            "url": BASE_URL
        }
    }, indent=2)

    extra_head = f'<script type="application/ld+json">\n{schema}\n    </script>'

    html = get_html_head(
        title="Forward Deployed Engineer Jobs & Salary Data",
        description="Find Forward Deployed Engineer jobs at OpenAI, Salesforce, Palantir, and 50+ companies. Salary data, market trends, and weekly intelligence.",
        canonical_path="/",
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

    os.makedirs(SITE_DIR, exist_ok=True)
    output_path = os.path.join(SITE_DIR, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n  Homepage generated: {output_path}")
    print(f"  Stats: {STATS['total_jobs']}+ jobs, {STATS['avg_salary']} avg salary")
    print(f"  Featured jobs: {len(FEATURED_JOBS)}")
    print("=" * 70)


if __name__ == "__main__":
    generate_homepage()
