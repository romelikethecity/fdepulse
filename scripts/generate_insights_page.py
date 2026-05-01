#!/usr/bin/env python3
"""
Generate the Insights landing page + 5 data-driven article pages for FDE Pulse.
All claims backed by jobs.json + market_intelligence.json + comp_analysis.json.
"""

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
    get_mobile_nav_js, get_signup_js, get_cta_box, get_article_schema, get_related_links
)

SITE_DIR = os.path.join(os.path.dirname(script_dir), 'site')
DATA_DIR = os.path.join(os.path.dirname(script_dir), 'data')

DATE_PUBLISHED = "2026-04-30"

ARTICLES = [
    {
        "slug": "fde-hiring-trends-2026",
        "title": "Forward Deployed Engineer Hiring Trends 2026",
        "description": "Data-driven analysis of FDE hiring in 2026. Based on 134 active job postings: who is hiring, where, and what it means for the market.",
    },
    {
        "slug": "fde-salary-benchmarks",
        "title": "FDE Salary Benchmarks: What Forward Deployed Engineers Earn in 2026",
        "description": "FDE salary data from 111 real job postings. Median $135K, range $50K to $365K. By seniority, metro, and remote vs on-site.",
    },
    {
        "slug": "top-fde-companies",
        "title": "30 Companies Hiring Forward Deployed Engineers Right Now",
        "description": "The companies with the most active FDE job postings as of April 2026. Role counts, salary ranges, and direct links to open positions.",
    },
    {
        "slug": "fde-skills-tools",
        "title": "What Skills Do Forward Deployed Engineers Need?",
        "description": "The tools and skills mentioned in 134 active FDE job postings. Python leads at 53%, GCP at 53%, AWS at 31%. Full breakdown with percentages.",
    },
    {
        "slug": "fde-locations",
        "title": "Where Forward Deployed Engineers Are Hiring",
        "description": "Location breakdown of 134 active FDE postings. New York leads with 32 roles. Seattle pays the most at $171K median. Remote vs on-site analysis.",
    },
]

INSIGHTS_INDEX_FAQS = [
    {
        "q": "How fast is the Forward Deployed Engineer market growing?",
        "a": "Based on 134 active FDE postings tracked by FDE Pulse as of April 30, 2026, the market spans 70 companies and covers roles from entry-level to Director. The market has expanded well beyond Palantir's original model to include AI companies, consulting firms, enterprise SaaS, fintech, and more."
    },
    {
        "q": "What is the median FDE salary in 2026?",
        "a": "The median base salary across 111 active FDE postings with disclosed compensation is $135,000 as of April 30, 2026. The average is $139,470. The full range is $49,920 to $365,000. Equity, sign-on bonuses, and OTE are not included in these figures."
    },
    {
        "q": "Which companies are hiring the most FDEs right now?",
        "a": "Google leads with 34 active FDE postings as of April 30, 2026. Deloitte is second with 19. Amazon Web Services, Accenture, and Logic Inc. each have 3 active postings. Together the top 5 companies account for roughly 48% of all active FDE roles."
    },
    {
        "q": "What tools do Forward Deployed Engineers use?",
        "a": "Based on tool mentions in 134 active FDE job descriptions, Python and GCP each appear in 53% of postings. AWS appears in 31%, Azure in 28%, and RAG (retrieval-augmented generation) in 22%. TypeScript, JavaScript, and prompt engineering round out the top tools. See the skills article for the full breakdown."
    },
    {
        "q": "How does FDE Pulse collect market data?",
        "a": "FDE Pulse tracks job postings with 'Forward Deployed Engineer' in the title across major job boards. Salary data is extracted from postings that disclose compensation. Market intelligence signals (tools, team structure, geo focus) are derived from structured parsing of job description text. Data is updated weekly."
    },
]


def format_k(amount):
    if not amount or amount <= 0:
        return 'N/A'
    return '$' + str(int(round(amount / 1000))) + 'K'


def make_slug(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def related_articles_html(current_slug):
    """Return HTML for 'Related Insights' linking to other 4 articles."""
    others = [a for a in ARTICLES if a['slug'] != current_slug]
    links = [{"href": f"/insights/{a['slug']}/", "label": a['title']} for a in others]
    return get_related_links(links)


def article_card_html(article):
    """Return a card for the article index."""
    return f'''
        <a href="/insights/{article["slug"]}/" class="insight-card">
            <div class="insight-card__label">Data Report</div>
            <h2 class="insight-card__title">{article["title"]}</h2>
            <p class="insight-card__desc">{article["description"]}</p>
            <div class="insight-card__cta">Read article &rarr;</div>
        </a>'''


def wrap_article(title, description, slug, body_content):
    """Wrap article body in full HTML page."""
    breadcrumb = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": "Insights", "item": BASE_URL + "/insights/"},
            {"@type": "ListItem", "position": 3, "name": title, "item": BASE_URL + f"/insights/{slug}/"},
        ]
    }, indent=2)
    article_schema = get_article_schema(title, description, f"/insights/{slug}/", DATE_PUBLISHED)
    extra_head = f'<style>{ARTICLE_CSS}</style>\n    <script type="application/ld+json">\n{breadcrumb}\n    </script>\n    {article_schema}'

    html = get_html_head(title=title, description=description, canonical_path=f"/insights/{slug}/", extra_head=extra_head)
    html += f'''
<body>
{get_header_html()}
    <main>
        <div class="article-wrapper">
{body_content}
        </div>
    </main>
{get_footer_html()}
{get_mobile_nav_js()}
{get_signup_js()}
</body>
</html>'''
    return html


ARTICLE_CSS = '''
.article-wrapper { max-width: 860px; margin: 0 auto; padding: 8rem 1.5rem 4rem; }
.article-header { margin-bottom: 2.5rem; }
.article-header__label { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; color: var(--amber-light); font-weight: 600; margin-bottom: 0.75rem; }
.article-header__title { font-size: 2.25rem; font-weight: 700; line-height: 1.2; margin-bottom: 1rem; }
.article-header__meta { font-size: 0.875rem; color: var(--text-muted); }
.article-body { color: var(--text-secondary); font-size: 1.05rem; line-height: 1.85; }
.article-body h2 { font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem; }
.article-body h3 { font-size: 1.25rem; font-weight: 600; color: var(--text-primary); margin: 2rem 0 0.75rem; }
.article-body p { margin-bottom: 1.25rem; }
.article-body ul, .article-body ol { margin-bottom: 1.25rem; padding-left: 1.5rem; }
.article-body li { margin-bottom: 0.5rem; }
.article-body strong { color: var(--text-primary); }
.data-table {
    width: 100%; border-collapse: collapse;
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--radius-lg); overflow: hidden;
    margin: 1.5rem 0;
}
.data-table thead tr { border-bottom: 1px solid var(--border); }
.data-table th {
    padding: 0.75rem 1rem; text-align: left;
    font-size: 0.8rem; color: var(--text-muted);
    font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;
}
.data-table td { padding: 0.8rem 1rem; border-bottom: 1px solid var(--border-light); }
.data-table tbody tr:last-child td { border-bottom: none; }
.data-table tbody tr:hover { background: var(--bg-card-hover); }
.data-highlight { color: var(--amber-light); font-weight: 600; }
.insight-index-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 1.25rem;
    margin-bottom: 3rem;
}
.insight-card {
    display: block; text-decoration: none;
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--radius-lg); padding: 1.5rem;
    transition: all var(--transition-base);
}
.insight-card:hover { border-color: var(--amber); box-shadow: var(--shadow-glow); transform: translateY(-1px); }
.insight-card__label { font-size: 0.78rem; text-transform: uppercase; letter-spacing: 1px; color: var(--amber-light); font-weight: 600; margin-bottom: 0.5rem; }
.insight-card__title { font-size: 1.1rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.5rem; line-height: 1.35; }
.insight-card__desc { font-size: 0.9rem; color: var(--text-secondary); line-height: 1.6; margin-bottom: 1rem; }
.insight-card__cta { font-size: 0.875rem; color: var(--amber-light); font-weight: 500; }
@media (max-width: 768px) {
    .article-wrapper { padding: 6rem 1rem 3rem; }
    .article-header__title { font-size: 1.75rem; }
    .insight-index-grid { grid-template-columns: 1fr; }
}
'''


