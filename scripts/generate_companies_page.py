#!/usr/bin/env python3
"""Generate the Companies landing page for FDE Pulse using real jobs.json data."""

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

FAQS = [
    {
        "q": "Which company is hiring the most Forward Deployed Engineers right now?",
        "a": "Based on 134 active FDE postings as of April 30, 2026, Google leads with 34 open roles across their Cloud division. Deloitte is second with 19 active postings. Together, Google and Deloitte account for nearly 40% of all active FDE job postings in the dataset."
    },
    {
        "q": "What types of companies hire Forward Deployed Engineers?",
        "a": "FDE hiring spans tech giants (Google, Amazon Web Services), major consulting firms (Deloitte, Accenture, KPMG, Boston Consulting Group), enterprise software companies (ServiceNow, Smartsheet, FloQast), fintech (BNY, Rippling, Bilt Rewards), and AI-focused startups (crewAI, LangChain, Hex Technologies). The role has spread well beyond Palantir's original model to cover nearly every sector in enterprise software."
    },
    {
        "q": "Do you need to work at a big company to be a Forward Deployed Engineer?",
        "a": "No. Based on current postings, smaller companies like crewAI, LangChain, Hyperscience, and Neara also hire FDEs. Startups typically offer earlier-stage equity and broader scope per role. Larger companies (Google, Deloitte) offer more structured career ladders, training programs, and higher base salaries. Both paths have merit depending on where you are in your career."
    },
    {
        "q": "Are consulting firms real FDE employers?",
        "a": "Yes. Deloitte has 19 active FDE postings in this dataset, ranking second behind Google. Accenture and KPMG each have active FDE roles. Consulting firm FDE roles deploy specific technology platforms (AWS, Snowflake, Databricks) at client sites, which is functionally similar to product-company FDE work. The main difference is that consulting FDEs rotate across clients and platforms rather than specializing in one product."
    },
    {
        "q": "How do I find companies actively hiring FDEs?",
        "a": "FDE Pulse tracks 134 active postings across 70 companies as of April 30, 2026. The /jobs/ section shows every current opening with salary data, location, and direct links to apply. Companies with the most postings include Google (34 roles), Deloitte (19 roles), Amazon Web Services (3), Accenture (3), and Logic Inc. (3)."
    },
]


def make_company_slug(name):
    """Convert company name to URL slug."""
    s = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    return s


def format_k(amount):
    if not amount or amount <= 0:
        return None
    return '$' + str(int(round(amount / 1000))) + 'K'


