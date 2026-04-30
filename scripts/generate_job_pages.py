#!/usr/bin/env python3
"""Generate individual job pages at /jobs/{slug}/index.html for FDE Pulse."""

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
JOBS_DIR = os.path.join(SITE_DIR, 'jobs')

JOB_DETAIL_CSS = """
/* Job Detail Page */
.job-detail { padding-top: 72px; }

.job-header {
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border);
    padding: var(--space-2xl) 0;
}
.job-header__inner {
    max-width: 900px;
    margin: 0 auto;
    padding: 0 var(--space-lg);
}
.job-header__breadcrumb {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    font-size: 0.9rem;
    color: var(--text-muted);
    margin-bottom: var(--space-lg);
}
.job-header__breadcrumb a {
    color: var(--text-secondary);
    transition: color var(--transition-fast);
}
.job-header__breadcrumb a:hover { color: var(--amber-light); }
.job-header__breadcrumb span.sep { color: var(--text-muted); }

.job-header__company {
    font-size: 1rem;
    color: var(--amber-light);
    font-weight: 500;
    margin-bottom: var(--space-sm);
}
.job-header__title {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: var(--space-lg);
    line-height: 1.2;
    color: var(--text-primary);
}
.job-header__meta {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-sm);
    margin-bottom: var(--space-xl);
}
.job-header__tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: var(--space-sm) var(--space-md);
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-full);
    font-size: 0.9rem;
    color: var(--text-secondary);
}
.job-header__tag--salary {
    background: rgba(74, 222, 128, 0.1);
    border-color: rgba(74, 222, 128, 0.3);
    color: #4ade80;
    font-weight: 600;
}
.job-header__tag--remote {
    background: rgba(74, 222, 128, 0.1);
    border-color: rgba(74, 222, 128, 0.3);
    color: #4ade80;
}
.job-header__tag--seniority {
    background: rgba(245, 158, 11, 0.1);
    border-color: rgba(245, 158, 11, 0.25);
    color: var(--amber-light);
}
.job-header__actions {
    display: flex;
    gap: var(--space-md);
    flex-wrap: wrap;
}

.stale-banner {
    background: rgba(245, 158, 11, 0.12);
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: var(--radius-md);
    padding: 0.75rem 1.25rem;
    margin-bottom: var(--space-lg);
    font-size: 0.9rem;
    color: var(--amber-light);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Content layout */
.job-content {
    max-width: 900px;
    margin: 0 auto;
    padding: var(--space-2xl) var(--space-lg);
    display: grid;
    grid-template-columns: 1fr 280px;
    gap: var(--space-2xl);
}
.job-main { min-width: 0; }
.job-sidebar {
    position: sticky;
    top: calc(72px + var(--space-xl));
    height: fit-content;
}

.job-section { margin-bottom: var(--space-2xl); }
.job-section__title {
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: var(--space-md);
    padding-bottom: var(--space-sm);
    border-bottom: 1px solid var(--border);
    color: var(--text-primary);
}
.job-description {
    color: var(--text-secondary);
    line-height: 1.8;
    font-size: 1rem;
}
.job-description p { margin-bottom: var(--space-md); }
.job-description ul, .job-description ol {
    margin: var(--space-md) 0;
    padding-left: var(--space-xl);
}
.job-description li { margin-bottom: var(--space-xs); }
.job-description strong { color: var(--text-primary); }
.job-description h3, .job-description h4 {
    color: var(--text-primary);
    font-weight: 600;
    margin: 1.25rem 0 0.5rem;
    font-size: 1rem;
}

/* Sidebar */
.sidebar-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    margin-bottom: var(--space-lg);
}
.sidebar-card__title {
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: var(--space-md);
    color: var(--text-primary);
}
.sidebar-card__item {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: var(--space-sm) 0;
    border-bottom: 1px solid var(--border-light);
    font-size: 0.875rem;
    gap: 0.5rem;
}
.sidebar-card__item:last-child { border-bottom: none; }
.sidebar-card__label { color: var(--text-muted); flex-shrink: 0; }
.sidebar-card__value { color: var(--text-primary); font-weight: 500; text-align: right; }
.sidebar-card__value--salary { color: #4ade80; }

/* Similar jobs */
.similar-jobs {
    margin-top: var(--space-2xl);
    padding-top: var(--space-2xl);
    border-top: 1px solid var(--border);
}
.similar-jobs__title {
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: var(--space-lg);
    color: var(--text-primary);
}
.similar-job {
    display: block;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    margin-bottom: var(--space-sm);
    transition: all var(--transition-fast);
    text-decoration: none;
}
.similar-job:hover {
    background: var(--bg-card-hover);
    border-color: var(--amber);
}
.similar-job__company {
    font-size: 0.8rem;
    color: var(--amber-light);
    margin-bottom: 3px;
    font-weight: 500;
}
.similar-job__title {
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--text-primary);
    margin-bottom: 0.4rem;
    line-height: 1.3;
}
.similar-job__salary {
    font-size: 0.85rem;
    color: #4ade80;
    font-weight: 600;
}

/* FDE About section */
.fde-about {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: var(--space-xl);
    margin-top: var(--space-2xl);
}
.fde-about h3 {
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: var(--space-md);
}
.fde-about p {
    color: var(--text-secondary);
    line-height: 1.7;
    margin-bottom: var(--space-md);
    font-size: 0.95rem;
}
.fde-about p:last-child { margin-bottom: 0; }

@media (max-width: 900px) {
    .job-content { grid-template-columns: 1fr; }
    .job-sidebar { position: static; order: -1; }
}
@media (max-width: 600px) {
    .job-header__title { font-size: 1.6rem; }
    .job-header__actions { flex-direction: column; }
    .job-header__actions .btn { justify-content: center; }
}
"""

