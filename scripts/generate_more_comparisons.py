#!/usr/bin/env python3
"""Generate additional comparison pages for FDE Pulse."""

import os, sys, json

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from nav_config import BASE_URL
from templates import get_html_head, get_header_html, get_footer_html, get_mobile_nav_js, get_signup_js, get_cta_box, get_related_links

SITE_DIR = os.path.join(os.path.dirname(script_dir), 'site')

COMPARISONS = [
    {
        "slug": "forward-deployed-engineer-vs-sales-engineer",
        "title": "Forward Deployed Engineer vs Sales Engineer",
        "meta_desc": "FDE vs Sales Engineer: salary, daily work, career path, and when to choose each. Side-by-side comparison with data.",
        "other_role": "Sales Engineer",
        "summary": "Sales Engineers close deals. Forward Deployed Engineers deliver on them. SEs work pre-sale to demonstrate product value, run technical evaluations, and overcome objections. FDEs work post-sale to build, deploy, and maintain custom solutions in customer environments. The skill sets overlap (both need technical chops and customer communication) but the incentive structures, daily work, and career trajectories diverge sharply.",
        "table": [
            {"dim": "Primary Focus", "fde": "Post-sale deployment: building custom solutions in customer environments", "other": "Pre-sale: demos, POCs, technical evaluations, objection handling"},
            {"dim": "Revenue Tie", "fde": "Retention and expansion (CSAT, NRR)", "other": "New business (pipeline, closed-won revenue)"},
            {"dim": "Compensation Model", "fde": "Base salary + equity (engineering comp)", "other": "Base salary + variable/commission (sales comp)"},
            {"dim": "Salary Range", "fde": "$150,000 - $300,000 (base + equity)", "other": "$120,000 - $280,000 (base + variable, OTE)"},
            {"dim": "Code Depth", "fde": "Production code. deployed, maintained, iterated", "other": "Demo code. POCs, sandbox environments, scripts"},
            {"dim": "Customer Duration", "fde": "Weeks to months per customer", "other": "Hours to days per prospect"},
            {"dim": "Travel", "fde": "20-40%", "other": "15-40% (varies widely by company)"},
            {"dim": "Reporting Line", "fde": "Engineering or FDE-specific org", "other": "Sales org (reports to CRO/VP Sales)"},
        ],
        "when_fde": "You want to build real systems, own production code, and work deeply with a smaller number of customers over extended periods. FDE compensation is base-heavy with equity upside. If you'd rather ship than sell, FDE is the path.",
        "when_other": "You thrive on variety (new prospects every week), enjoy the competitive energy of a sales environment, and want compensation tied directly to revenue performance. Top Sales Engineers at enterprise companies earn $250,000-$350,000+ OTE. If you like winning technical evaluations and influencing seven-figure deals, SE is the path.",
        "faq": [
            {"q": "Can Sales Engineers transition to FDE?", "a": "Yes, and it's a common transition. SEs already have customer-facing experience and product knowledge. The gap is usually production-level coding: FDE roles require building and maintaining real systems, not just demo environments. SEs transitioning to FDE should invest in backend engineering skills and demonstrate they can ship production code independently. Some companies (Palantir, Salesforce) have internal transfer paths between SE and FDE teams."},
            {"q": "Which role earns more: FDE or Sales Engineer?", "a": "It depends on performance. Top-performing SEs with commission can out-earn FDEs at the same seniority: $250,000-$350,000+ OTE at enterprise companies. FDEs earn more predictably ($150,000-$300,000 base + equity) without variable compensation risk. If you consistently hit quota, SE can pay more. If you want stable, high base compensation with equity upside, FDE is more predictable."},
            {"q": "Do FDEs work with Sales Engineers?", "a": "Frequently. In many enterprise sales cycles, SEs run the technical evaluation pre-sale, then hand off to FDEs for post-sale deployment. At companies like Palantir and Salesforce, the SE-to-FDE handoff is a defined process. FDEs inherit the technical context from the SE's POC work. Strong SE-FDE collaboration directly impacts customer time-to-value and renewal rates."},
            {"q": "Which is better for long-term career growth?", "a": "FDE leads to engineering leadership, product management, solutions architecture, or founding a startup. SE leads to sales leadership (VP Solutions, CRO), sales operations, or customer success leadership. FDE builds deeper technical credibility. SE builds broader business and revenue experience. Neither is universally 'better'. it depends on whether you want your career to trend technical or commercial."},
            {"q": "Is FDE replacing the Sales Engineer role?", "a": "No. The roles serve different stages of the customer lifecycle. Companies that hire FDEs also hire SEs. In fact, companies with FDE teams often need more SEs because the FDE model enables selling more complex, higher-value deployments that require stronger pre-sale technical evaluation. The two roles are complementary, not substitutes."},
        ],
    },
    {
        "slug": "forward-deployed-engineer-vs-solutions-architect",
        "title": "Forward Deployed Engineer vs Solutions Architect",
        "meta_desc": "FDE vs Solutions Architect: hands-on building vs strategic design. Salary, skills, and career path comparison.",
        "other_role": "Solutions Architect",
        "summary": "Solutions Architects design; Forward Deployed Engineers build. SAs create high-level technical blueprints, reference architectures, and integration strategies for customers. FDEs take those designs and turn them into working production systems. SAs think in diagrams and documents; FDEs think in code and deployments. Both roles require deep technical knowledge and customer communication, but they operate at different levels of abstraction.",
        "table": [
            {"dim": "Primary Focus", "fde": "Hands-on building: writing code, deploying systems, maintaining production", "other": "Strategic design: architecture diagrams, reference designs, technical strategy"},
            {"dim": "Abstraction Level", "fde": "Implementation. in the code", "other": "Design. above the code"},
            {"dim": "Deliverables", "fde": "Working software, deployed systems, running integrations", "other": "Architecture documents, reference designs, migration plans"},
            {"dim": "Salary Range", "fde": "$150,000 - $300,000", "other": "$140,000 - $280,000"},
            {"dim": "Customer Interaction", "fde": "Daily, embedded with customer engineering teams", "other": "Regular, meeting with customer architects and leadership"},
            {"dim": "Seniority", "fde": "Mid to Senior (3-10 years experience typical)", "other": "Senior to Principal (7-15+ years experience typical)"},
            {"dim": "Travel", "fde": "20-40%", "other": "20-50% (more workshops and strategy sessions)"},
            {"dim": "Career Path", "fde": "Senior FDE, engineering management, product, founding", "other": "Principal Architect, CTO, VP Engineering, consulting partner"},
        ],
        "when_fde": "You want to build things. FDEs write code every day, solve concrete technical problems, and see their work running in production at customer sites. If your energy comes from shipping software rather than designing systems on whiteboards, FDE is the path. FDE roles are also accessible earlier in your career (3-5 years vs. 7+ for most SA roles).",
        "when_other": "You've reached a point in your career where you want to influence technical decisions at a strategic level rather than writing code day-to-day. Solutions Architects shape how entire organizations use technology. If you prefer designing systems at scale and mentoring engineers over implementing features yourself, SA is the natural progression. Many SAs are former FDEs or senior engineers who moved up the abstraction ladder.",
        "faq": [
            {"q": "Is Solutions Architect a natural next step after FDE?", "a": "Yes. Many Solutions Architects started in hands-on roles like FDE, SWE, or consulting. The FDE-to-SA path is logical: FDEs build deep customer deployment experience, which translates directly into the ability to design deployment architectures at a strategic level. The transition typically happens at 7-10 years of experience when engineers want to influence more broadly and code less directly."},
            {"q": "Do FDEs and Solutions Architects work together?", "a": "Frequently. In large enterprise deals, a Solutions Architect designs the overall integration strategy and an FDE implements it. The SA handles the 10,000-foot view: which systems connect, what the data flow looks like, what the migration sequence should be. The FDE handles the ground-level reality: writing the integration code, debugging the edge cases, and making the architecture work in practice. The best customer outcomes happen when SA and FDE collaborate closely."},
            {"q": "Which role is more technical?", "a": "FDE is more hands-on technical (writing production code daily). Solutions Architect requires broader technical knowledge (understanding entire technology stacks) but less daily coding. SAs need to evaluate technologies, design integrations across multiple vendor products, and understand enterprise IT landscapes at a level most FDEs don't need to. The technical depth differs in kind, not degree."},
            {"q": "Do Solutions Architects code?", "a": "Some do, some don't. At smaller companies and cloud providers (AWS, GCP, Azure), SAs frequently write reference implementations, build POCs, and contribute to customer solutions. At larger companies, SAs focus more on design documents and architectural reviews. The trend is toward SAs who can code: 'architecture' as a purely non-coding role is declining."},
            {"q": "Which pays more at senior levels?", "a": "Similar at equivalent experience levels. Senior SAs at cloud providers (AWS, GCP) earn $200,000-$300,000+ total comp. Senior FDEs at AI companies earn $200,000-$300,000+. Principal SAs and Distinguished Architects at enterprise companies can earn $300,000-$450,000+, which exceeds most FDE compensation. The SA track has a slightly higher ceiling because there are more principal/distinguished-level SA positions than equivalent FDE positions."},
        ],
    },
    {
        "slug": "forward-deployed-engineer-vs-customer-engineer",
        "title": "Forward Deployed Engineer vs Customer Engineer",
        "meta_desc": "FDE vs Customer Engineer: overlapping titles or different roles? Salary, scope, and career path breakdown.",
        "other_role": "Customer Engineer",
        "summary": "Forward Deployed Engineer and Customer Engineer are the two titles most often confused with each other. At some companies, they're literally the same role with different names. At others, they're meaningfully different. The distinction usually comes down to code ownership: FDEs write and maintain production code in customer environments, while Customer Engineers at some companies focus more on support, enablement, and technical account management with less original code.",
        "table": [
            {"dim": "Primary Focus", "fde": "Building custom solutions deployed in customer production environments", "other": "Technical customer success: enablement, support, and light integration work"},
            {"dim": "Code Depth", "fde": "Heavy. production code, custom features, full-stack development", "other": "Varies. some CEs code heavily (Google), others focus on configuration and support"},
            {"dim": "Origin", "fde": "Palantir (2010s)", "other": "Google Cloud (2010s)"},
            {"dim": "Salary Range", "fde": "$150,000 - $300,000", "other": "$130,000 - $250,000"},
            {"dim": "Customer Relationship", "fde": "Deep embedding, weeks-to-months per customer", "other": "Ongoing relationship, portfolio of customers"},
            {"dim": "Who Hires", "fde": "AI companies, enterprise SaaS, startups", "other": "Cloud providers (Google, AWS), enterprise SaaS"},
            {"dim": "Reporting Line", "fde": "Engineering org or FDE-specific team", "other": "Customer success org or sales engineering org"},
            {"dim": "Career Path", "fde": "Engineering management, product, solutions architecture", "other": "Customer success leadership, solutions architecture, TAM leadership"},
        ],
        "when_fde": "You want to write production code and work on deep, technically complex customer deployments. FDE is the right fit if you see yourself as an engineer first who happens to work with customers. The coding expectation is higher, the deployments are more custom, and the technical problems are harder.",
        "when_other": "You prefer a portfolio model (managing relationships with multiple customers) over deep embedding with one customer at a time. Customer Engineer roles at Google Cloud, for example, combine technical problem-solving with account management and often come with better work-life balance than FDE roles at startups. CE is also a good fit if you want a more structured role with clearer boundaries between engineering and customer management.",
        "faq": [
            {"q": "Is Customer Engineer just another name for FDE?", "a": "Sometimes, but not always. At companies like Google Cloud, Customer Engineer is a well-defined role with its own career ladder, distinct from SWE. At startups, 'Customer Engineer' and 'Forward Deployed Engineer' may describe identical roles. The safest way to tell: read the job description. If it emphasizes building custom production software, it's functionally an FDE. If it emphasizes technical account management and enablement, it's closer to a traditional CE."},
            {"q": "Do Customer Engineers write code?", "a": "It varies dramatically by company. Google Cloud Customer Engineers write significant code: building custom solutions, automating customer infrastructure, and creating reference architectures. Customer Engineers at smaller SaaS companies may focus more on configuration, support, and enablement with minimal coding. FDE roles consistently require production-level coding regardless of company."},
            {"q": "Which role is better for career growth?", "a": "FDE has stronger engineering credibility if you want to stay on a technical track. Customer Engineer has stronger customer success credibility if you want to move into leadership roles that manage customer relationships at scale. Both can lead to solutions architecture. The FDE title is newer and growing faster, which means more greenfield opportunities but less established career infrastructure."},
            {"q": "Can I switch between Customer Engineer and FDE?", "a": "Yes. The skills overlap significantly. A Customer Engineer at Google moving to an FDE role at OpenAI would need to demonstrate stronger coding skills but already has the customer-facing experience. An FDE moving to a CE role would need to demonstrate portfolio management skills (handling multiple customers simultaneously) rather than deep single-customer embedding."},
            {"q": "Which role pays more?", "a": "FDE roles pay more on average ($150,000-$300,000 vs. $130,000-$250,000 for CE). The gap is widest at AI companies, where FDE salary premiums reflect the difficulty of finding engineers with both strong coding skills and LLM deployment experience. At Google Cloud, senior Customer Engineers can earn $200,000-$280,000 total comp, which closes the gap with equivalent-seniority FDE roles elsewhere."},
        ],
    },
    {
        "slug": "forward-deployed-engineer-vs-implementation-engineer",
        "title": "FDE vs Implementation Engineer",
        "meta_desc": "FDE vs Implementation Engineer: both deploy software for customers, but scope, salary, and career path differ. Full comparison.",
        "other_role": "Implementation Engineer",
        "summary": "Both roles deploy software at customer sites. The difference is scope and creativity. Implementation Engineers follow established playbooks to deploy a product according to predefined configurations. Forward Deployed Engineers build custom solutions that don't exist yet. Implementation is repeatable; forward deployment is inventive. Implementation Engineers are operators; FDEs are builders.",
        "table": [
            {"dim": "Primary Focus", "fde": "Building new custom solutions for each customer", "other": "Deploying standardized product according to established playbooks"},
            {"dim": "Creativity Required", "fde": "High. each deployment is unique", "other": "Moderate. follows documented processes with some customization"},
            {"dim": "Code Depth", "fde": "Heavy. production code, custom integrations, new features", "other": "Light to moderate. configuration, scripting, data migration"},
            {"dim": "Salary Range", "fde": "$150,000 - $300,000", "other": "$90,000 - $170,000"},
            {"dim": "Experience Required", "fde": "3-7+ years software engineering", "other": "1-5 years technical experience"},
            {"dim": "Problem Complexity", "fde": "Novel. no existing solution for this customer's needs", "other": "Known. well-documented deployment scenarios"},
            {"dim": "Team Size", "fde": "Small (1-3 FDEs per customer)", "other": "Larger implementation teams with project managers"},
            {"dim": "Career Path", "fde": "Engineering management, product, solutions architecture", "other": "Implementation management, professional services leadership, solutions consulting"},
        ],
        "when_fde": "You want to solve novel technical problems, write significant production code, and work at the edge of what a product can do. FDEs encounter situations where the product doesn't do what the customer needs, and they build the solution. If repetitive deployment work bores you, FDE is the path.",
        "when_other": "You want structured, process-driven work with clear success criteria and established playbooks. Implementation Engineering is a strong entry point for engineers who want customer-facing technical work without the ambiguity and pressure of FDE deployments. It's also more accessible early in your career (1-3 years experience vs. 3-7+ for FDE).",
        "faq": [
            {"q": "Is Implementation Engineer a stepping stone to FDE?", "a": "It can be. Implementation Engineers who demonstrate strong coding skills and the ability to handle ambiguous customer situations are strong FDE candidates. The experience with customer deployments, data migration, and system configuration directly transfers. The gap to close is production-level software engineering: FDE roles require building new solutions, not just deploying existing ones."},
            {"q": "Why is the FDE salary so much higher than Implementation Engineer?", "a": "The salary gap ($150K-$300K vs. $90K-$170K) reflects the difference in required skills. FDEs need strong software engineering fundamentals (system design, production code, debugging complex systems) plus customer communication. Implementation Engineers need technical configuration skills and process management. The supply of engineers who can do both engineering and customer work is much smaller, driving FDE salaries higher."},
            {"q": "Do companies have both FDEs and Implementation Engineers?", "a": "Some do. Large enterprise software companies (Salesforce, ServiceNow, Workday) have Implementation/Professional Services teams for standard deployments and FDE teams for complex, custom deployments. The FDE team handles the customers whose needs exceed what standard implementation playbooks can deliver."},
            {"q": "Which role is more stressful?", "a": "FDE is generally more stressful because the problems are novel and the expectations are higher. FDEs work in ambiguous environments where the solution doesn't exist yet. Implementation Engineers follow established processes with clearer success criteria. However, Implementation Engineers often handle higher volumes (more customers simultaneously) and face project management pressure around timelines and resource constraints."},
            {"q": "Can I become an FDE without previous implementation experience?", "a": "Yes. Most FDEs come from software engineering backgrounds, not implementation backgrounds. Implementation experience is helpful but not required. Strong coding skills and customer communication ability matter more than deployment process experience. Many FDEs have never worked in implementation or professional services before their first FDE role."},
        ],
    },
    {
        "slug": "forward-deployed-engineer-vs-product-manager",
        "title": "Forward Deployed Engineer vs Product Manager",
        "meta_desc": "FDE vs Product Manager: both shape products, but from different angles. Technical depth, salary, daily work comparison.",
        "other_role": "Product Manager",
        "summary": "Both roles shape how products serve customers, but from opposite directions. Product Managers define what to build based on market research, user feedback, and business strategy. Forward Deployed Engineers discover what to build by deploying the product at customer sites and hitting the gaps firsthand. PMs work upstream (before code is written); FDEs work downstream (after the product ships) and feed insights back upstream. The FDE-to-PM transition is one of the most common career paths in the FDE world.",
        "table": [
            {"dim": "Primary Focus", "fde": "Deploying product + building custom solutions at customer sites", "other": "Defining product strategy, requirements, and roadmap"},
            {"dim": "Technical Depth", "fde": "Deep. writes production code daily", "other": "Broad. understands technology, rarely writes code"},
            {"dim": "Customer Exposure", "fde": "Direct, embedded with customer engineering teams", "other": "Structured: user research, interviews, analytics, sales feedback"},
            {"dim": "Salary Range", "fde": "$150,000 - $300,000", "other": "$130,000 - $300,000"},
            {"dim": "Decision Authority", "fde": "Tactical. solves this customer's problem today", "other": "Strategic. decides what all customers get next quarter"},
            {"dim": "Org Influence", "fde": "Influences product through deployment feedback", "other": "Owns the product roadmap directly"},
            {"dim": "Output", "fde": "Working software, deployed systems, customer outcomes", "other": "PRDs, roadmaps, success metrics, launch plans"},
            {"dim": "Career Path", "fde": "Engineering management, product management, founding", "other": "Group PM, VP Product, CPO, founding"},
        ],
        "when_fde": "You love building things with your hands (writing code, deploying systems) and want to discover customer needs through direct technical work. FDEs have the most authentic understanding of customer pain because they experience it while building solutions. If you want to influence product decisions through action rather than documents, FDE is the path. Many FDEs eventually transition to PM with the advantage of deep technical and customer credibility.",
        "when_other": "You want to shape product direction at a strategic level, enjoy synthesizing information from multiple sources (users, data, sales, engineering), and prefer influence over implementation. Product Managers own the 'what' and 'why' while engineers own the 'how.' If you're energized by defining problems rather than solving them directly, PM is the path.",
        "faq": [
            {"q": "Is FDE a good path to Product Management?", "a": "One of the best. FDEs develop two things PMs covet: deep technical credibility and firsthand customer understanding. FDE-to-PM transitions are common at companies like Palantir, OpenAI, and Salesforce. The FDE background means you can evaluate technical feasibility, have empathy for engineering constraints, and bring real customer stories to product decisions. Many FDEs find the PM transition natural after 3-5 years."},
            {"q": "Do FDEs and PMs work together?", "a": "Closely. FDEs are one of the most valuable feedback channels for PMs. FDEs see how the product works (or doesn't work) in real customer environments. They surface feature requests, usability issues, and integration gaps that analytics and user research can't capture. At well-run companies, FDEs have direct access to PMs and influence roadmap prioritization through deployment feedback."},
            {"q": "Which role has more impact on the product?", "a": "PMs have more direct influence on product direction (they own the roadmap). FDEs have more direct influence on customer outcomes (they build what customers actually use). Both matter. Products built without FDE feedback tend to miss real-world deployment challenges. Products without PM leadership tend to lack strategic direction. The highest-performing product organizations integrate FDE insights into PM decision-making."},
            {"q": "Which pays more?", "a": "Similar at equivalent seniority levels. PM compensation ranges from $130,000-$300,000 depending on company and level. FDE compensation ranges from $150,000-$300,000. The PM path has a slightly higher ceiling at the executive level (VP Product, CPO roles earning $350,000-$600,000+). The FDE path has higher earning potential if your company's equity appreciates significantly."},
            {"q": "Should I become a PM directly or go FDE first?", "a": "Going FDE first gives you technical credibility that direct-to-PM candidates lack. In interviews, you can describe product decisions you influenced through real customer deployment experience rather than theoretical frameworks. The downside is that it takes 3-5 years as an FDE before transitioning, while direct PM paths start immediately. If you have strong engineering skills and want the deepest possible customer understanding, FDE-then-PM is the stronger long-term play."},
        ],
    },
]


