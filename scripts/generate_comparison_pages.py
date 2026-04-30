#!/usr/bin/env python3
"""
Generate comparison pages: FDE vs other roles.
pSEO Comparisons playbook. each page targets "[role A] vs [role B]" queries.
"""

import os
import sys
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from nav_config import SITE_NAME, BASE_URL
from templates import (
    get_html_head, get_header_html, get_footer_html,
    get_mobile_nav_js, get_signup_js, get_cta_box, get_related_links,
    get_article_schema
)

SITE_DIR = os.path.join(os.path.dirname(script_dir), 'site')

COMPARISONS = [
    {
        "slug": "forward-deployed-engineer-vs-solutions-engineer",
        "title": "Forward Deployed Engineer vs Solutions Engineer",
        "meta_desc": "FDE vs Solutions Engineer: salary, skills, career path, and day-to-day differences. Which role fits your background?",
        "other_role": "Solutions Engineer",
        "summary": "Both roles sit at the intersection of engineering and customer-facing work. The key difference: FDEs write production code deployed in customer environments, while Solutions Engineers typically focus on pre-sales technical demos, proof-of-concepts, and sales support.",
        "table": [
            {"dimension": "Primary Focus", "fde": "Building custom solutions in customer production environments", "other": "Pre-sales technical demos, POCs, and sales support"},
            {"dimension": "Code Ownership", "fde": "Writes and maintains production code deployed at customer sites", "other": "Builds demo environments and POCs, rarely production code"},
            {"dimension": "Customer Relationship", "fde": "Post-sale, embedded long-term (weeks to months)", "other": "Pre-sale, shorter engagements (days to weeks)"},
            {"dimension": "Salary Range", "fde": "$150,000 - $300,000", "other": "$120,000 - $250,000"},
            {"dimension": "Technical Depth", "fde": "Deep. full-stack, data engineering, ML/AI integration", "other": "Broad. product knowledge, API demos, integration architecture"},
            {"dimension": "Reporting Structure", "fde": "Engineering org or FDE-specific org", "other": "Sales org or solutions org"},
            {"dimension": "Travel", "fde": "20-40% (customer site embedding)", "other": "10-30% (sales meetings, onsite demos)"},
            {"dimension": "Career Path", "fde": "Engineering management, product, solutions architecture, founding", "other": "Sales leadership, solutions architecture, customer success leadership"},
        ],
        "when_fde": "You want to write production code, work deeply on a single customer's problems for extended periods, and care more about engineering craft than sales outcomes. FDEs are engineers first. If you'd rather build than demo, FDE is the path.",
        "when_other": "You enjoy variety (different prospects every week), want compensation tied to sales performance (commissions/bonuses), and prefer breadth over depth. Solutions Engineers influence deals. If you like the technical win that closes revenue, SE is the path.",
        "faq": [
            {"q": "Can you switch from Solutions Engineer to Forward Deployed Engineer?", "a": "Yes, and it's one of the most common transitions. Solutions Engineers already have customer-facing experience and product knowledge. The main gap is production-level coding: FDE roles require stronger software engineering fundamentals (system design, data structures, writing maintainable code). SEs transitioning to FDE should invest in backend engineering skills and build side projects that demonstrate production code quality."},
            {"q": "Do FDEs make more than Solutions Engineers?", "a": "On average, yes. FDE base salaries ($150,000-$300,000) are higher than SE base salaries ($120,000-$250,000). However, Solutions Engineers at top companies often earn significant variable compensation (commissions, deal bonuses) that can close or exceed the gap. Total comp depends heavily on company stage and deal flow."},
            {"q": "Which role has better work-life balance?", "a": "Neither role is a 9-to-5 job. FDEs face intense periods during customer deployments but have quieter intervals between engagements. Solutions Engineers face sales cycle pressure (quarter-end crunch, back-to-back demos) but rarely work weekends. The travel requirements are similar. Overall work-life balance depends more on the specific company than the role title."},
            {"q": "Is Forward Deployed Engineer a better title for your resume?", "a": "FDE is a stronger signal for engineering roles because it implies production-level coding. SE is a stronger signal for GTM and sales-adjacent roles. If you're planning to stay in engineering long-term, FDE looks better. If you're targeting leadership roles that bridge sales and engineering (CTO, VP Solutions), either title works."},
            {"q": "Which role is growing faster?", "a": "Forward Deployed Engineer postings grew 800% in 2025, while Solutions Engineer remains a mature, stable job market. FDE is earlier in its growth curve, meaning more greenfield opportunities but also more uncertainty about how the role evolves at each company. Solutions Engineer is well-established with clear career ladders at most tech companies."},
        ],
    },
    {
        "slug": "forward-deployed-engineer-vs-software-engineer",
        "title": "Forward Deployed Engineer vs Software Engineer",
        "meta_desc": "FDE vs Software Engineer: how the roles differ in scope, salary, customer exposure, and career trajectory. Detailed comparison.",
        "other_role": "Software Engineer",
        "summary": "Both roles write production code. The fundamental difference is scope: Software Engineers build products used by many customers, while Forward Deployed Engineers build solutions for specific customers. FDEs trade product generality for customer specificity.",
        "table": [
            {"dimension": "Primary Focus", "fde": "Custom solutions for specific customers", "other": "Products and features for all customers"},
            {"dimension": "Customer Exposure", "fde": "Direct. embedded with customers daily", "other": "Indirect. product requirements come through PMs"},
            {"dimension": "Code Scope", "fde": "Customer-specific integrations, data pipelines, custom features", "other": "Core product, platform, infrastructure"},
            {"dimension": "Salary Range", "fde": "$150,000 - $300,000", "other": "$130,000 - $350,000"},
            {"dimension": "Technical Depth", "fde": "Broad. full-stack, integration, customer infra", "other": "Deep. specialized in one domain (backend, frontend, ML, infra)"},
            {"dimension": "Autonomy", "fde": "High. often solo or small team at customer site", "other": "Varies. sprint teams, code review, shared ownership"},
            {"dimension": "Travel", "fde": "20-40% (customer site embedding)", "other": "0-5% (occasional offsites)"},
            {"dimension": "Career Path", "fde": "Engineering management, solutions architecture, product, founding", "other": "Staff/Principal engineer, engineering management, CTO track"},
        ],
        "when_fde": "You want direct customer impact, variety in technical problems (every customer is different), and the autonomy of working independently. FDEs see the business impact of their code immediately. If you're energized by solving real problems for real people rather than building features in a backlog, FDE is the path.",
        "when_other": "You want to go deep on a technical domain, build systems that scale to millions of users, and advance along a pure engineering track (Staff, Principal, Distinguished). Software Engineering offers clearer specialization paths and doesn't require customer-facing communication skills. If you prefer technical depth to breadth, stay on the SWE track.",
        "faq": [
            {"q": "Do Forward Deployed Engineers write less code than Software Engineers?", "a": "No. FDEs write as much or more code than typical SWEs. The difference is the type of code. FDEs write integration code, data pipeline code, custom feature implementations, and deployment scripts. SWEs write product code, platform code, and infrastructure code. FDE code tends to be more varied but less reviewed (smaller teams), while SWE code goes through structured review processes."},
            {"q": "Is FDE considered real engineering?", "a": "Yes. FDEs write production code, design systems, debug complex issues, and ship software. The perception that FDE is 'less technical' comes from Palantir's early model where some FDEs did more consulting than coding. At modern AI companies (OpenAI, Databricks, Scale AI), FDEs are expected to be strong engineers who happen to work in customer environments rather than on core product."},
            {"q": "Can you go from FDE back to regular Software Engineering?", "a": "Absolutely. FDE experience is valued in SWE hiring because it demonstrates breadth, autonomy, and ability to ship under pressure. The main adjustment is adapting to sprint-based development and code review processes after working independently. Many engineers alternate between FDE and SWE roles throughout their careers."},
            {"q": "Which pays more: FDE or Software Engineer?", "a": "At the same company and seniority, FDEs typically earn 10-15% more in base salary than SWEs. However, the highest-paying engineering roles are Staff+ SWE positions at FAANG companies ($400,000-$700,000+ total comp), which don't have FDE equivalents. FDEs max out around $300,000-$350,000 total comp. If maximizing lifetime earnings is the priority, the SWE path has a higher ceiling."},
            {"q": "Which role is harder to get hired for?", "a": "FDE roles are currently harder to fill because the candidate pool is smaller. Most engineers don't have combined strong coding + customer communication skills. SWE roles are more competitive in terms of applicant volume (hundreds of applications per posting) but have a larger qualified candidate pool. FDE interviews typically add a customer scenario or case study round that SWE interviews don't have."},
        ],
    },
    {
        "slug": "forward-deployed-engineer-vs-consultant",
        "title": "Forward Deployed Engineer vs Consultant",
        "meta_desc": "FDE vs Management/Technology Consultant: compensation, skills, career path, and lifestyle differences. Which path delivers more long-term value?",
        "other_role": "Technology Consultant",
        "summary": "Both roles work directly with clients to solve technical problems. The key difference: FDEs build and deploy a specific company's product, while consultants advise across multiple vendors and technology stacks. FDEs are product engineers; consultants are advisors.",
        "table": [
            {"dimension": "Primary Focus", "fde": "Deploying and customizing one product at customer sites", "other": "Advising on strategy and implementing across multiple vendors"},
            {"dimension": "Product Tie", "fde": "Tied to one company's product", "other": "Vendor-agnostic (in theory)"},
            {"dimension": "Code Depth", "fde": "Production code. builds, ships, maintains", "other": "Varies. some code, mostly architecture, strategy, project management"},
            {"dimension": "Salary Range", "fde": "$150,000 - $300,000 (salary + equity)", "other": "$100,000 - $250,000 (salary + bonus)"},
            {"dimension": "Equity", "fde": "Common. RSUs or options at tech companies", "other": "Rare. partnership track at Big 4 is the equity equivalent"},
            {"dimension": "Client Variety", "fde": "Fewer clients, deeper engagements", "other": "More clients, shorter engagements"},
            {"dimension": "Travel", "fde": "20-40%", "other": "40-80% (especially at MBB and Big 4)"},
            {"dimension": "Career Path", "fde": "Engineering leadership, product, founding a startup", "other": "Partner track, executive leadership, corporate strategy"},
        ],
        "when_fde": "You want to write code, build real systems, and earn equity in a technology company. FDEs solve technical problems hands-on. If you'd rather build than advise, and want the upside of startup/pre-IPO equity rather than a consulting partnership track, FDE is the path.",
        "when_other": "You want exposure to diverse industries and business problems, a structured career progression (Analyst → Associate → VP → Partner), and the prestige and network of a consulting firm. Consulting develops general business acumen faster than FDE work. If you're not sure what industry to specialize in, consulting gives you time to figure it out.",
        "faq": [
            {"q": "Is FDE just consulting with a different name?", "a": "No. The structural difference is product alignment. FDEs deploy one company's product and contribute improvements back to that product's codebase. Consultants advise on strategy across multiple vendor products and rarely contribute to product development. FDEs are engineers who happen to work at customer sites; consultants are advisors who sometimes write code."},
            {"q": "Do ex-consultants make good FDEs?", "a": "Often, yes. Consultants bring strong client management, communication, and problem-structuring skills. The gap is usually technical depth: FDE roles require production-level coding that consulting roles don't always develop. Ex-consultants from technical implementation practices (Deloitte Technology, PwC Digital) transition more easily than those from strategy practices (McKinsey, BCG)."},
            {"q": "Which has better exit opportunities?", "a": "Consulting exits are more established: corporate strategy, executive roles, PE/VC, startup operations. FDE exits are more technical: engineering management, product management, solutions architecture, CTO/VP Engineering at smaller companies, or founding a startup. Consulting gives broader optionality; FDE gives deeper technical credibility."},
            {"q": "Do FDEs travel less than consultants?", "a": "Significantly less. FDEs travel 20-40% (and many roles are remote with periodic customer visits). Big 4 and MBB consultants travel 40-80%. Monday-Thursday at client sites is the norm. This is one of the top reasons engineers choose FDE over consulting. The lifestyle difference is substantial, especially for engineers with families."},
            {"q": "Which pays more over a 10-year career?", "a": "It depends on the path. A Partner at McKinsey or PwC earns $500,000-$2,000,000+. A Staff FDE at a pre-IPO company that goes public could earn more through equity. In expected value, consulting has a more predictable high-income trajectory (if you make Partner). FDE has higher variance: equity can be worth millions or zero. For risk-adjusted returns, consulting pays more reliably. For upside potential, FDE at the right company wins."},
        ],
    },
]


