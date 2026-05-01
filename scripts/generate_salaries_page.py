#!/usr/bin/env python3
"""Generate the Salaries landing page for FDE Pulse using real comp_analysis data."""

import os
import sys
import json
import re
from collections import Counter
from statistics import median as stat_median

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from nav_config import SITE_NAME, BASE_URL
from templates import (
    get_html_head, get_header_html, get_footer_html,
    get_mobile_nav_js, get_signup_js, get_cta_box
)

SITE_DIR = os.path.join(os.path.dirname(script_dir), 'site')
DATA_DIR = os.path.join(os.path.dirname(script_dir), 'data')

# duplicated from generate_jobs_page.py -- keep in sync
def derive_seniority(title):
    """Classify a job title into a seniority bucket."""
    t = title or ''
    t_lower = t.lower()
    if re.search(r'\b(manager|director|head of|vp|lead)\b', t_lower):
        return 'lead'
    if re.search(r'\b(senior|sr\.|sr |staff|principal)\b', t_lower):
        return 'senior'
    if re.search(r'\b(junior|jr\.|associate|entry|intern|analyst)\b', t_lower):
        return 'junior'
    return 'mid'

SENIORITY_DISPLAY = {
    'lead': 'Manager / Lead',
    'senior': 'Senior+',
    'mid': 'Mid-level',
    'junior': 'Junior',
}

FAQS = [
    {
        "q": "What is the median Forward Deployed Engineer salary?",
        "a": "Based on 111 of 134 active FDE postings that disclosed pay as of April 2026, the median base salary is $135,000 and the average is $139,470. The full salary range spans $49,920 to $365,000. These figures cover base compensation only. Equity, sign-on bonuses, and benefits are not included."
    },
    {
        "q": "Do Forward Deployed Engineers earn more than regular software engineers?",
        "a": "FDE roles typically target engineers with 3 or more years of experience and strong customer-facing skills. The $135,000 median base reflects a market that skews mid-to-senior. At companies like Google, KPMG, and ServiceNow, senior FDE base salaries reach $200,000 to $365,000, which sits above most comparable software engineering bands at the same firms."
    },
    {
        "q": "How does FDE pay vary by location?",
        "a": "Based on 134 active postings, Seattle-area FDE roles show a median of $171,300 and New York roles show a median of $153,000. San Francisco and Austin are close behind at $160,000 and $141,000 respectively. Remote FDE roles show a median of $120,240, roughly 11% below the overall median, which reflects the geographic pay gap common in tech compensation."
    },
    {
        "q": "Do remote FDE roles pay less than on-site?",
        "a": "Yes. Based on 134 active postings, on-site FDE roles show a median base of $140,000 versus $120,240 for fully remote roles. That is an 14% gap. However, remote roles carry no cost-of-living burden and eliminate commute costs, which narrows the effective gap for engineers outside major metro areas."
    },
    {
        "q": "What are the top paying Forward Deployed Engineer roles right now?",
        "a": "The highest disclosed FDE salary range in the current dataset is $262,000 to $365,000 for a Senior Staff Forward Deployed Developer at Google Cloud. KPMG, ServiceNow, and Vista Equity Partners also list roles with max salaries above $300,000. These are senior-level positions in major metro markets with significant experience requirements."
    },
]


def format_k(amount):
    """Format a dollar amount as $Xk."""
    if not amount:
        return 'N/A'
    return '$' + str(int(round(amount / 1000))) + 'K'