def _build_page(comp):
    """Build a single comparison page HTML."""
    related = get_related_links([
        {"href": "/career/what-is-a-forward-deployed-engineer/", "label": "What Is an FDE?"},
        {"href": "/salaries/", "label": "FDE Salary Data"},
        {"href": "/career/how-to-become-a-forward-deployed-engineer/", "label": "How to Become an FDE"},
        {"href": "/companies/", "label": "Companies Hiring FDEs"},
    ])
    table_rows = ""
    for row in comp["table"]:
        table_rows += '''
                    <tr>
                        <td style="padding: 0.75rem 1rem; font-weight: 600; color: var(--text-primary); width: 20%%; border-right: 1px solid var(--border);">%s</td>
                        <td style="padding: 0.75rem 1rem; color: var(--text-secondary); width: 40%%;">%s</td>
                        <td style="padding: 0.75rem 1rem; color: var(--text-secondary); width: 40%%;">%s</td>
                    </tr>''' % (row["dim"], row["fde"], row["other"])

    faq_html = ""
    faq_items = []
    for faq in comp["faq"]:
        faq_html += '''
            <div style="margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border);">
                <h3 style="font-size: 1.15rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">%s</h3>
                <p style="color: var(--text-secondary); line-height: 1.7;">%s</p>
            </div>''' % (faq["q"], faq["a"])
        faq_items.append({"@type": "Question", "name": faq["q"], "acceptedAnswer": {"@type": "Answer", "text": faq["a"]}})

    body = '''
        <section class="section" style="max-width: 900px; margin: 0 auto; padding-top: 8rem;">
            <h1 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem;">%s</h1>
            <p style="font-size: 1.15rem; color: var(--text-secondary); margin-bottom: 2.5rem; line-height: 1.7;">%s</p>

            <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 0 0 1.25rem;">Side-by-Side Comparison</h2>

            <div style="overflow-x: auto; margin-bottom: 2.5rem;">
                <table style="width: 100%%; border-collapse: collapse; background: var(--bg-card); border-radius: var(--radius-lg); overflow: hidden;">
                    <thead>
                        <tr style="border-bottom: 1px solid var(--border);">
                            <th style="padding: 0.75rem 1rem; text-align: left; font-size: 0.85rem; color: var(--text-muted); font-weight: 600;"></th>
                            <th style="padding: 0.75rem 1rem; text-align: left; font-size: 0.85rem; color: var(--amber-light); font-weight: 600;">Forward Deployed Engineer</th>
                            <th style="padding: 0.75rem 1rem; text-align: left; font-size: 0.85rem; color: var(--text-muted); font-weight: 600;">%s</th>
                        </tr>
                    </thead>
                    <tbody>
%s
                    </tbody>
                </table>
            </div>

            <div style="color: var(--text-secondary); font-size: 1.05rem; line-height: 1.8;">
                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Choose FDE If...</h2>
                <p style="margin-bottom: 1.25rem;">%s</p>

                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Choose %s If...</h2>
                <p style="margin-bottom: 1.25rem;">%s</p>

                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Frequently Asked Questions</h2>
                %s
            </div>

            %s

            %s
        </section>
''' % (comp["title"], comp["summary"], comp["other_role"], table_rows, comp["when_fde"], comp["other_role"], comp["when_other"], faq_html, related, get_cta_box())

    faq_schema = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_items}, indent=2)
    breadcrumb = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL},
        {"@type": "ListItem", "position": 2, "name": "Insights", "item": BASE_URL + "/insights/"},
        {"@type": "ListItem", "position": 3, "name": comp["title"], "item": BASE_URL + "/insights/" + comp["slug"] + "/"}
    ]}, indent=2)

    extra_head = '<script type="application/ld+json">\n' + faq_schema + '\n    </script>\n    <script type="application/ld+json">\n' + breadcrumb + '\n    </script>'

    html = get_html_head(
        title=comp["title"],
        description=comp["meta_desc"],
        canonical_path="/insights/" + comp["slug"] + "/",
        extra_head=extra_head
    )
    html += "\n<body>\n"
    html += get_header_html()
    html += "\n    <main>\n" + body + "\n    </main>\n"
    html += get_footer_html()
    html += get_mobile_nav_js()
    html += get_signup_js()
    html += "\n</body>\n</html>"
    return html


def generate_more_comparisons():
    print("  Generating additional comparison pages...")
    count = 0
    for comp in COMPARISONS:
        html = _build_page(comp)
        out_dir = os.path.join(SITE_DIR, 'insights', comp['slug'])
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        count += 1
    print("  " + str(count) + " additional comparison pages generated")


if __name__ == "__main__":
    generate_more_comparisons()