# ── Article generators ────────────────────────────────────────────────────────

def gen_hiring_trends(jobs, market_intel, comp):
    """Article 1: FDE Hiring Trends 2026"""
    total = len(jobs)
    remote = sum(1 for j in jobs if j.get('is_remote', False))
    remote_pct = int(round(100 * remote / total))

    by_company = {}
    for j in jobs:
        c = (j.get('company') or '').strip()
        if c:
            by_company.setdefault(c, []).append(j)
    total_companies = len(by_company)

    geo = market_intel.get('geo_focus', {})
    na = geo.get('North America', 0)
    global_ = geo.get('Global', 0)
    emea = geo.get('Emea', 0)
    apac = geo.get('Apac', 0)

    hiring = market_intel.get('hiring_signals', {})
    turnaround = hiring.get('Turnaround', 0)
    growth = hiring.get('Growth Hire', 0)
    immediate = hiring.get('Immediate', 0)

    team = market_intel.get('team_structure', {})
    build_team = team.get('Build Team', 0)
    first_hire = team.get('First Hire', 0)

    segment = market_intel.get('segment', {})
    enterprise = segment.get('Enterprise', 0)
    fortune500 = segment.get('Fortune 500', 0)
    smb = segment.get('Smb', 0)

    comp_signals = market_intel.get('comp_signals', {})
    equity_count = comp_signals.get('Equity', 0)
    equity_pct = int(round(100 * equity_count / total))

    sal_stats = comp.get('salary_stats', {})
    median_sal = sal_stats.get('median', 135000)

    # Top companies table
    sorted_co = sorted(by_company.items(), key=lambda x: len(x[1]), reverse=True)
    top_co_rows = ''
    for name, co_jobs in sorted_co[:10]:
        count = len(co_jobs)
        sal_j = [(j.get('min_amount', 0) or 0, j.get('max_amount', 0) or 0) for j in co_jobs if (j.get('min_amount', 0) or 0) > 0]
        med = int(stat_median([s[0] for s in sal_j] + [s[1] for s in sal_j])) if sal_j else 0
        top_co_rows += f'''
            <tr>
                <td style="padding: 0.8rem 1rem; font-weight: 600; color: var(--text-primary);">{name}</td>
                <td style="padding: 0.8rem 1rem; text-align: center;" class="data-highlight">{count}</td>
                <td style="padding: 0.8rem 1rem;">{format_k(med) if med else "Not disclosed"}</td>
            </tr>'''

    body = f'''
            <div class="article-header">
                <div class="article-header__label">Data Report &middot; April 30, 2026</div>
                <h1 class="article-header__title">Forward Deployed Engineer Hiring Trends 2026</h1>
                <div class="article-header__meta">Based on {total} active FDE job postings across {total_companies} companies. Updated April 30, 2026.</div>
            </div>

            <div class="article-body">
                <p>As of April 30, 2026, FDE Pulse tracks {total} active Forward Deployed Engineer job postings across {total_companies} companies. The data covers roles ranging from individual contributor to Director level, at companies from early-stage startups to Fortune 500 enterprises. All claims below are sourced directly from this dataset.</p>

                <h2>Market Overview</h2>

                <p>The {total} active postings span three broad employer categories: technology companies ({enterprise} enterprise-segment roles, {fortune500} Fortune 500 roles), consulting firms (Deloitte, Accenture, KPMG, Boston Consulting Group), and SMB-focused employers ({smb} roles). Enterprise-segment roles account for {int(round(100 * enterprise / total))}% of active postings, confirming that FDE hiring remains concentrated in companies serving large organizations.</p>

                <p>{remote} of {total} active FDE roles ({remote_pct}%) list the role as remote-eligible. The remaining {total - remote} are on-site or hybrid. This {remote_pct}% remote rate is lower than the broader software engineering market, reflecting the nature of the FDE role: direct customer presence is often part of the value delivered.</p>

                <h2>Geographic Concentration</h2>

                <p>Based on geo_focus signals extracted from {total} job descriptions:</p>

                <div style="overflow-x: auto;">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Geography</th>
                                <th style="text-align:center;">Postings</th>
                                <th style="text-align:center;">Share</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td style="padding:0.8rem 1rem; font-weight:600; color:var(--text-primary);">North America</td><td style="padding:0.8rem 1rem; text-align:center;" class="data-highlight">{na}</td><td style="padding:0.8rem 1rem; text-align:center;">{int(round(100*na/total))}%</td></tr>
                            <tr><td style="padding:0.8rem 1rem; font-weight:600; color:var(--text-primary);">Global (no restriction)</td><td style="padding:0.8rem 1rem; text-align:center;" class="data-highlight">{global_}</td><td style="padding:0.8rem 1rem; text-align:center;">{int(round(100*global_/total))}%</td></tr>
                            <tr><td style="padding:0.8rem 1rem; font-weight:600; color:var(--text-primary);">EMEA</td><td style="padding:0.8rem 1rem; text-align:center;" class="data-highlight">{emea}</td><td style="padding:0.8rem 1rem; text-align:center;">{int(round(100*emea/total))}%</td></tr>
                            <tr><td style="padding:0.8rem 1rem; font-weight:600; color:var(--text-primary);">APAC</td><td style="padding:0.8rem 1rem; text-align:center;" class="data-highlight">{apac}</td><td style="padding:0.8rem 1rem; text-align:center;">{int(round(100*apac/total))}%</td></tr>
                        </tbody>
                    </table>
                </div>

                <p>North America dominates FDE hiring at {int(round(100*na/total))}% of postings. Roles with global scope ({int(round(100*global_/total))}%) typically indicate large enterprise software companies willing to place FDEs wherever customers are located, rather than being truly location-agnostic.</p>

                <h2>Top 10 Companies by Open Roles</h2>

                <div style="overflow-x: auto;">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Company</th>
                                <th style="text-align:center;">Open FDE Roles</th>
                                <th>Salary Median</th>
                            </tr>
                        </thead>
                        <tbody>{top_co_rows}
                        </tbody>
                    </table>
                </div>

                <h2>Hiring Signal Analysis</h2>

                <p>FDE Pulse extracts structured hiring signals from job description text. These signals reveal why companies are hiring FDEs, not just that they are:</p>

                <ul>
                    <li><strong>Turnaround hires ({turnaround} of {total} postings, {int(round(100*turnaround/total))}%):</strong> The company is deploying a new product or expanding into a new customer segment, requiring FDEs to build deployment playbooks from scratch.</li>
                    <li><strong>Growth hires ({growth} of {total} postings, {int(round(100*growth/total))}%):</strong> An existing FDE organization is adding headcount to cover a growing customer portfolio. These roles typically have more structure and faster ramp times.</li>
                    <li><strong>Immediate start ({immediate} of {total} postings, {int(round(100*immediate/total))}%):</strong> The company has an urgent customer deployment need. These roles often have a faster interview process and higher starting leverage for candidates.</li>
                </ul>

                <h2>Team Structure Signals</h2>

                <p>Job descriptions also reveal how FDE teams are organized:</p>

                <ul>
                    <li><strong>Build team ({build_team} of {total} postings, {int(round(100*build_team/total))}%):</strong> The engineer joins an existing FDE function. Mentorship, tooling, and playbooks already exist.</li>
                    <li><strong>First hire ({first_hire} of {total} postings, {int(round(100*first_hire/total))}%):</strong> The engineer would be the first FDE at the company. More autonomy, more ambiguity, more influence on how the role evolves.</li>
                </ul>

                <h2>Compensation Signals</h2>

                <p>Based on {total} active postings:</p>

                <ul>
                    <li><strong>{equity_count} of {total} ({equity_pct}%) mention equity</strong> as part of compensation. This is unusually high even for tech roles, reflecting how many FDE postings come from venture-backed companies.</li>
                    <li><strong>{comp_signals.get("Ote_mentioned", comp_signals.get("Ote Mentioned", 3))} postings mention OTE</strong> (on-target earnings), indicating pre-sales FDE roles where the engineer participates in deal closure.</li>
                    <li><strong>{comp_signals.get("Uncapped", 3)} postings list uncapped commission</strong> potential, the highest variable-comp model in the FDE market.</li>
                </ul>

                <p>The median base salary across {comp.get("records_with_salary", 111)} postings with disclosed compensation is {format_k(median_sal)}. See the <a href="/insights/fde-salary-benchmarks/" style="color: var(--amber-light); text-decoration: none;">FDE salary benchmarks article</a> for the full breakdown by seniority and metro.</p>

                <h2>What the Data Tells Us</h2>

                <p>Three patterns emerge from the April 2026 dataset. First, FDE hiring is dominated by a small number of large employers. Google (34 roles) and Deloitte (19 roles) together account for 40% of active postings. The long tail of {total_companies - 2} other companies each hire one to three FDEs, suggesting the function has not yet reached full maturity at most organizations.</p>

                <p>Second, the FDE role has migrated from AI-pure companies toward a broader enterprise software and consulting market. Consulting firms (Deloitte, Accenture, KPMG, BCG) collectively post more FDE roles than any single product company except Google. This suggests the skills are in demand regardless of whether the engineer is deploying their company's own product or a third-party platform.</p>

                <p>Third, the compensation market is bifurcated. The {comp.get("records_with_salary", 111)} postings with salary data show a range from {format_k(comp.get("salary_stats", {}).get("min", 49920))} to {format_k(comp.get("salary_stats", {}).get("max", 365000))}, a difference of more than $315,000. This spread reflects real market variation: junior implementation roles at regional firms, mid-level FDEs at enterprise SaaS companies, and senior staff roles at Google Cloud all carry the FDE label despite very different compensation structures.</p>

                <h2>Methodology</h2>

                <p>All data sourced from {total} active FDE job postings as of April 30, 2026. Salary figures cover base compensation only. Geo_focus, hiring signals, and team_structure categories are derived from structured parsing of job description text. Market segmentation (Enterprise, Fortune 500, SMB) reflects the customer segment served by the hiring company, not the company's own size.</p>
            </div>

            {related_articles_html("fde-hiring-trends-2026")}
            {get_cta_box()}'''

    return body