def generate_salaries_page():
    print("  Generating salaries page...")

    # Load data
    comp_file = os.path.join(DATA_DIR, 'comp_analysis.json')
    jobs_file = os.path.join(DATA_DIR, 'jobs.json')

    with open(comp_file, encoding='utf-8') as f:
        comp = json.load(f)

    with open(jobs_file, encoding='utf-8') as f:
        jobs_data = json.load(f)

    jobs = jobs_data.get('jobs', [])

    # Top-level stats
    sal_stats = comp.get('salary_stats', {})
    median_sal = sal_stats.get('median', 135000)
    avg_sal = sal_stats.get('avg', 139470)
    sal_min = sal_stats.get('min', 49920)
    sal_max = sal_stats.get('max', 365000)
    count_with_sal = sal_stats.get('count_with_salary', 111)
    total_records = comp.get('total_records', 134)
    disclosure_rate = comp.get('disclosure_rate', 82.8)

    # ── Hero stats bar ──────────────────────────────────────────────────────────
    stats_bar = f'''
    <div class="job-stats-bar">
        <div class="job-stats-bar__inner">
            <span class="job-stat-item"><strong>{format_k(median_sal)}</strong> median base</span>
            <span class="job-stat-item"><strong>{format_k(avg_sal)}</strong> average base</span>
            <span class="job-stat-item"><strong>{format_k(sal_min)}&ndash;{format_k(sal_max)}</strong> full range</span>
            <span class="job-stat-item"><strong>{int(round(disclosure_rate))}%</strong> disclosure rate ({count_with_sal} of {total_records} roles)</span>
        </div>
    </div>'''

    # ── Page header ─────────────────────────────────────────────────────────────
    page_header = '''
        <div class="page-header">
            <div class="page-header__inner">
                <h1 class="page-header__title">Forward Deployed Engineer Salaries</h1>
                <p class="page-header__subtitle">Compensation data drawn from real FDE job postings. Base salary benchmarks by seniority, metro, and remote status.</p>
            </div>
        </div>'''

    # ── Seniority table ─────────────────────────────────────────────────────────
    # Derive seniority from job titles since most have empty seniority field
    seniority_buckets = {'lead': [], 'senior': [], 'mid': [], 'junior': []}
    for j in jobs:
        bucket = derive_seniority(j.get('title', ''))
        mn = j.get('min_amount', 0) or 0
        mx = j.get('max_amount', 0) or 0
        seniority_buckets[bucket].append({'min': mn, 'max': mx})

    seniority_rows = ''
    for bucket in ('senior', 'lead', 'mid', 'junior'):
        all_j = seniority_buckets[bucket]
        count = len(all_j)
        sal_j = [j for j in all_j if j['min'] > 0 and j['max'] > 0]
        if sal_j:
            mins = [j['min'] for j in sal_j]
            maxs = [j['max'] for j in sal_j]
            med = int(stat_median([m for pair in zip(mins, maxs) for m in pair]))
            rng = format_k(min(mins)) + ' &ndash; ' + format_k(max(maxs))
        else:
            med = 0
            rng = 'N/A'
        label = SENIORITY_DISPLAY.get(bucket, bucket)
        med_str = format_k(med) if med else 'N/A'
        seniority_rows += f'''
                <tr>
                    <td style="padding: 0.85rem 1rem; font-weight: 600; color: var(--text-primary);">{label}</td>
                    <td style="padding: 0.85rem 1rem; text-align: center; color: var(--text-secondary);">{count}</td>
                    <td style="padding: 0.85rem 1rem; color: var(--amber-light); font-weight: 600;">{med_str}</td>
                    <td style="padding: 0.85rem 1rem; color: var(--text-secondary);">{rng}</td>
                </tr>'''

    seniority_note = f'Seniority derived from job title analysis of all {total_records} active postings. Most postings do not explicitly label a seniority tier.'

    seniority_section = f'''
        <div class="sal-section">
            <h2 class="sal-section__title">Salary by Seniority</h2>
            <p class="sal-section__note">{seniority_note}</p>
            <div style="overflow-x: auto;">
                <table class="sal-table">
                    <thead>
                        <tr>
                            <th>Level</th>
                            <th style="text-align:center;">Active Roles</th>
                            <th>Median Base</th>
                            <th>Range</th>
                        </tr>
                    </thead>
                    <tbody>{seniority_rows}
                    </tbody>
                </table>
            </div>
        </div>'''

    # ── Metro table ─────────────────────────────────────────────────────────────
    by_metro = comp.get('by_metro', {})
    metro_rows = ''
    # Skip 'Unknown', show up to 8 known metros
    metro_items = [(m, v) for m, v in by_metro.items() if m != 'Unknown']
    # Sort by median descending
    metro_items.sort(key=lambda x: x[1].get('median', 0), reverse=True)

    for metro, v in metro_items[:8]:
        count = v.get('count', 0)
        med = v.get('median', 0)
        mn_avg = v.get('min_base_avg', 0)
        mx_avg = v.get('max_base_avg', 0)
        metro_rows += f'''
                <tr>
                    <td style="padding: 0.85rem 1rem; font-weight: 600; color: var(--text-primary);">{metro}</td>
                    <td style="padding: 0.85rem 1rem; text-align: center; color: var(--text-secondary);">{count}</td>
                    <td style="padding: 0.85rem 1rem; color: var(--amber-light); font-weight: 600;">{format_k(med)}</td>
                    <td style="padding: 0.85rem 1rem; color: var(--text-secondary);">{format_k(mn_avg)} &ndash; {format_k(mx_avg)}</td>
                </tr>'''

    metro_section = f'''
        <div class="sal-section">
            <h2 class="sal-section__title">Salary by Metro</h2>
            <p class="sal-section__note">Based on postings with a disclosed location. {by_metro.get("Unknown", {}).get("count", 0)} postings listed no specific metro.</p>
            <div style="overflow-x: auto;">
                <table class="sal-table">
                    <thead>
                        <tr>
                            <th>Metro</th>
                            <th style="text-align:center;">Roles</th>
                            <th>Median Base</th>
                            <th>Avg Range</th>
                        </tr>
                    </thead>
                    <tbody>{metro_rows}
                    </tbody>
                </table>
            </div>
        </div>'''

    # ── Remote vs On-site ───────────────────────────────────────────────────────
    by_remote = comp.get('by_remote', {})
    onsite = by_remote.get('onsite', {})
    remote = by_remote.get('remote', {})

    remote_cards = f'''
        <div class="sal-section">
            <h2 class="sal-section__title">Remote vs. On-Site Compensation</h2>
            <div class="sal-remote-grid">
                <div class="sal-remote-card">
                    <div class="sal-remote-card__label">On-Site</div>
                    <div class="sal-remote-card__value">{format_k(onsite.get("median", 0))}</div>
                    <div class="sal-remote-card__sub">median base</div>
                    <div class="sal-remote-card__meta">{onsite.get("count", 0)} active roles</div>
                    <div class="sal-remote-card__range">{format_k(onsite.get("min_base_avg", 0))} &ndash; {format_k(onsite.get("max_base_avg", 0))} avg range</div>
                </div>
                <div class="sal-remote-card">
                    <div class="sal-remote-card__label">Remote</div>
                    <div class="sal-remote-card__value">{format_k(remote.get("median", 0))}</div>
                    <div class="sal-remote-card__sub">median base</div>
                    <div class="sal-remote-card__meta">{remote.get("count", 0)} active roles</div>
                    <div class="sal-remote-card__range">{format_k(remote.get("min_base_avg", 0))} &ndash; {format_k(remote.get("max_base_avg", 0))} avg range</div>
                </div>
            </div>
            <p class="sal-section__note" style="margin-top: 1rem;">Remote FDE roles pay roughly {int(round(100 * (1 - remote.get("median", 120000) / onsite.get("median", 140000))))}% less at the median than on-site positions. Most remote FDE postings require periodic travel to customer sites.</p>
        </div>'''

    # ── Top paying roles ────────────────────────────────────────────────────────
    top_paying = comp.get('top_paying_roles', [])
    if not top_paying:
        # Fallback: derive from jobs.json
        jobs_with_sal = [j for j in jobs if (j.get('max_amount', 0) or 0) > 0]
        jobs_with_sal.sort(key=lambda j: j.get('max_amount', 0), reverse=True)
        top_paying = [
            {
                'title': j.get('title', ''),
                'company': j.get('company', ''),
                'salary_min': j.get('min_amount', 0),
                'salary_max': j.get('max_amount', 0),
            }
            for j in jobs_with_sal[:10]
        ]

    top_rows = ''
    for i, role in enumerate(top_paying[:10], 1):
        title = role.get('title', '')
        company = role.get('company', '')
        sal_min = role.get('salary_min', 0) or 0
        sal_max = role.get('salary_max', 0) or 0
        rng = format_k(sal_min) + ' &ndash; ' + format_k(sal_max)
        top_rows += f'''
                <tr>
                    <td style="padding: 0.85rem 1rem; text-align: center; color: var(--text-muted); font-weight: 600;">{i}</td>
                    <td style="padding: 0.85rem 1rem; font-weight: 600; color: var(--text-primary);">{title}</td>
                    <td style="padding: 0.85rem 1rem; color: var(--text-secondary);">{company}</td>
                    <td style="padding: 0.85rem 1rem; color: var(--amber-light); font-weight: 600; white-space: nowrap;">{rng}</td>
                </tr>'''

    top_paying_section = f'''
        <div class="sal-section">
            <h2 class="sal-section__title">Top 10 Paying FDE Roles (Active Postings)</h2>
            <p class="sal-section__note">Ranked by maximum disclosed salary. All roles are currently active postings as of April 30, 2026.</p>
            <div style="overflow-x: auto;">
                <table class="sal-table">
                    <thead>
                        <tr>
                            <th style="text-align:center;">#</th>
                            <th>Title</th>
                            <th>Company</th>
                            <th>Salary Range</th>
                        </tr>
                    </thead>
                    <tbody>{top_rows}
                    </tbody>
                </table>
            </div>
        </div>'''

    # ── Prose body ──────────────────────────────────────────────────────────────
    prose = f'''
        <div class="sal-prose">
            <h2>How FDE Compensation Works</h2>

            <p>Forward Deployed Engineers command premium compensation because the role demands a skill set most engineers don't have: production-grade software engineering plus the ability to run customer engagements independently. Companies pay for that combination because it's difficult to recruit for.</p>

            <p>The $135,000 median base across all 134 active postings reflects a market skewed toward mid-to-senior engineers. Most FDE job descriptions list three to seven years of software engineering experience as a baseline. Junior-level FDE roles exist primarily at large, structured FDE programs like Google Cloud, Deloitte, and Salesforce, which can afford the training investment.</p>

            <h2>Why the Salary Range Is So Wide</h2>

            <p>The $50K-to-$365K range in the current dataset reflects genuine market variation, not data error. At the low end, roles like technical implementation contractors and junior field engineers at smaller regional firms sit well below the median. At the top, Staff and Director-level FDE roles at Google, KPMG, and ServiceNow carry total compensation structures that push the maximum well past $300,000.</p>

            <p>Company stage matters more than seniority for determining compensation ceiling. A senior FDE at a Series B startup typically earns less in cash than a mid-level FDE at Google Cloud, though startup equity may offset the gap if the company grows. The {int(disclosure_rate)}% disclosure rate in the current dataset means the true market range may be wider than what's visible here.</p>

            <h2>Equity and Total Compensation</h2>

            <p>Base salary is only part of FDE compensation. Based on the current postings, {comp.get("comp_signals", {}).get("Equity", 0)} of {total_records} active FDE roles ({int(round(100 * comp.get("comp_signals", {}).get("Equity", 0) / total_records))}%) mention equity as part of the compensation package. At pre-IPO companies, equity grants can represent 20 to 50 percent of total annual compensation. At public companies, RSU grants vest over four years and carry predictable value.</p>

            <p>{comp.get("comp_signals", {}).get("Ote_mentioned", comp.get("comp_signals", {}).get("OTE_mentioned", comp.get("comp_signals", {}).get("Ote Mentioned", 3)))} postings mention on-target earnings (OTE), which typically applies to pre-sales FDE roles where the engineer participates in deal closure and earns commission. {comp.get("comp_signals", {}).get("Uncapped", 3)} postings mention uncapped commission structures. These roles often carry the highest potential total compensation but come with variable income.</p>

            <h2>Salary Trends to Watch</h2>

            <p>The FDE salary market is actively moving upward. Three factors are driving this:</p>

            <p>First, Salesforce's commitment to hiring 1,000 FDEs for Agentforce is creating a floor for the role. When the largest enterprise software company in the world offers $170,000 to $240,000 for FDE roles, that sets a reference point that other companies compete against.</p>

            <p>Second, AI companies are pulling experienced engineers out of traditional SaaS companies with compensation packages that include significant equity upside. Google Cloud, ServiceNow, and Deloitte are counter-offering to retain FDE talent, which compresses the gap between startup and enterprise FDE compensation.</p>

            <p>Third, the skill requirements are rising. Two years ago, an FDE with strong Python and API integration skills was the standard profile. Today, postings increasingly require RAG architecture, LLM evaluation, and AI safety knowledge. That specialization commands higher compensation.</p>

            <h2>Frequently Asked Questions</h2>'''

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

    # ── Methodology ─────────────────────────────────────────────────────────────
    methodology = f'''
        <div class="sal-section" style="margin-top: 0;">
            <h2 class="sal-section__title">Methodology</h2>
            <p style="color: var(--text-secondary); line-height: 1.8; font-size: 0.95rem;">
                Compensation data drawn from {count_with_sal} of {total_records} active FDE postings that disclosed pay as of April 30, 2026.
                Salary figures represent base compensation only. Equity, sign-on bonuses, benefits, and variable pay (OTE, commission) are not included.
                Median and average figures exclude postings with no disclosed compensation.
                Seniority buckets are derived from job title analysis because most postings ({comp.get("by_seniority", {}).get("Unknown", {}).get("count", 81)} of {count_with_sal}) do not explicitly label a tier.
                Metro grouping uses the primary city in the posted location. Remote postings are classified separately regardless of listed location.
                Data is updated weekly as new postings are added and closed roles are removed.
            </p>
        </div>'''

    # Combine all sections
    body = f'''
{stats_bar}
{page_header}

        <div class="sal-body">
{seniority_section}
{metro_section}
{remote_cards}
{top_paying_section}
{prose}
            {faq_html}
        </div>

{methodology}

        <div style="max-width: 900px; margin: 0 auto; padding: 0 1.5rem;">
            {get_cta_box()}
        </div>
    '''

    # Page CSS
    page_css = '''
.page-header {
    padding: 8rem 0 3rem;
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border);
}
.page-header__inner {
    max-width: 900px;
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
.job-stats-bar {
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border);
    padding: 1rem var(--space-lg);
}
.job-stats-bar__inner {
    max-width: 900px;
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
.sal-body {
    max-width: 900px;
    margin: 0 auto;
    padding: 3rem 1.5rem;
}
.sal-section {
    margin-bottom: 3rem;
}
.sal-section__title {
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.75rem;
}
.sal-section__note {
    font-size: 0.9rem;
    color: var(--text-muted);
    margin-bottom: 1.25rem;
}
.sal-table {
    width: 100%;
    border-collapse: collapse;
    background: var(--bg-card);
    border-radius: var(--radius-lg);
    overflow: hidden;
    border: 1px solid var(--border);
}
.sal-table thead tr {
    border-bottom: 1px solid var(--border);
}
.sal-table th {
    padding: 0.75rem 1rem;
    text-align: left;
    font-size: 0.8rem;
    color: var(--text-muted);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.sal-table tbody tr {
    border-bottom: 1px solid var(--border-light);
    transition: background var(--transition-fast);
}
.sal-table tbody tr:last-child {
    border-bottom: none;
}
.sal-table tbody tr:hover {
    background: var(--bg-card-hover);
}
.sal-remote-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.25rem;
}
.sal-remote-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.75rem;
    text-align: center;
}
.sal-remote-card__label {
    font-size: 0.85rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.5rem;
    font-weight: 600;
}
.sal-remote-card__value {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--amber-light);
    line-height: 1;
    margin-bottom: 0.25rem;
}
.sal-remote-card__sub {
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin-bottom: 0.75rem;
}
.sal-remote-card__meta {
    font-size: 0.875rem;
    color: var(--text-muted);
    margin-bottom: 0.25rem;
}
.sal-remote-card__range {
    font-size: 0.85rem;
    color: var(--text-secondary);
}
.sal-prose {
    color: var(--text-secondary);
    font-size: 1.05rem;
    line-height: 1.8;
    margin-bottom: 3rem;
}
.sal-prose h2 {
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 2.5rem 0 1rem;
}
.sal-prose p {
    margin-bottom: 1.25rem;
}
@media (max-width: 768px) {
    .page-header { padding: 6rem 0 2rem; }
    .page-header__title { font-size: 2rem; }
    .sal-remote-grid { grid-template-columns: 1fr; }
    .job-stats-bar__inner { gap: 1rem; }
}
'''

    # JSON-LD schemas
    faq_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_schema_items
    }, indent=2)

    breadcrumb = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": "Salaries", "item": BASE_URL + "/salaries/"}
        ]
    }, indent=2)

    dataset = json.dumps({
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": "Forward Deployed Engineer Salary Data 2026",
        "description": f"Compensation benchmarks for Forward Deployed Engineers from {count_with_sal} active job postings",
        "url": BASE_URL + "/salaries/",
        "creator": {"@type": "Organization", "name": SITE_NAME},
        "dateModified": "2026-04-30"
    }, indent=2)

    extra_head = (
        f'<style>{page_css}</style>\n'
        f'    <script type="application/ld+json">\n{faq_schema}\n    </script>\n'
        f'    <script type="application/ld+json">\n{breadcrumb}\n    </script>\n'
        f'    <script type="application/ld+json">\n{dataset}\n    </script>'
    )

    html = get_html_head(
        title="Forward Deployed Engineer Salaries 2026",
        description=f"FDE salary data from {count_with_sal} real job postings. Median ${int(median_sal/1000)}K, range ${int(sal_min/1000)}K-${int(sal_max/1000)}K. By seniority, metro, and remote vs on-site.",
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
    out_path = os.path.join(SITE_DIR, 'salaries', 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  Salaries page generated: {out_path} ({len(html):,} bytes)")


if __name__ == "__main__":
    generate_salaries_page()