def generate_comparison_pages():
    print("  Generating comparison pages...")
    count = 0

    for comp in COMPARISONS:
        related = get_related_links([
            {"href": "/career/what-is-a-forward-deployed-engineer/", "label": "What Is an FDE?"},
            {"href": "/salaries/", "label": "FDE Salary Data"},
            {"href": "/career/how-to-become-a-forward-deployed-engineer/", "label": "How to Become an FDE"},
            {"href": "/companies/", "label": "Companies Hiring FDEs"},
        ])
        table_rows = ""
        for row in comp["table"]:
            table_rows += f'''
                    <tr>
                        <td style="padding: 0.75rem 1rem; font-weight: 600; color: var(--text-primary); width: 20%; border-right: 1px solid var(--border);">{row["dimension"]}</td>
                        <td style="padding: 0.75rem 1rem; color: var(--text-secondary); width: 40%;">{row["fde"]}</td>
                        <td style="padding: 0.75rem 1rem; color: var(--text-secondary); width: 40%;">{row["other"]}</td>
                    </tr>'''

        faq_html = ""
        faq_items = []
        for faq in comp["faq"]:
            faq_html += f'''
                <div style="margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border);">
                    <h3 style="font-size: 1.15rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">{faq["q"]}</h3>
                    <p style="color: var(--text-secondary); line-height: 1.7;">{faq["a"]}</p>
                </div>'''
            faq_items.append({"@type": "Question", "name": faq["q"], "acceptedAnswer": {"@type": "Answer", "text": faq["a"]}})

        body = f'''
        <section class="section" style="max-width: 900px; margin: 0 auto; padding-top: 8rem;">
            <h1 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">{comp["title"]}</h1>
            <div style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 1.5rem;">By <a href="https://www.linkedin.com/in/romethorndike/" target="_blank" rel="noopener" style="color: var(--amber); text-decoration: none;">Rome Thorndike</a></div>
            <p style="font-size: 1.15rem; color: var(--text-secondary); margin-bottom: 2.5rem; line-height: 1.7;">{comp["summary"]}</p>

            <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 0 0 1.25rem;">Side-by-Side Comparison</h2>

            <div style="overflow-x: auto; margin-bottom: 2.5rem;">
                <table style="width: 100%; border-collapse: collapse; background: var(--bg-card); border-radius: var(--radius-lg); overflow: hidden;">
                    <thead>
                        <tr style="border-bottom: 1px solid var(--border);">
                            <th style="padding: 0.75rem 1rem; text-align: left; font-size: 0.85rem; color: var(--text-muted); font-weight: 600;"></th>
                            <th style="padding: 0.75rem 1rem; text-align: left; font-size: 0.85rem; color: var(--amber-light); font-weight: 600;">Forward Deployed Engineer</th>
                            <th style="padding: 0.75rem 1rem; text-align: left; font-size: 0.85rem; color: var(--text-muted); font-weight: 600;">{comp["other_role"]}</th>
                        </tr>
                    </thead>
                    <tbody>
{table_rows}
                    </tbody>
                </table>
            </div>

            <div style="color: var(--text-secondary); font-size: 1.05rem; line-height: 1.8;">
                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Choose FDE If...</h2>
                <p style="margin-bottom: 1.25rem;">{comp["when_fde"]}</p>

                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Choose {comp["other_role"]} If...</h2>
                <p style="margin-bottom: 1.25rem;">{comp["when_other"]}</p>

                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Frequently Asked Questions</h2>
                {faq_html}
            </div>

            {related}

            {get_cta_box()}
        </section>
'''

        faq_schema = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_items}, indent=2)
        breadcrumb = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": "Insights", "item": f"{BASE_URL}/insights/"},
            {"@type": "ListItem", "position": 3, "name": comp["title"], "item": f"{BASE_URL}/insights/{comp['slug']}/"}
        ]}, indent=2)

        article = get_article_schema(comp["title"], comp["meta_desc"], f"/insights/{comp['slug']}/", "2026-04-10")
        extra_head = f'<script type="application/ld+json">\n{faq_schema}\n    </script>\n    <script type="application/ld+json">\n{breadcrumb}\n    </script>\n    {article}'

        html = get_html_head(
            title=comp["title"],
            description=comp["meta_desc"],
            canonical_path=f"/insights/{comp['slug']}/",
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

        out_dir = os.path.join(SITE_DIR, 'insights', comp['slug'])
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        count += 1

    print(f"  {count} comparison pages generated")


if __name__ == "__main__":
    generate_comparison_pages()