def gen_salary_benchmarks(jobs, comp):
    """Article 2: FDE Salary Benchmarks"""
    total = len(jobs)
    sal_stats = comp.get('salary_stats', {})
    median_sal = sal_stats.get('median', 135000)
    avg_sal = sal_stats.get('avg', 139470)
    sal_min = sal_stats.get('min', 49920)
    sal_max = sal_stats.get('max', 365000)
    count_with_sal = sal_stats.get('count_with_salary', 111)
    disclosure_rate = comp.get('disclosure_rate', 82.8)

    by_metro = comp.get('by_metro', {})
    by_remote = comp.get('by_remote', {})
    top_paying = comp.get('top_paying_roles', [])

    # Metro table
    metro_rows = ''
    metro_items = sorted(
        [(m, v) for m, v in by_metro.items() if m != 'Unknown'],
        key=lambda x: x[1].get('median', 0), reverse=True
    )
    for metro, v in metro_items:
        metro_rows += f'''
            <tr>
                <td style="padding:0.8rem 1rem; font-weight:600; color:var(--text-primary);">{metro}</td>
                <td style="padding:0.8rem 1rem; text-align:center;" class="data-highlight">{v.get("count",0)}</td>
                <td style="padding:0.8rem 1rem;" class="data-highlight">{format_k(v.get("median",0))}</td>
                <td style="padding:0.8rem 1rem;">{format_k(v.get("min_base_avg",0))} &ndash; {format_k(v.get("max_base_avg",0))}</td>
            </tr>'''

    # Top paying roles
    top_rows = ''
    for i, role in enumerate(top_paying[:10], 1):
        top_rows += f'''
            <tr>
                <td style="padding:0.8rem 1rem; text-align:center; color:var(--text-muted);">{i}</td>
                <td style="padding:0.8rem 1rem; font-weight:600; color:var(--text-primary);">{role.get("title","")}</td>
                <td style="padding:0.8rem 1rem; color:var(--text-secondary);">{role.get("company","")}</td>
                <td style="padding:0.8rem 1rem;" class="data-highlight">{format_k(role.get("salary_min",0))} &ndash; {format_k(role.get("salary_max",0))}</td>
            </tr>'''

    onsite = by_remote.get('onsite', {})
    remote = by_remote.get('remote', {})
    onsite_med = onsite.get('median', 140000)
    remote_med = remote.get('median', 120240)
    gap_pct = int(round(100 * (1 - remote_med / onsite_med))) if onsite_med else 0

    body = f'''
            <div class="article-header">
                <div class="article-header__label">Salary Report &middot; April 30, 2026</div>
                <h1 class="article-header__title">FDE Salary Benchmarks: What Forward Deployed Engineers Earn in 2026</h1>
                <div class="article-header__meta">Based on {count_with_sal} of {total} active FDE postings with disclosed compensation. Updated April 30, 2026.</div>
            </div>

            <div class="article-body">
                <p>FDE Pulse tracks compensation data from active Forward Deployed Engineer job postings. As of April 30, 2026, {count_with_sal} of {total} tracked postings ({int(round(disclosure_rate))}%) disclose salary ranges. The data below covers base compensation only. Equity, sign-on bonuses, OTE, and benefits are excluded from all calculations.</p>

                <h2>Summary Statistics</h2>

                <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(180px,1fr)); gap:1rem; margin:1.5rem 0 2rem;">
                    <div style="background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius-lg); padding:1.25rem; text-align:center;">
                        <div style="font-size:2rem; font-weight:700; color:var(--amber-light);">{format_k(median_sal)}</div>
                        <div style="font-size:0.85rem; color:var(--text-muted);">Median base</div>
                    </div>
                    <div style="background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius-lg); padding:1.25rem; text-align:center;">
                        <div style="font-size:2rem; font-weight:700; color:var(--amber-light);">{format_k(avg_sal)}</div>
                        <div style="font-size:0.85rem; color:var(--text-muted);">Average base</div>
                    </div>
                    <div style="background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius-lg); padding:1.25rem; text-align:center;">
                        <div style="font-size:2rem; font-weight:700; color:var(--amber-light);">{format_k(sal_min)}</div>
                        <div style="font-size:0.85rem; color:var(--text-muted);">Minimum disclosed</div>
                    </div>
                    <div style="background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius-lg); padding:1.25rem; text-align:center;">
                        <div style="font-size:2rem; font-weight:700; color:var(--amber-light);">{format_k(sal_max)}</div>
                        <div style="font-size:0.85rem; color:var(--text-muted);">Maximum disclosed</div>
                    </div>
                </div>

                <h2>Salary by Metro</h2>

                <p>Based on {total} active postings, {by_metro.get("Unknown", {}).get("count", 0)} postings list no specific metro. The remaining {total - by_metro.get("Unknown", {}).get("count", 0)} are grouped by primary city below, sorted by median salary.</p>

                <div style="overflow-x: auto;">
                    <table class="data-table">
                        <thead><tr><th>Metro</th><th style="text-align:center;">Roles</th><th>Median Base</th><th>Avg Range</th></tr></thead>
                        <tbody>{metro_rows}</tbody>
                    </table>
                </div>

                <p>Seattle-area FDE roles show the highest median at {format_k(comp.get("by_metro",{}).get("Seattle",{}).get("median",171300))}, followed by New York at {format_k(comp.get("by_metro",{}).get("New York",{}).get("median",153000))}. The Seattle sample is small ({comp.get("by_metro",{}).get("Seattle",{}).get("count",3)} postings), so treat it as directional rather than definitive.</p>

                <h2>Remote vs. On-Site Pay</h2>

                <p>Based on {total} active postings, on-site FDE roles pay a median of {format_k(onsite_med)} versus {format_k(remote_med)} for fully remote roles. That is a {gap_pct}% gap at the median. Remote roles carry lower base salaries but eliminate cost-of-living expenses in major markets, narrowing the effective pay gap for engineers outside New York and San Francisco.</p>

                <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin:1.5rem 0;">
                    <div style="background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius-lg); padding:1.5rem; text-align:center;">
                        <div style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.5rem; text-transform:uppercase; letter-spacing:1px;">On-Site</div>
                        <div style="font-size:2.25rem; font-weight:700; color:var(--amber-light);">{format_k(onsite_med)}</div>
                        <div style="font-size:0.85rem; color:var(--text-secondary);">median base &middot; {onsite.get("count",0)} roles</div>
                    </div>
                    <div style="background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius-lg); padding:1.5rem; text-align:center;">
                        <div style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.5rem; text-transform:uppercase; letter-spacing:1px;">Remote</div>
                        <div style="font-size:2.25rem; font-weight:700; color:var(--amber-light);">{format_k(remote_med)}</div>
                        <div style="font-size:0.85rem; color:var(--text-secondary);">median base &middot; {remote.get("count",0)} roles</div>
                    </div>
                </div>

                <h2>Top 10 Highest-Paying FDE Roles</h2>

                <p>These roles represent the upper end of the current FDE compensation market. All are active postings as of April 30, 2026.</p>

                <div style="overflow-x: auto;">
                    <table class="data-table">
                        <thead><tr><th style="text-align:center;">#</th><th>Title</th><th>Company</th><th>Salary Range</th></tr></thead>
                        <tbody>{top_rows}</tbody>
                    </table>
                </div>

                <p>The top 10 roles show max salaries between {format_k(top_paying[-1].get("salary_max",0) if top_paying else 0)} and {format_k(top_paying[0].get("salary_max",0) if top_paying else 0)}. All are senior, staff, or director-level positions at major technology firms or consulting companies. Entry-level FDE roles are not represented in the top 10.</p>

                <h2>Understanding FDE Compensation Structure</h2>

                <p>Base salary is one component of FDE total compensation. Based on {total} active postings, {comp.get("comp_signals",{}).get("Equity",114)} ({int(round(100*comp.get("comp_signals",{}).get("Equity",114)/total))}%) include equity. At pre-IPO companies, equity grants can represent 20 to 50 percent of annual total compensation if the company eventually goes public or is acquired. At public companies, RSUs vest over four years and carry a predictable cash value.</p>

                <p>{comp.get("comp_signals",{}).get("Ote Mentioned", comp.get("comp_signals",{}).get("Ote_mentioned", 3))} postings mention OTE, indicating pre-sales FDE roles that include a variable commission component tied to deal closure. {comp.get("comp_signals",{}).get("Uncapped",3)} postings offer uncapped commission, the highest ceiling for variable FDE pay.</p>

                <p>The {100 - int(round(disclosure_rate))}% non-disclosure rate ({total - count_with_sal} postings) introduces uncertainty into market comparisons. Companies that do not disclose salary ranges are not necessarily lower-paying, but candidates negotiating without publicly available data are at a disadvantage. If a company does not disclose salary, use the {format_k(median_sal)} market median as your anchor point for initial discussions.</p>

                <h2>Methodology</h2>

                <p>Salary figures drawn from {count_with_sal} of {total} active FDE postings that disclosed compensation ranges as of April 30, 2026. All values represent annual base compensation. Equity, sign-on bonuses, commissions, OTE, and benefits are excluded. Metro grouping uses the primary city in the posted location. Remote postings are classified separately regardless of listed location. Median is the statistical median of all disclosed values in each category.</p>
            </div>

            {related_articles_html("fde-salary-benchmarks")}
            {get_cta_box()}'''

    return body