FDE_ABOUT_SECTION = """
<div class="fde-about">
    <h3>About Forward Deployed Engineering</h3>
    <p>Forward Deployed Engineers are embedded directly with customers to build custom solutions, integrate products into existing infrastructure, and bridge the gap between product engineering and customer success. The role combines deep technical skills with the ability to operate in client environments and translate business requirements into working software.</p>
    <p>Originally pioneered by Palantir, the FDE model has spread across AI, enterprise SaaS, and cloud infrastructure companies. FDEs write production code, architect integrations, train customer teams, and feed product insights back to the core engineering organization. At companies like OpenAI, Salesforce, and Databricks, FDE teams are treated as elite engineering units that can ship custom solutions in days rather than quarters.</p>
    <p>Typical FDE stack: Python, TypeScript, SQL, REST/GraphQL APIs, cloud platforms (AWS/GCP/Azure), and increasingly LLM APIs and AI orchestration frameworks. Strong communication and the ability to context-switch between technical and business conversations are as important as coding ability.</p>
</div>
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


def format_date_long(date_str):
    if not date_str:
        return ''
    try:
        dt = datetime.strptime(date_str[:10], '%Y-%m-%d')
        return dt.strftime('%B %d, %Y')
    except Exception:
        return date_str


def is_stale(date_scraped_str, threshold_days=14):
    """Return True if job was scraped more than threshold_days ago."""
    if not date_scraped_str:
        return False
    try:
        scraped = datetime.strptime(date_scraped_str[:10], '%Y-%m-%d').date()
        return (date.today() - scraped).days > threshold_days
    except Exception:
        return False


def markdown_to_html(text):
    """Convert basic markdown to HTML. Fallback since 'markdown' package not installed."""
    if not text:
        return ''

    # Unescape literal backslash-escaped punctuation common in scraped Indeed descriptions
    text = text.replace('\\\\', '\x00BKSLASH\x00').replace('\\', '').replace('\x00BKSLASH\x00', '\\')

    # Bold: **text**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

    # ATX headers: ### Header
    text = re.sub(r'^#{1,6}\s+(.+)$', lambda m: f'<h4>{m.group(1).strip()}</h4>', text, flags=re.MULTILINE)

    paragraphs = text.split('\n\n')
    html_parts = []

    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        lines = p.split('\n')

        # Check if block is a bullet list
        bullet_lines = [l for l in lines if l.strip()]
        if bullet_lines and all(re.match(r'^[\*\-\•]\s', l) or not l.strip() for l in lines if l.strip()):
            items = [re.sub(r'^[\*\-\•]\s*', '', l.strip()) for l in lines if l.strip()]
            html_parts.append('<ul>' + ''.join(f'<li>{item}</li>' for item in items if item) + '</ul>')
        elif p.startswith('<h4>'):
            html_parts.append(p)
        else:
            p_clean = p.replace('\n', ' ')
            html_parts.append(f'<p>{p_clean}</p>')

    return '\n'.join(html_parts)


def parse_location(location_str):
    """Parse 'City, ST, US' into schema.org PostalAddress dict."""
    if not location_str or location_str.lower().startswith('remote'):
        return {"@type": "PostalAddress", "addressCountry": "US"}
    parts = [p.strip() for p in location_str.split(',')]
    address = {"@type": "PostalAddress"}
    if len(parts) >= 3:
        address["addressLocality"] = parts[0]
        address["addressRegion"] = parts[1]
        address["addressCountry"] = parts[2]
    elif len(parts) == 2:
        address["addressLocality"] = parts[0]
        address["addressRegion"] = parts[1]
        address["addressCountry"] = "US"
    else:
        address["addressCountry"] = parts[0] if parts else "US"
    return address


def build_job_posting_schema(job, slug):
    """Build JobPosting JSON-LD schema dict."""
    description_text = (
        job.get('description_snippet', '') or
        job.get('description', '')[:800] or
        f"{job.get('title', 'Forward Deployed Engineer')} role at {job.get('company', 'a company')}."
    )
    # Strip markdown markers for schema text
    description_clean = re.sub(r'\*\*|__|\#\#?\#?\s*|^\*\s', '', description_text, flags=re.MULTILINE)[:800]

    schema = {
        "@context": "https://schema.org",
        "@type": "JobPosting",
        "title": job.get('title', ''),
        "description": description_clean,
        "datePosted": job.get('date_posted', ''),
        "hiringOrganization": {
            "@type": "Organization",
            "name": job.get('company', 'Confidential')
        },
        "jobLocation": {
            "@type": "Place",
            "address": parse_location(job.get('location', ''))
        },
        "employmentType": "FULL_TIME",
        "url": f"{BASE_URL}/jobs/{slug}/"
    }

    if job.get('is_remote'):
        schema["jobLocationType"] = "TELECOMMUTE"

    min_amt = job.get('min_amount', 0) or 0
    max_amt = job.get('max_amount', 0) or 0
    if min_amt > 0 and max_amt > 0:
        schema["baseSalary"] = {
            "@type": "MonetaryAmount",
            "currency": "USD",
            "value": {
                "@type": "QuantitativeValue",
                "minValue": min_amt,
                "maxValue": max_amt,
                "unitText": "YEAR"
            }
        }

    return schema


def build_breadcrumb_schema(company, title, slug):
    """Build BreadcrumbList JSON-LD."""
    label = f"{title} at {company}"
    if len(label) > 50:
        label = label[:47].rstrip(' -,') + '...'
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Jobs", "item": f"{BASE_URL}/jobs/"},
            {"@type": "ListItem", "position": 3, "name": label, "item": f"{BASE_URL}/jobs/{slug}/"}
        ]
    }


def build_faq_schema(company, title):
    """Build role-specific FAQ JSON-LD for individual job pages."""
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"What does a Forward Deployed Engineer do at {company}?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"Forward Deployed Engineers at {company} are embedded directly with enterprise customers to implement and customize the platform, build integrations, and solve technical problems in real-world client environments. They combine software engineering skills with direct customer interaction, writing production code while also serving as the primary technical point of contact."
                }
            },
            {
                "@type": "Question",
                "name": f"What skills are required for this {title} role?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"The {title} role at {company} typically requires strong software engineering skills (Python, TypeScript, SQL), experience with APIs and system integration, comfort with cloud platforms, and the ability to communicate complex technical topics to non-technical stakeholders. Most FDE roles require 3-7 years of engineering experience."
                }
            },
            {
                "@type": "Question",
                "name": f"Is this Forward Deployed Engineer position at {company} remote?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"Remote availability varies by {company} FDE role. Some positions are fully remote, others require travel to customer sites, and some are hybrid. Check the full job description above for the specific location requirements for this posting."
                }
            }
        ]
    }


def find_similar_jobs(current_job, all_jobs, slug_map, n=3):
    """Find similar jobs: prefer same company, then same seniority, then random."""
    current_slug = slug_map.get(id(current_job), '')
    company = current_job.get('company', '')
    seniority = current_job.get('seniority', '')

    same_company = [j for j in all_jobs if j.get('company') == company and slug_map.get(id(j)) != current_slug]
    if len(same_company) >= n:
        return same_company[:n]

    # Fill remaining from same seniority or all jobs
    result = list(same_company)
    remaining_pool = [j for j in all_jobs if j.get('company') != company and slug_map.get(id(j)) != current_slug]
    if seniority:
        same_seniority = [j for j in remaining_pool if j.get('seniority') == seniority]
        result += same_seniority[:n - len(result)]

    if len(result) < n:
        others = [j for j in remaining_pool if j not in result]
        result += others[:n - len(result)]

    return result[:n]


def word_count_html(html_str):
    """Estimate word count from HTML string."""
    text = re.sub(r'<[^>]+>', ' ', html_str)
    text = re.sub(r'\s+', ' ', text).strip()
    return len(text.split())


def generate_job_page(job, slug, all_jobs, slug_map):
    """Generate HTML for one job page."""
    company = job.get('company', 'Confidential')
    title = job.get('title', 'Forward Deployed Engineer')
    location = job.get('location', '')
    is_remote = job.get('is_remote', False)
    seniority = job.get('seniority', '')
    date_posted = format_date_long(job.get('date_posted', ''))
    date_scraped = job.get('date_scraped', '')
    source = job.get('source', 'Indeed').title()
    source_url = job.get('source_url', '#')
    description_raw = job.get('description', '') or job.get('description_snippet', '')
    min_amt = job.get('min_amount', 0) or 0
    max_amt = job.get('max_amount', 0) or 0

    sal_fmt = format_salary(min_amt, max_amt)
    stale = is_stale(date_scraped)

    # Stale banner
    stale_banner = ''
    if stale:
        stale_banner = '''
                <div class="stale-banner">
                    <span>&#9432;</span>
                    This posting is more than 14 days old. The apply window may have closed &mdash;
                    <a href="/jobs/" style="color: var(--amber); text-decoration: underline;">browse all active FDE roles</a>.
                </div>'''

    # Breadcrumb
    breadcrumb_html = f'''
                <nav class="job-header__breadcrumb">
                    <a href="/">Home</a>
                    <span class="sep">/</span>
                    <a href="/jobs/">Jobs</a>
                    <span class="sep">/</span>
                    <span>{escape_html(company)}</span>
                </nav>'''

    # Meta tags
    meta_tags = []
    if sal_fmt:
        meta_tags.append(f'<span class="job-header__tag job-header__tag--salary">{sal_fmt}</span>')
    if is_remote:
        meta_tags.append('<span class="job-header__tag job-header__tag--remote">Remote</span>')
    elif location:
        meta_tags.append(f'<span class="job-header__tag">{escape_html(location)}</span>')
    if seniority:
        meta_tags.append(f'<span class="job-header__tag job-header__tag--seniority">{escape_html(seniority)}</span>')
    if date_posted:
        meta_tags.append(f'<span class="job-header__tag">Posted {date_posted}</span>')
    meta_tags_html = '\n                        '.join(meta_tags)

    # Description HTML
    description_html = markdown_to_html(description_raw) if description_raw else '<p>See full description on the source posting.</p>'

    # Check word count, append FDE section if needed
    desc_words = word_count_html(description_html)
    fde_section = ''
    if desc_words < 800:
        fde_section = FDE_ABOUT_SECTION

    # Similar jobs
    similar = find_similar_jobs(job, all_jobs, slug_map, n=3)
    similar_html = ''
    if similar:
        cards = ''
        for sj in similar:
            sj_slug = slug_map.get(id(sj), '')
            sj_sal = format_salary(sj.get('min_amount', 0) or 0, sj.get('max_amount', 0) or 0)
            sj_sal_html = f'<div class="similar-job__salary">{sj_sal}</div>' if sj_sal else ''
            cards += f'''
                <a href="/jobs/{sj_slug}/" class="similar-job">
                    <div class="similar-job__company">{escape_html(sj.get("company", ""))}</div>
                    <div class="similar-job__title">{escape_html(sj.get("title", ""))}</div>
                    {sj_sal_html}
                </a>'''
        similar_html = f'''
            <div class="similar-jobs">
                <h2 class="similar-jobs__title">Similar Roles</h2>
                {cards}
            </div>'''

    # Sidebar
    sidebar_items = [('Company', escape_html(company))]
    if is_remote:
        sidebar_items.append(('Location', 'Remote'))
    elif location:
        sidebar_items.append(('Location', escape_html(location)))
    if seniority:
        sidebar_items.append(('Level', escape_html(seniority)))
    if sal_fmt:
        sidebar_items.append(('Salary', f'<span class="sidebar-card__value--salary">{sal_fmt}</span>'))
    if date_posted:
        sidebar_items.append(('Posted', date_posted))
    sidebar_items.append(('Source', escape_html(source)))

    sidebar_rows = ''
    for label, value in sidebar_items:
        sidebar_rows += f'''
                    <div class="sidebar-card__item">
                        <span class="sidebar-card__label">{label}</span>
                        <span class="sidebar-card__value">{value}</span>
                    </div>'''

    # JSON-LD schemas
    job_schema = build_job_posting_schema(job, slug)
    breadcrumb_schema = build_breadcrumb_schema(company, title, slug)
    faq_schema = build_faq_schema(company, title)

    schemas_html = f'''
    <script type="application/ld+json">{json.dumps(job_schema)}</script>
    <script type="application/ld+json">{json.dumps(breadcrumb_schema)}</script>
    <script type="application/ld+json">{json.dumps(faq_schema)}</script>'''

    # Meta title & description
    meta_title = f"{title} at {company}"
    if len(meta_title) > 46:
        meta_title = meta_title[:43].rstrip(' -,') + '...'

    loc_text = 'Remote' if is_remote else location
    meta_desc_parts = [f"{title} at {company}"]
    if sal_fmt:
        meta_desc_parts.append(sal_fmt)
    if loc_text:
        meta_desc_parts.append(loc_text)
    meta_desc = '. '.join(meta_desc_parts) + '. View role details, requirements, and apply. FDE jobs updated weekly on FDE Pulse.'
    if len(meta_desc) > 160:
        meta_desc = meta_desc[:157].rstrip(' .,') + '.'

    # Body
    body = f'''
        <div class="job-detail">
            <div class="job-header">
                <div class="job-header__inner">
                    {breadcrumb_html}
                    {stale_banner}
                    <div class="job-header__company">{escape_html(company)}</div>
                    <h1 class="job-header__title">{escape_html(title)}</h1>
                    <div class="job-header__meta">
                        {meta_tags_html}
                    </div>
                    <div class="job-header__actions">
                        <a href="{escape_html(source_url)}" target="_blank" rel="noopener" class="btn btn--primary">Apply on {escape_html(source)}</a>
                        <a href="/jobs/" class="btn btn--secondary">All FDE Jobs</a>
                    </div>
                </div>
            </div>

            <div class="job-content">
                <div class="job-main">
                    <div class="job-section">
                        <h2 class="job-section__title">Role Description</h2>
                        <div class="job-description">
                            {description_html}
                        </div>
                    </div>
                    {fde_section}
                    {similar_html}
                    <div style="margin-top: 2rem;">
                        {get_cta_box()}
                    </div>
                </div>

                <aside class="job-sidebar">
                    <div class="sidebar-card">
                        <h3 class="sidebar-card__title">Job Details</h3>
                        {sidebar_rows}
                    </div>
                    <a href="{escape_html(source_url)}" target="_blank" rel="noopener" class="btn btn--primary" style="width: 100%; justify-content: center; display: flex;">
                        Apply on {escape_html(source)}
                    </a>
                </aside>
            </div>
        </div>
'''

    extra_head = f'''<style>{JOB_DETAIL_CSS}</style>
{schemas_html}'''

    html = get_html_head(
        title=meta_title,
        description=meta_desc,
        canonical_path=f"/jobs/{slug}/",
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

    return html


def main():
    print("=" * 60)
    print("  FDE PULSE - GENERATING INDIVIDUAL JOB PAGES")
    print("=" * 60)

    os.makedirs(JOBS_DIR, exist_ok=True)

    jobs_file = os.path.join(DATA_DIR, 'jobs.json')
    if not os.path.exists(jobs_file):
        print(f"  ERROR: {jobs_file} not found")
        sys.exit(1)

    with open(jobs_file, encoding='utf-8') as f:
        data = json.load(f)

    jobs = data.get('jobs', [])
    print(f"  Loaded {len(jobs)} jobs from jobs.json")

    # Pre-compute all slugs and map by object id for O(1) lookup
    slug_map = {}
    for job in jobs:
        slug = make_slug(job.get('company', ''), job.get('title', ''), job.get('source_url', ''))
        slug_map[id(job)] = slug

    generated = 0
    errors = 0

    for i, job in enumerate(jobs):
        slug = slug_map[id(job)]
        job_dir = os.path.join(JOBS_DIR, slug)
        os.makedirs(job_dir, exist_ok=True)
        output_path = os.path.join(job_dir, 'index.html')

        try:
            html = generate_job_page(job, slug, jobs, slug_map)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
            generated += 1
        except Exception as e:
            print(f"  ERROR generating {slug}: {e}")
            errors += 1

        if (i + 1) % 25 == 0:
            print(f"  Progress: {i + 1}/{len(jobs)} pages generated...")

    print(f"  Generated {generated} job pages ({errors} errors)")
    print(f"  Output: {JOBS_DIR}/{{slug}}/index.html")

    # Quick sanity check
    dirs = [d for d in os.listdir(JOBS_DIR) if os.path.isdir(os.path.join(JOBS_DIR, d))]
    print(f"  Total job directories: {len(dirs)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