def generate_companies_page():
    print("  Generating companies page...")

    jobs_file = os.path.join(DATA_DIR, 'jobs.json')
    with open(jobs_file, encoding='utf-8') as f:
        jobs_data = json.load(f)

    jobs = jobs_data.get('jobs', [])
    total_jobs = len(jobs)

    # Build company data from jobs.json
    by_company = {}
    for j in jobs:
        comp = (j.get('company') or '').strip()
        if not comp:
            continue
        if comp not in by_company:
            by_company[comp] = []
        by_company[comp].append(j)

    total_companies = len(by_company)
    avg_roles = round(total_jobs / total_companies, 1) if total_companies else 0

    # Sort companies by role count
    sorted_companies = sorted(by_company.items(), key=lambda x: len(x[1]), reverse=True)

    # Build filter data for JS
    company_filter_data = []
    for name, co_jobs in sorted_companies:
        count = len(co_jobs)
        sal_jobs = [(j.get('min_amount', 0) or 0, j.get('max_amount', 0) or 0) for j in co_jobs if (j.get('min_amount', 0) or 0) > 0 and (j.get('max_amount', 0) or 0) > 0]
        if sal_jobs:
            all_sals = [s[0] for s in sal_jobs] + [s[1] for s in sal_jobs]
            med = int(stat_median(all_sals))
        else:
            med = 0
        size_bucket = '1' if count == 1 else ('2-5' if count <= 5 else '6+')
        slug = make_company_slug(name)
        company_filter_data.append({
            'name': name,
            'count': count,
            'med': med,
            'size': size_bucket,
            'slug': slug,
        })

    # ── Stats bar ───────────────────────────────────────────────────────────────
    stats_bar = f'''
    <div class="job-stats-bar">
        <div class="job-stats-bar__inner">
            <span class="job-stat-item"><strong>{total_companies}</strong> companies hiring FDEs</span>
            <span class="job-stat-item"><strong>{total_jobs}</strong> open roles total</span>
            <span class="job-stat-item"><strong>{avg_roles}</strong> avg roles per company</span>
        </div>
    </div>'''

    # ── Filter bar ──────────────────────────────────────────────────────────────
    filter_bar = f'''
    <div class="job-filter-bar" id="compFilterBar">
        <div class="job-filter-bar__inner">
            <input type="search" id="filterSearch" class="job-filter-bar__search"
                placeholder="Search by company name..." autocomplete="off">
            <select id="filterSize" class="job-filter-bar__select" aria-label="Company size">
                <option value="">All sizes</option>
                <option value="1">1 role</option>
                <option value="2-5">2-5 roles</option>
                <option value="6+">6+ roles</option>
            </select>
            <select id="filterSort" class="job-filter-bar__select" aria-label="Sort by">
                <option value="roles">Most roles</option>
                <option value="pay">Best paying</option>
                <option value="az">A-Z</option>
            </select>
            <button class="job-filter-bar__reset" id="filterReset">Clear</button>
            <span class="job-filter-bar__count" id="filterCount">
                Showing <strong id="filterCountNum">{total_companies}</strong> of {total_companies} companies
            </span>
        </div>
    </div>'''

    # ── Company grid cards ──────────────────────────────────────────────────────
    company_cards_html = ''
    for item in company_filter_data:
        name = item['name']
        count = item['count']
        med = item['med']
        size = item['size']
        slug = item['slug']
        med_str = format_k(med) if med else 'Salary not disclosed'
        med_numeric = med  # for sorting

        # Build company page link -- only if profile page exists or we generate one
        profile_link = f'/companies/{slug}/'

        company_cards_html += f'''
        <a href="{profile_link}" class="co-card"
           data-name="{name.lower()}"
           data-size="{size}"
           data-roles="{count}"
           data-pay="{med_numeric}">
            <div class="co-card__header">
                <div class="co-card__name">{name}</div>
                <span class="co-card__badge">{count} role{"s" if count != 1 else ""}</span>
            </div>
            <div class="co-card__salary">{med_str}{"" if not med else " median"}</div>
            <div class="co-card__cta">View FDE roles &rarr;</div>
        </a>'''

    # ── Prose content ───────────────────────────────────────────────────────────
    top3 = sorted_companies[:3]
    top3_names = ', '.join(n for n, _ in top3)

    faq_html = ''
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

    prose = f'''
        <div class="co-prose">
            <h2>The FDE Company Landscape</h2>

            <p>Based on 134 active FDE postings as of April 30, 2026, {total_companies} companies are actively hiring Forward Deployed Engineers. {top3_names} lead the market by raw posting volume. But the spread across company types is the more telling signal: FDE hiring now covers tech giants, consulting firms, enterprise SaaS platforms, fintech companies, and early-stage AI startups.</p>

            <p>Google Cloud's 34 active FDE postings reflect a deliberate expansion of their customer deployment capability. Many of these roles are titled "Forward Deployed Developer" or "Forward Deployed Engineering Manager," indicating a structured FDE organization rather than ad-hoc customer engineering. Deloitte's 19 postings are spread across cloud migration, data platform deployment, and AI implementation roles. Both companies use the FDE title for roles that deploy specific technologies at client sites.</p>

            <h2>How FDE Team Structures Differ</h2>

            <p>Companies with many open FDE postings typically have formalized FDE programs: defined career ladders, onboarding processes, and internal tooling built specifically for customer deployments. Google Cloud and Deloitte fit this profile. These programs offer more career structure and training but can also mean more process and less autonomy per engineer.</p>

            <p>Companies with one to three FDE roles tend to be in an earlier phase of building their FDE function. An "FDE first hire" at a company like crewAI or Hex Technologies means defining the role from scratch, which requires more initiative but offers broader influence on how the company serves customers. FDE Pulse's market_intelligence data shows {int(100 * 16 / 134)}% of current postings are "first hire" FDE roles where the engineer would build the program.</p>

            <p>Consulting firms represent a distinct model. Deloitte, Accenture, KPMG, and Boston Consulting Group collectively account for more than 20% of active FDE postings. These roles deploy specific vendor platforms (AWS, Snowflake, Databricks, ServiceNow) for enterprise clients. Engineers rotate between clients rather than specializing in a single customer, which builds broad platform exposure but limits the depth of any single customer relationship.</p>

            <h2>What to Look For When Evaluating FDE Companies</h2>

            <p>When comparing FDE opportunities across companies, four factors matter most:</p>

            <p><strong>Team size and structure.</strong> A company with 10 or more FDE roles has an established program. A company with one or two roles is building the function. Both are legitimate choices, but they require different skills and offer different growth trajectories.</p>

            <p><strong>Salary disclosure rate.</strong> Companies that disclose salary ranges in job postings tend to be more transparent about compensation overall. Of the {total_companies} companies in this dataset, those with disclosed salaries show ranges from $50K to $365K. Companies without disclosed salaries are not necessarily lower-paying, but you'll need to negotiate without benchmark data.</p>

            <p><strong>Customer segment.</strong> Enterprise FDE roles (large Fortune 500 customers) involve longer sales cycles, higher stakes deployments, and more process. SMB-focused FDE roles move faster with more iterative customer relationships. The customer segment shapes the day-to-day work more than the company name does.</p>

            <p><strong>Technology focus.</strong> AI company FDEs work primarily with LLMs, RAG architectures, and model deployment. Data platform FDEs (Databricks, Snowflake ecosystem) focus on pipeline architecture. ERP integration FDEs (Salesforce, ServiceNow, Rippling) work with business process automation. Match the technology focus to your engineering interests before applying.</p>

            <h2>Frequently Asked Questions</h2>

            {faq_html}
        </div>'''

    body = f'''
{stats_bar}

        <div class="page-header">
            <div class="page-header__inner">
                <h1 class="page-header__title">Companies Hiring Forward Deployed Engineers</h1>
                <p class="page-header__subtitle">{total_companies} companies with active FDE postings. {total_jobs} open roles total as of April 30, 2026.</p>
            </div>
        </div>

{filter_bar}

        <div class="co-body">
            <div class="co-grid" id="coGrid">
                {company_cards_html}
            </div>
            {prose}
        </div>

        <div style="max-width: 900px; margin: 0 auto; padding: 0 1.5rem 3rem;">
            {get_cta_box()}
        </div>'''

    # Filter + sort JS
    filter_js = f'''
<script>
(function() {{
    var TOTAL = {total_companies};
    var search = document.getElementById('filterSearch');
    var selSize = document.getElementById('filterSize');
    var selSort = document.getElementById('filterSort');
    var resetBtn = document.getElementById('filterReset');
    var countNum = document.getElementById('filterCountNum');
    var grid = document.getElementById('coGrid');
    var cards = Array.from(grid.querySelectorAll('.co-card'));

    function isFiltered() {{
        return search.value.trim() !== '' || selSize.value !== '';
    }}

    function applyFilters() {{
        var q = search.value.trim().toLowerCase();
        var size = selSize.value;
        var sort = selSort.value;
        var visible = [];

        cards.forEach(function(card) {{
            var show = true;
            if (q && card.dataset.name.indexOf(q) === -1) show = false;
            if (show && size && card.dataset.size !== size) show = false;
            if (show) visible.push(card);
            card.style.display = show ? '' : 'none';
        }});

        // Sort visible cards
        visible.sort(function(a, b) {{
            if (sort === 'roles') return parseInt(b.dataset.roles) - parseInt(a.dataset.roles);
            if (sort === 'pay') return parseInt(b.dataset.pay || 0) - parseInt(a.dataset.pay || 0);
            if (sort === 'az') return a.dataset.name.localeCompare(b.dataset.name);
            return 0;
        }});

        // Re-insert in sorted order
        visible.forEach(function(card) {{ grid.appendChild(card); }});

        if (countNum) countNum.textContent = String(visible.length);
        if (isFiltered()) resetBtn.classList.add('visible');
        else resetBtn.classList.remove('visible');
    }}

    search.addEventListener('input', applyFilters);
    selSize.addEventListener('change', applyFilters);
    selSort.addEventListener('change', applyFilters);
    resetBtn.addEventListener('click', function() {{
        search.value = '';
        selSize.value = '';
        selSort.value = 'roles';
        applyFilters();
    }});
}})();
</script>'''

    # Page CSS
    page_css = '''
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
.page-header__title { font-size: 2.5rem; font-weight: 700; margin-bottom: var(--space-sm); }
.page-header__subtitle { color: var(--text-secondary); font-size: 1.1rem; }
.job-stats-bar {
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border);
    padding: 1rem var(--space-lg);
}
.job-stats-bar__inner {
    max-width: 1100px; margin: 0 auto;
    display: flex; gap: 2rem; flex-wrap: wrap; align-items: center;
}
.job-stat-item { display: flex; align-items: center; gap: 0.4rem; font-size: 0.9rem; color: var(--text-secondary); }
.job-stat-item strong { color: var(--amber-light); font-weight: 600; }
/* Filter bar */
.job-filter-bar {
    background: #162232;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    padding: 14px 20px;
    position: sticky;
    top: 72px;
    z-index: 10;
}
.job-filter-bar__inner {
    max-width: 1100px; margin: 0 auto;
    display: flex; gap: 10px; flex-wrap: wrap; align-items: center;
}
.job-filter-bar__search {
    flex: 1; min-width: 180px;
    background: #0F1923; border: 1px solid rgba(255,255,255,0.08);
    color: #fff; padding: 8px 12px; border-radius: 6px;
    font-size: 0.9rem; font-family: inherit; outline: none;
    transition: border-color 150ms ease;
}
.job-filter-bar__search::placeholder { color: rgba(255,255,255,0.35); }
.job-filter-bar__search:focus { border-color: #F59E0B; }
.job-filter-bar__select {
    background: #0F1923; border: 1px solid rgba(255,255,255,0.08);
    color: #fff; padding: 8px 12px; border-radius: 6px;
    font-size: 0.9rem; font-family: inherit; cursor: pointer; outline: none;
    transition: border-color 150ms ease; appearance: none; -webkit-appearance: none;
    padding-right: 28px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%23ffffff66' stroke-width='1.5' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");
    background-repeat: no-repeat; background-position: right 10px center;
}
.job-filter-bar__select:focus { border-color: #F59E0B; }
.job-filter-bar__select option { background: #162232; color: #fff; }
.job-filter-bar__reset {
    background: none; border: 1px solid rgba(255,255,255,0.12); color: rgba(255,255,255,0.5);
    padding: 8px 12px; border-radius: 6px; font-size: 0.875rem; font-family: inherit;
    cursor: pointer; transition: all 150ms ease; white-space: nowrap; display: none;
}
.job-filter-bar__reset.visible { display: inline-block; }
.job-filter-bar__reset:hover { border-color: #F59E0B; color: #FBBF24; }
.job-filter-bar__count { margin-left: auto; font-size: 0.875rem; color: rgba(255,255,255,0.5); white-space: nowrap; }
.job-filter-bar__count strong { color: #FBBF24; }
/* Company grid */
.co-body { max-width: 1100px; margin: 0 auto; padding: 2.5rem 1.5rem; }
.co-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1rem;
    margin-bottom: 3rem;
}
.co-card {
    display: block;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1.25rem;
    text-decoration: none;
    transition: all var(--transition-fast);
}
.co-card:hover {
    background: var(--bg-card-hover);
    border-color: var(--amber);
    transform: translateY(-1px);
    box-shadow: var(--shadow-glow);
}
.co-card__header {
    display: flex; justify-content: space-between; align-items: flex-start;
    margin-bottom: 0.5rem; gap: 0.5rem;
}
.co-card__name { font-size: 1.05rem; font-weight: 600; color: var(--text-primary); }
.co-card__badge {
    background: rgba(245, 158, 11, 0.12);
    border: 1px solid rgba(245, 158, 11, 0.25);
    color: var(--amber-light); font-size: 0.78rem; font-weight: 600;
    padding: 0.2rem 0.6rem; border-radius: var(--radius-full); white-space: nowrap;
}
.co-card__salary { font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.75rem; }
.co-card__cta { font-size: 0.85rem; color: var(--amber-light); font-weight: 500; }
/* Prose */
.co-prose {
    max-width: 900px; margin: 0 auto;
    color: var(--text-secondary); font-size: 1.05rem; line-height: 1.8;
}
.co-prose h2 { font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem; }
.co-prose p { margin-bottom: 1.25rem; }
.co-prose strong { color: var(--text-primary); }
@media (max-width: 768px) {
    .page-header { padding: 6rem 0 2rem; }
    .page-header__title { font-size: 2rem; }
    .job-filter-bar { top: 0; padding: 10px 12px; }
    .job-filter-bar__search { min-width: 100%; }
    .job-filter-bar__count { margin-left: 0; }
    .co-grid { grid-template-columns: 1fr; }
}
'''

    # Schemas
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
            {"@type": "ListItem", "position": 2, "name": "Companies", "item": BASE_URL + "/companies/"}
        ]
    }, indent=2)

    extra_head = (
        f'<style>{page_css}</style>\n'
        f'    <script type="application/ld+json">\n{faq_schema}\n    </script>\n'
        f'    <script type="application/ld+json">\n{breadcrumb}\n    </script>'
    )

    html = get_html_head(
        title=f"Companies Hiring Forward Deployed Engineers ({total_companies})",
        description=f"{total_companies} companies with active FDE job postings. {total_jobs} open roles at Google, Deloitte, AWS, Accenture, and more. Updated weekly.",
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
{filter_js}
</body>
</html>'''

    os.makedirs(os.path.join(SITE_DIR, 'companies'), exist_ok=True)
    out_path = os.path.join(SITE_DIR, 'companies', 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  Companies page generated: {out_path} ({len(html):,} bytes)")


if __name__ == "__main__":
    generate_companies_page()