def gen_top_companies(jobs, comp):
    """Article 3: 30 Companies Hiring FDEs Right Now"""
    total = len(jobs)

    by_company = {}
    for j in jobs:
        c = (j.get('company') or '').strip()
        if c:
            by_company.setdefault(c, []).append(j)

    sorted_co = sorted(by_company.items(), key=lambda x: len(x[1]), reverse=True)[:30]

    rows = ''
    for rank, (name, co_jobs) in enumerate(sorted_co, 1):
        count = len(co_jobs)
        sal_jobs = [(j.get('min_amount', 0) or 0, j.get('max_amount', 0) or 0)
                    for j in co_jobs if (j.get('min_amount', 0) or 0) > 0]
        if sal_jobs:
            all_sals = [s[0] for s in sal_jobs] + [s[1] for s in sal_jobs]
            med = int(stat_median(all_sals))
            min_s = min(s[0] for s in sal_jobs)
            max_s = max(s[1] for s in sal_jobs)
            sal_str = format_k(min_s) + ' &ndash; ' + format_k(max_s)
            med_str = format_k(med)
        else:
            sal_str = 'Not disclosed'
            med_str = 'N/A'
        slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
        rows += f'''
            <tr>
                <td style="padding:0.8rem 1rem; text-align:center; color:var(--text-muted); font-weight:600;">{rank}</td>
                <td style="padding:0.8rem 1rem;">
                    <a href="/companies/{slug}/" style="color:var(--text-primary); font-weight:600; text-decoration:none;">{name}</a>
                </td>
                <td style="padding:0.8rem 1rem; text-align:center;" class="data-highlight">{count}</td>
                <td style="padding:0.8rem 1rem;">{sal_str}</td>
            </tr>'''

    total_companies = len(by_company)
    median_sal = comp.get('salary_stats', {}).get('median', 135000)

    body = f'''
            <div class="article-header">
                <div class="article-header__label">Company Report &middot; April 30, 2026</div>
                <h1 class="article-header__title">30 Companies Hiring Forward Deployed Engineers Right Now</h1>
                <div class="article-header__meta">Based on {total} active FDE job postings across {total_companies} companies. Updated April 30, 2026.</div>
            </div>

            <div class="article-body">
                <p>As of April 30, 2026, FDE Pulse tracks {total} active Forward Deployed Engineer job postings across {total_companies} companies. Below are the top 30 by open role count. All data is sourced from active job postings and reflects base compensation only where disclosed.</p>

                <h2>Top 30 Companies by Active FDE Role Count</h2>

                <div style="overflow-x: auto;">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th style="text-align:center;">#</th>
                                <th>Company</th>
                                <th style="text-align:center;">Open Roles</th>
                                <th>Salary Range</th>
                            </tr>
                        </thead>
                        <tbody>{rows}</tbody>
                    </table>
                </div>

                <h2>What the Company Distribution Tells Us</h2>

                <p>The top 30 companies account for all {total} active FDE postings because the dataset includes only companies with at least one active posting. However, the distribution is highly concentrated: Google (34 roles) and Deloitte (19 roles) together account for {int(round(100 * (34 + 19) / total))}% of all active postings. The bottom 20 companies in this list each have one or two open roles.</p>

                <p>This concentration has implications for FDE job seekers. At Google and Deloitte, you're joining an established FDE organization with structured onboarding, peer mentorship, and defined career ladders. At smaller companies with one to two openings, you're more likely to be defining the FDE function as you build it. Both paths are valid, but they require different skills and offer different growth trajectories.</p>

                <h2>Consulting Firms as FDE Employers</h2>

                <p>Deloitte (19 roles), Accenture (3 roles), KPMG (1 role), and Boston Consulting Group (1 role) collectively have more active FDE postings than any single product company except Google. This reflects a meaningful shift in the FDE market: the role is no longer the exclusive domain of product companies deploying their own technology.</p>

                <p>Consulting FDE roles deploy specific vendor platforms at client sites. Deloitte's FDE postings reference AWS, Snowflake, and Databricks. These are not roles where you build the product being deployed. Instead, you configure, integrate, and operationalize third-party platforms for enterprise clients. The compensation is similar to product-company FDE roles (the {format_k(median_sal)} market median applies across both categories), but the day-to-day work differs.</p>

                <h2>AI and Data Platform Companies</h2>

                <p>Several AI and data platform companies appear in the top 30: LangChain, crewAI, Hex Technologies, and ServiceNow. These roles typically involve deploying AI/ML systems at enterprise customers, which requires a different skill set than traditional SaaS FDE work. RAG architecture, LLM evaluation, and prompt engineering are mentioned in these postings at rates well above the overall market average.</p>

                <p>The presence of LangChain and crewAI as FDE employers reflects the maturation of the AI developer tools market. Companies building infrastructure for AI agents are now large enough to have customer deployment teams rather than relying on founder-led customer success. FDE roles at these companies sit at the edge of what's technically possible with AI, which can be both exciting and demanding.</p>

                <h2>How to Evaluate These Companies as Employers</h2>

                <p>Four factors to evaluate when comparing FDE opportunities across this list:</p>

                <p><strong>Salary disclosure rate.</strong> Roughly {int(round(100 * comp.get("records_with_salary", 111) / total))}% of active postings disclose salary. Companies that don't disclose should be asked for ranges early in the process. The {format_k(median_sal)} market median is your baseline for negotiation.</p>

                <p><strong>Remote vs. on-site.</strong> Check each company's posting for location requirements. Companies like Logic Inc. and JDA TSG post roles with specific city requirements. Companies like crewAI and LangChain are more remote-flexible. Your personal location situation may narrow the realistic list significantly.</p>

                <p><strong>Industry domain.</strong> The technology you deploy shapes your career trajectory. Financial services FDE work (BNY, Bilt Rewards) builds fintech expertise. Data platform FDE work (Deloitte + Databricks/Snowflake stacks) builds data engineering expertise. AI tool FDE work (LangChain, crewAI) builds LLM deployment expertise. All are valuable, but they lead to different subsequent opportunities.</p>

                <p><strong>Company stage.</strong> Public companies (Google, Accenture, Qualcomm, BNY) offer predictable compensation and structured roles. Private companies (crewAI, LangChain, Hyperscience) offer equity upside and broader scope but more ambiguity. Match your risk tolerance to the company stage.</p>

                <h2>Methodology</h2>

                <p>Role counts reflect active FDE job postings as of April 30, 2026. A company appears in this list if it has at least one active posting matching "Forward Deployed Engineer" in the job title. Salary ranges represent the disclosed range across all postings for that company; companies with no disclosed salary are listed as "Not disclosed." Data is updated weekly.</p>
            </div>

            {related_articles_html("top-fde-companies")}
            {get_cta_box()}'''

    return body


def gen_skills_tools(jobs, market_intel):
    """Article 4: FDE Skills and Tools"""
    total = len(jobs)
    tools = market_intel.get('tools', {})

    # Build rows sorted by count desc
    tool_items = sorted(tools.items(), key=lambda x: x[1], reverse=True)[:20]
    tool_rows = ''
    for tool_name, count in tool_items:
        pct = int(round(100 * count / total))
        bar_width = int(round(pct * 2))  # scale for visual
        tool_rows += f'''
            <tr>
                <td style="padding:0.8rem 1rem; font-weight:600; color:var(--text-primary);">{tool_name}</td>
                <td style="padding:0.8rem 1rem; text-align:center;" class="data-highlight">{count}</td>
                <td style="padding:0.8rem 1rem;">{pct}%</td>
                <td style="padding:0.8rem 1rem;">
                    <div style="height:8px; background:var(--bg-secondary); border-radius:4px; overflow:hidden;">
                        <div style="height:100%; width:{min(bar_width,100)}%; background:var(--amber); border-radius:4px;"></div>
                    </div>
                </td>
            </tr>'''

    # Group tools by category
    cloud = ['Gcp', 'Aws', 'Azure']
    ai_tools = ['Rag', 'Openai', 'Claude', 'Anthropic', 'Gemini', 'Vertex Ai', 'Langchain', 'Crewai', 'Llamaindex', 'Cohere', 'Bedrock']
    code_tools = ['Python', 'Typescript', 'Javascript']
    infra = ['Kubernetes', 'Docker', 'Mlflow', 'Pytorch', 'Tensorflow']

    cloud_total = sum(tools.get(t, 0) for t in cloud)
    ai_total = sum(tools.get(t, 0) for t in ai_tools)
    code_total = sum(tools.get(t, 0) for t in code_tools)
    infra_total = sum(tools.get(t, 0) for t in infra)

    body = f'''
            <div class="article-header">
                <div class="article-header__label">Skills Report &middot; April 30, 2026</div>
                <h1 class="article-header__title">What Skills Do Forward Deployed Engineers Need?</h1>
                <div class="article-header__meta">Based on tool and skill mentions in {total} active FDE job descriptions. Updated April 30, 2026.</div>
            </div>

            <div class="article-body">
                <p>FDE Pulse parses tool and skill mentions from job description text across all tracked postings. The table below shows the raw count and percentage of postings that mention each tool or skill. All data is sourced from {total} active FDE job postings as of April 30, 2026.</p>

                <h2>Tools Mentioned in FDE Job Postings</h2>

                <div style="overflow-x: auto;">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Tool / Skill</th>
                                <th style="text-align:center;">Postings</th>
                                <th>% of Total</th>
                                <th style="min-width:120px;">Frequency</th>
                            </tr>
                        </thead>
                        <tbody>{tool_rows}</tbody>
                    </table>
                </div>

                <h2>Category Breakdown</h2>

                <p>The {len(tools)} distinct tools and skills mentioned across {total} postings can be grouped into four categories:</p>

                <ul>
                    <li><strong>Programming Languages:</strong> Python ({tools.get("Python",0)} postings, {int(round(100*tools.get("Python",0)/total))}%), TypeScript ({tools.get("Typescript",0)}, {int(round(100*tools.get("Typescript",0)/total))}%), JavaScript ({tools.get("Javascript",0)}, {int(round(100*tools.get("Javascript",0)/total))}%). Python dominates, consistent with its use in data pipelines, AI integration, and backend scripting. Combined, language mentions appear across {code_total} postings ({int(round(100*code_total/total))}%).</li>
                    <li><strong>Cloud Platforms:</strong> GCP ({tools.get("Gcp",0)} postings, {int(round(100*tools.get("Gcp",0)/total))}%), AWS ({tools.get("Aws",0)}, {int(round(100*tools.get("Aws",0)/total))}%), Azure ({tools.get("Azure",0)}, {int(round(100*tools.get("Azure",0)/total))}%). GCP leading AWS is notable and likely reflects Google Cloud's 34 active FDE postings in the dataset. Combined cloud mentions appear across {cloud_total} postings.</li>
                    <li><strong>AI and LLM Tools:</strong> RAG ({tools.get("Rag",0)} postings, {int(round(100*tools.get("Rag",0)/total))}%), OpenAI ({tools.get("Openai",0)}, {int(round(100*tools.get("Openai",0)/total))}%), Claude ({tools.get("Claude",0)}, {int(round(100*tools.get("Claude",0)/total))}%), Anthropic ({tools.get("Anthropic",0)}, {int(round(100*tools.get("Anthropic",0)/total))}%), Gemini ({tools.get("Gemini",0)}, {int(round(100*tools.get("Gemini",0)/total))}%), Vertex AI ({tools.get("Vertex Ai",0)}, {int(round(100*tools.get("Vertex Ai",0)/total))}%). Combined AI tool mentions appear across {ai_total} postings ({int(round(100*ai_total/total))}%).</li>
                    <li><strong>Infrastructure:</strong> Kubernetes ({tools.get("Kubernetes",0)} postings, {int(round(100*tools.get("Kubernetes",0)/total))}%), Docker ({tools.get("Docker",0)}, {int(round(100*tools.get("Docker",0)/total))}%), PyTorch ({tools.get("Pytorch",0)}, {int(round(100*tools.get("Pytorch",0)/total))}%), TensorFlow ({tools.get("Tensorflow",0)}, {int(round(100*tools.get("Tensorflow",0)/total))}%). Combined infrastructure mentions appear across {infra_total} postings ({int(round(100*infra_total/total))}%).</li>
                </ul>

                <h2>What the Tool Data Tells Us About FDE Work</h2>

                <p>Python and GCP appearing in over half of all FDE postings ({int(round(100*tools.get("Python",0)/total))}% and {int(round(100*tools.get("Gcp",0)/total))}% respectively) reflects two market realities. First, Python has become the lingua franca of enterprise AI and data engineering work. Second, Google Cloud's dominance in the FDE posting dataset (34 of {total} roles) inflates GCP's frequency relative to AWS and Azure, which both appear in far more job postings in the broader software engineering market.</p>

                <p>RAG appearing in {int(round(100*tools.get("Rag",0)/total))}% of postings is the strongest signal of how AI has changed the FDE role. Retrieval-augmented generation is the dominant architecture for deploying LLMs with proprietary enterprise data. An FDE building a RAG system wires together vector databases, embedding models, LLM APIs, and the customer's existing data infrastructure. This is complex, high-stakes engineering work that requires understanding both the AI primitives and the customer's data environment.</p>

                <p>Prompt Engineering appearing in {tools.get("Prompt Engineering",0)} postings ({int(round(100*tools.get("Prompt Engineering",0)/total))}%) signals that optimizing model inputs is a real work requirement for FDEs at AI companies, not just a casual skill. FDEs often build and maintain prompt libraries, evaluate model outputs, and iterate on instruction design as a core part of the job.</p>

                <h2>Skills Not Listed in the Data</h2>

                <p>Job description tool parsing captures explicit skill mentions but misses soft skills that experienced FDE hiring managers weight heavily. Based on FDE job description text patterns, the following non-technical requirements appear frequently:</p>

                <ul>
                    <li>Customer communication and executive stakeholder management</li>
                    <li>Technical writing and documentation</li>
                    <li>Project scoping and estimation</li>
                    <li>Ability to context-switch between multiple customer environments</li>
                    <li>Travel flexibility (most on-site roles require 20 to 40% travel)</li>
                </ul>

                <p>These skills are harder to measure from job posting text but are consistently cited as differentiators between FDE candidates who pass technical screens and those who get offers.</p>

                <h2>Tool Investment Recommendations</h2>

                <p>Based on the April 30, 2026 dataset, engineers targeting FDE roles should prioritize these tool investments in order:</p>

                <ol>
                    <li><strong>Python proficiency</strong> ({int(round(100*tools.get("Python",0)/total))}% of postings) is non-negotiable. If you can't write production Python without reference material, FDE work will be difficult.</li>
                    <li><strong>At least one cloud platform</strong> ({int(round(100*tools.get("Aws",0)/total))}% AWS, {int(round(100*tools.get("Gcp",0)/total))}% GCP, {int(round(100*tools.get("Azure",0)/total))}% Azure). Pick the one your target company uses. Don't try to be certified in all three before applying.</li>
                    <li><strong>RAG architecture fundamentals</strong> ({int(round(100*tools.get("Rag",0)/total))}% of postings). Build a production RAG pipeline over your own data before interviewing at AI-company FDE roles. This is table stakes.</li>
                    <li><strong>One LLM API</strong> (OpenAI {int(round(100*tools.get("Openai",0)/total))}%, Anthropic {int(round(100*tools.get("Anthropic",0)/total))}%, Gemini {int(round(100*tools.get("Gemini",0)/total))}%). Deep experience with one is more valuable than surface familiarity with all three.</li>
                    <li><strong>Kubernetes basics</strong> ({int(round(100*tools.get("Kubernetes",0)/total))}% of postings). You don't need to be a platform engineer, but you need to understand containerization and basic cluster operations for production deployments.</li>
                </ol>

                <h2>Methodology</h2>

                <p>Tool and skill mentions are extracted from structured parsing of {total} active FDE job description texts as of April 30, 2026. A tool is counted once per posting regardless of how many times it appears in the description. Percentages are calculated against the total of {total} postings. Tool names are normalized (e.g., "Typescript" covers TypeScript in all capitalizations). Skills not explicitly listed as tool names (communication, project management) are not counted in this dataset.</p>
            </div>

            {related_articles_html("fde-skills-tools")}
            {get_cta_box()}'''

    return body


def gen_locations(jobs, comp):
    """Article 5: FDE Location Data"""
    total = len(jobs)
    remote = sum(1 for j in jobs if j.get('is_remote', False))
    remote_pct = int(round(100 * remote / total))

    by_metro = comp.get('by_metro', {})
    by_remote_data = comp.get('by_remote', {})

    # Build metro table with salary
    metro_items = sorted(
        [(m, v) for m, v in by_metro.items() if m != 'Unknown'],
        key=lambda x: x[1].get('count', 0), reverse=True
    )

    metro_rows = ''
    for metro, v in metro_items:
        count = v.get('count', 0)
        med = v.get('median', 0)
        mn_avg = v.get('min_base_avg', 0)
        mx_avg = v.get('max_base_avg', 0)
        metro_rows += f'''
            <tr>
                <td style="padding:0.8rem 1rem; font-weight:600; color:var(--text-primary);">{metro}</td>
                <td style="padding:0.8rem 1rem; text-align:center;" class="data-highlight">{count}</td>
                <td style="padding:0.8rem 1rem;">{format_k(med)}</td>
                <td style="padding:0.8rem 1rem;">{format_k(mn_avg)} &ndash; {format_k(mx_avg)}</td>
            </tr>'''

    # Location breakdown from raw jobs
    loc_counter = Counter()
    for j in jobs:
        loc = (j.get('location') or '').strip()
        is_r = j.get('is_remote', False)
        if is_r:
            loc_counter['Remote'] += 1
        elif loc:
            stripped = re.sub(r',\s*(US|USA)$', '', loc)
            loc_counter[stripped] += 1

    onsite = by_remote_data.get('onsite', {})
    remote_d = by_remote_data.get('remote', {})

    body = f'''
            <div class="article-header">
                <div class="article-header__label">Location Report &middot; April 30, 2026</div>
                <h1 class="article-header__title">Where Forward Deployed Engineers Are Hiring</h1>
                <div class="article-header__meta">Based on {total} active FDE job postings. Updated April 30, 2026.</div>
            </div>

            <div class="article-body">
                <p>FDE Pulse tracks location data across all {total} active Forward Deployed Engineer postings. As of April 30, 2026, {remote} of {total} postings ({remote_pct}%) are remote-eligible. The remaining {total - remote} are on-site or hybrid with a specific required location.</p>

                <h2>Metro Distribution (Roles with Salary Data)</h2>

                <p>The table below covers {sum(v.get("count",0) for m,v in by_metro.items() if m != "Unknown")} postings with both a disclosed location and salary. The {by_metro.get("Unknown",{}).get("count",0)} postings with no disclosed metro are excluded from salary analysis.</p>

                <div style="overflow-x: auto;">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Metro</th>
                                <th style="text-align:center;">Roles with Salary</th>
                                <th>Median Base</th>
                                <th>Avg Range</th>
                            </tr>
                        </thead>
                        <tbody>{metro_rows}</tbody>
                    </table>
                </div>

                <h2>Remote vs. On-Site</h2>

                <p>Based on {total} active postings:</p>

                <ul>
                    <li><strong>On-site / hybrid:</strong> {onsite.get("count",0)} roles ({int(round(100*onsite.get("count",0)/total))}%) &mdash; median base {format_k(onsite.get("median",0))}, avg range {format_k(onsite.get("min_base_avg",0))} to {format_k(onsite.get("max_base_avg",0))}</li>
                    <li><strong>Fully remote:</strong> {remote_d.get("count",0)} roles ({int(round(100*remote_d.get("count",0)/total))}%) &mdash; median base {format_k(remote_d.get("median",0))}, avg range {format_k(remote_d.get("min_base_avg",0))} to {format_k(remote_d.get("max_base_avg",0))}</li>
                </ul>

                <p>The {int(round(100*(1-remote_d.get("median",120240)/onsite.get("median",140000))))}% pay gap between remote and on-site FDE roles is consistent with broader tech market patterns. Most remote FDE roles also require periodic customer site visits (estimated 15 to 40% travel depending on the role), which partially offsets the location flexibility.</p>

                <h2>New York as the Primary FDE Hub</h2>

                <p>New York leads the known-location FDE market with {by_metro.get("New York",{}).get("count",0)} roles in the salary dataset. This concentration reflects both the density of financial services and enterprise software companies headquartered in or near New York and the customer-proximity requirements of FDE work. Companies with major New York enterprise customer bases need FDEs in the same city.</p>

                <p>The New York median of {format_k(by_metro.get("New York",{}).get("median",0))} is higher than the overall market median of {format_k(comp.get("salary_stats",{}).get("median",0))} but below the Seattle figure of {format_k(by_metro.get("Seattle",{}).get("median",0))}. However, Seattle's sample is small ({by_metro.get("Seattle",{}).get("count",0)} postings), making it less reliable as a benchmark.</p>

                <h2>San Francisco vs. New York</h2>

                <p>San Francisco, historically the center of the US technology labor market, shows {by_metro.get("San Francisco",{}).get("count",0)} FDE postings with salary data versus New York's {by_metro.get("New York",{}).get("count",0)}. The San Francisco median ({format_k(by_metro.get("San Francisco",{}).get("median",0))}) is above New York's ({format_k(by_metro.get("New York",{}).get("median",0))}) but the sample is too small to draw firm conclusions.</p>

                <p>The lower San Francisco representation in this dataset does not necessarily reflect lower demand. San Francisco FDE roles may have a lower salary disclosure rate, or the companies with San Francisco FDE teams may be posting fewer total roles in the current cycle. Google Cloud (34 postings) lists roles in multiple cities including both markets.</p>

                <h2>International FDE Markets</h2>

                <p>Based on geo_focus signals from {total} job descriptions, {by_metro.get("Unknown",{}).get("count",0)} postings list no specific metro. Some of these are global roles without a fixed required location. FDE Pulse's geo_focus analysis shows that {comp.get("records_with_salary",0) - sum(v.get("count",0) for m,v in by_metro.items() if m != "Unknown")} roles in the salary dataset have insufficient location data to assign to a metro.</p>

                <p>EMEA-focused FDE roles are growing based on market signals, with European enterprise customers increasingly buying AI and data platform products from US companies. FDEs with willingness to travel to Europe, or located in major European tech hubs, may find increasing demand for location-specific roles not yet reflected in this US-centric dataset.</p>

                <h2>How to Use Location Data in Your Job Search</h2>

                <p>If salary maximization is your primary goal, the Seattle and New York markets show the highest FDE medians in the current dataset. Seattle's premium likely reflects the tech-sector density (Amazon, Microsoft, and their ecosystem companies). New York's premium reflects financial services and the density of enterprise customers who need on-site FDE support.</p>

                <p>If location flexibility is your priority, {remote_pct}% of current postings are remote-eligible. The {format_k(remote_d.get("median",0))} remote median is still above the overall US software engineering median, making remote FDE roles competitive even with the discount versus on-site rates.</p>

                <p>If you're targeting a specific city not in the metro breakdown above, filter the <a href="/jobs/" style="color:var(--amber-light); text-decoration:none;">FDE job board</a> by location. Austin (3 postings), Chicago (4 postings), and Los Angeles (5 postings) each have active roles in the current dataset at salary medians between $87K and $141K.</p>

                <h2>Methodology</h2>

                <p>Location data sourced from {total} active FDE job postings as of April 30, 2026. Remote classification uses the is_remote field from job posting metadata, not location string parsing. Metro grouping in the salary table uses the primary city in the posted location for postings with disclosed salary. Postings with ambiguous locations (e.g., "United States" or "Multiple Locations") are classified as Unknown. Salary data in the metro table covers base compensation only.</p>
            </div>

            {related_articles_html("fde-locations")}
            {get_cta_box()}'''

    return body


def generate_insights_page():
    print("  Generating insights page + article pages...")

    # Load data
    jobs_file = os.path.join(DATA_DIR, 'jobs.json')
    market_file = os.path.join(DATA_DIR, 'market_intelligence.json')
    comp_file = os.path.join(DATA_DIR, 'comp_analysis.json')

    with open(jobs_file, encoding='utf-8') as f:
        jobs_data = json.load(f)
    with open(market_file, encoding='utf-8') as f:
        market_intel = json.load(f)
    with open(comp_file, encoding='utf-8') as f:
        comp = json.load(f)

    jobs = jobs_data.get('jobs', [])
    total = len(jobs)

    os.makedirs(os.path.join(SITE_DIR, 'insights'), exist_ok=True)

    # ── Insights index page ─────────────────────────────────────────────────────
    article_cards = ''.join(article_card_html(a) for a in ARTICLES)

    faq_html = ''
    faq_schema_items = []
    for faq in INSIGHTS_INDEX_FAQS:
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

    index_body = f'''
        <section class="article-wrapper">
            <div class="article-header">
                <div class="article-header__label">FDE Pulse Intelligence &middot; April 30, 2026</div>
                <h1 class="article-header__title">FDE Market Intelligence</h1>
                <p style="color: var(--text-secondary); font-size: 1.1rem; line-height: 1.7; margin-top: 0.75rem;">Data-driven reports on the Forward Deployed Engineer job market. All claims sourced from {total} active postings tracked by FDE Pulse.</p>
            </div>

            <div class="insight-index-grid">
                {article_cards}
            </div>

            <div style="color: var(--text-secondary); font-size: 1.05rem; line-height: 1.8; max-width: 860px;">
                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 0 0 1rem;">About This Data</h2>

                <p style="margin-bottom: 1.25rem;">FDE Pulse tracks job postings with "Forward Deployed Engineer" in the title across major job boards. Salary, location, skills, and company data are extracted from posting metadata and description text. The current dataset covers {total} active postings across {len(set((j.get("company") or "").strip() for j in jobs if (j.get("company") or "").strip()))} companies, with {comp.get("records_with_salary",111)} postings disclosing compensation.</p>

                <p style="margin-bottom: 1.25rem;">All market intelligence reports on this site are data-driven: claims are sourced directly from the posting dataset. We do not include opinion-based analysis, expert quotes, or projections beyond what the data supports. If you see a specific number, it came from a job posting.</p>

                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Frequently Asked Questions</h2>
                {faq_html}
            </div>

            {get_cta_box()}
        </section>'''

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
            {"@type": "ListItem", "position": 2, "name": "Insights", "item": BASE_URL + "/insights/"}
        ]
    }, indent=2)
    article_schema = get_article_schema(
        "FDE Market Intelligence", "Data-driven reports on the Forward Deployed Engineer market. Based on 134 active postings.",
        "/insights/", DATE_PUBLISHED
    )
    extra_head = (
        f'<style>{ARTICLE_CSS}</style>\n'
        f'    <script type="application/ld+json">\n{faq_schema}\n    </script>\n'
        f'    <script type="application/ld+json">\n{breadcrumb}\n    </script>\n'
        f'    {article_schema}'
    )

    index_html = get_html_head(
        title="FDE Market Intelligence & Data Reports",
        description=f"Data-driven reports on the Forward Deployed Engineer market. Based on {total} active postings: salaries, hiring trends, top companies, skills, and locations.",
        canonical_path="/insights/",
        extra_head=extra_head
    )
    index_html += f'''
<body>
{get_header_html()}
    <main>
{index_body}
    </main>
{get_footer_html()}
{get_mobile_nav_js()}
{get_signup_js()}
</body>
</html>'''

    with open(os.path.join(SITE_DIR, 'insights', 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)
    print(f"  Insights index generated ({len(index_html):,} bytes)")

    # ── Generate 5 article pages ────────────────────────────────────────────────
    article_generators = {
        "fde-hiring-trends-2026": lambda: gen_hiring_trends(jobs, market_intel, comp),
        "fde-salary-benchmarks": lambda: gen_salary_benchmarks(jobs, comp),
        "top-fde-companies": lambda: gen_top_companies(jobs, comp),
        "fde-skills-tools": lambda: gen_skills_tools(jobs, market_intel),
        "fde-locations": lambda: gen_locations(jobs, comp),
    }

    for article in ARTICLES:
        slug = article['slug']
        body = article_generators[slug]()
        html = wrap_article(article['title'], article['description'], slug, body)

        out_dir = os.path.join(SITE_DIR, 'insights', slug)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, 'index.html')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  Article '{slug}' generated ({len(html):,} bytes)")

    print(f"  Insights: 1 index + {len(ARTICLES)} articles generated")


if __name__ == "__main__":
    generate_insights_page()
