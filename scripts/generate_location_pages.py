#!/usr/bin/env python3
"""Generate location-specific FDE job pages. Targets "fde jobs [location]" queries."""

import os, sys, json

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from nav_config import BASE_URL
from templates import get_html_head, get_header_html, get_footer_html, get_mobile_nav_js, get_signup_js, get_cta_box, get_related_links

SITE_DIR = os.path.join(os.path.dirname(script_dir), 'site')

LOCATIONS = [
    {
        "slug": "remote", "name": "Remote", "salary_range": "$155,000 - $280,000",
        "overview": "About 62% of Forward Deployed Engineer job postings offer remote or hybrid work. Remote FDE roles typically pay 5-15% below equivalent Bay Area on-site positions but offer location flexibility that increasingly matters to senior engineers. The catch: most remote FDE roles require 20-40% travel to customer sites. Fully remote with zero travel FDE positions represent less than 15% of postings.",
        "companies": "Salesforce (Agentforce FDE roles), Databricks (select positions), Cohere (Toronto-headquartered, remote-friendly), PostHog (fully remote company), Watershed (remote-first), some Palantir commercial deployments. OpenAI and Anthropic rarely offer fully remote FDE positions.",
        "market": "Remote FDE demand is growing but facing headwinds. Some companies are pulling FDEs back to customer sites as enterprise customers prefer on-site engagement. The tension between engineer preference (remote) and customer preference (on-site) defines the remote FDE market. Companies that offer truly remote FDE roles with limited travel have a hiring advantage. Salesforce's 'Work from Anywhere' policy for Agentforce FDEs is the most notable example of a large company committing to remote FDE work.",
        "tips": "When evaluating remote FDE roles, ask three questions: What percentage of time is spent at customer sites? Are customer visits concentrated (one week per month) or distributed (random travel)? Does the company pay location-adjusted or location-agnostic salaries? The answers determine whether 'remote' means flexibility or just working from home between customer trips.",
        "faq": [
            {"q": "Can Forward Deployed Engineers work fully remote?", "a": "Some can, but most remote FDE roles require 20-40% travel to customer sites. Fully remote with zero travel FDE positions exist but represent less than 15% of postings. Companies like PostHog and Watershed are the most remote-friendly. Larger companies like Salesforce offer remote FDE roles but expect periodic customer visits. If zero travel is a hard requirement, your options narrow significantly."},
            {"q": "Do remote FDEs earn less than on-site FDEs?", "a": "On average, 5-15% less in base salary. Some companies (Salesforce, Cohere) pay location-agnostic rates for remote FDE roles, effectively making them the highest-paying FDE positions when adjusted for cost of living outside SF/NYC. Other companies (Palantir, Ramp) apply location-based pay bands that reduce compensation for remote workers outside major tech hubs."},
            {"q": "Which companies hire remote Forward Deployed Engineers?", "a": "Salesforce (Agentforce), Databricks (select positions), Cohere, PostHog, Watershed, and various startups. OpenAI and Anthropic rarely offer remote FDE roles. Palantir offers some remote commercial FDE positions but government deployments require on-site presence. The trend is toward hybrid: remote with regular customer visits."},
            {"q": "Is remote FDE work sustainable long-term?", "a": "It depends on the travel burden. Remote FDEs who travel 20-30% report similar satisfaction to on-site engineers. Above 40% travel, burnout risk increases regardless of where your 'home base' is. The key variable is travel predictability: concentrated trips (one week per month at customer sites) are more sustainable than unpredictable ad-hoc travel."},
            {"q": "How do remote FDEs collaborate with customer teams?", "a": "Video calls, shared development environments (cloud IDEs, pair programming tools), async documentation, and periodic on-site visits. Most remote FDEs front-load on-site time at the start of a deployment (first 1-2 weeks embedded with the customer) then transition to remote work for ongoing development. This hybrid model balances relationship building with execution efficiency."},
        ],
    },
    {
        "slug": "new-york", "name": "New York City", "salary_range": "$165,000 - $290,000",
        "overview": "New York City is the second-largest FDE job market after San Francisco. NYC FDE roles skew toward fintech (Ramp, Stripe), enterprise SaaS (Rippling, ServiceNow), and consulting (PwC, Deloitte). The financial services concentration creates unique FDE demand: banks, hedge funds, and insurance companies deploying AI and analytics platforms need engineers who understand both the technology and financial regulation.",
        "companies": "Ramp (HQ), Rippling (major office), Palantir (major office), PwC (HQ), Deloitte (major office), Goldman Sachs (internal FDE-equivalent roles), JPMorgan (internal FDE-equivalent), various fintech and enterprise startups. Salesforce has NYC-based Agentforce FDE positions.",
        "market": "NYC FDE salaries are 5-10% above the national average, reflecting the city's high cost of living and the premium that financial services companies pay for technical talent. The fintech concentration means NYC FDEs are more likely to work with financial data, regulatory systems, and banking infrastructure than FDEs in San Francisco who skew toward AI and developer tools. NYC FDE roles are predominantly in-office or hybrid, with fewer fully remote options than the SF market.",
        "tips": "NYC FDE candidates should highlight any financial services or fintech experience. Understanding of banking regulations (SOX, PCI-DSS), financial data standards, and ERP systems (NetSuite, SAP) differentiates NYC candidates. The Ramp and Rippling FDE teams are particularly accessible for engineers already in the NYC market. Palantir's NYC office focuses on financial services and healthcare deployments.",
        "faq": [
            {"q": "Which NYC companies hire Forward Deployed Engineers?", "a": "Ramp (headquartered in NYC), Rippling (major NYC office), Palantir (NYC office focused on finance/healthcare), PwC, Deloitte, and various fintech startups. Salesforce has NYC-based Agentforce FDE positions. Goldman Sachs and JPMorgan hire for FDE-equivalent roles internally under titles like 'Platform Engineer' or 'Client Solutions Engineer.'"},
            {"q": "What is the FDE salary in NYC?", "a": "NYC FDE base salaries range from $165,000 to $290,000, approximately 5-10% above the national average. Total compensation including equity can reach $350,000+ at senior levels. NYC's cost of living is high but FDE salaries are competitive with other top-paying engineering roles in the city. Fintech FDE roles at companies like Ramp may include equity in fast-growing startups."},
            {"q": "Are NYC FDE roles in-office?", "a": "Most NYC FDE roles are in-office or hybrid (3-4 days per week). Ramp has a strong in-office culture. Palantir's NYC office expects regular in-office presence. Some companies offer hybrid arrangements with customer site travel. Fully remote FDE positions based in NYC exist but are less common than in the SF market."},
            {"q": "Do NYC FDEs need financial services experience?", "a": "Not required but it's a meaningful differentiator. NYC's FDE market skews toward fintech and financial services. Understanding of banking regulations, financial data standards, and enterprise finance systems (NetSuite, SAP, Workday) helps NYC FDE candidates stand out. Engineers with both strong coding skills and financial domain knowledge are especially competitive."},
            {"q": "Is NYC or San Francisco better for FDE careers?", "a": "SF has more FDE roles total (especially at AI companies like OpenAI, Anthropic, and Databricks). NYC has a stronger fintech and enterprise FDE market. SF salaries are slightly higher on average but NYC cost of living is comparable. If you want to work at AI companies, SF is stronger. If you want fintech or enterprise SaaS FDE roles, NYC is equally strong. Both cities offer excellent FDE career opportunities."},
        ],
    },
    {
        "slug": "san-francisco", "name": "San Francisco", "salary_range": "$175,000 - $300,000",
        "overview": "San Francisco is the epicenter of the Forward Deployed Engineer job market. The majority of FDE-hiring companies are headquartered in SF or the broader Bay Area: OpenAI, Anthropic, Salesforce, Databricks, Scale AI, Rippling, Watershed, and dozens of startups. SF FDE roles pay the highest salaries in the market and offer the most exposure to leading-edge AI deployment work.",
        "companies": "OpenAI (HQ), Anthropic (HQ), Salesforce (HQ), Databricks (HQ), Scale AI (HQ), Rippling (HQ), Watershed (HQ), PostHog, Cohere (SF office), and 30+ startups with FDE roles. Palantir's Palo Alto office is nearby. The concentration of AI companies makes the Bay Area the strongest market for AI-focused FDE roles specifically.",
        "market": "SF FDE demand outpaces supply. Companies compete aggressively for engineers with both strong coding skills and customer-facing experience. The AI focus means SF FDE roles increasingly require LLM deployment experience, which further narrows the candidate pool. Salaries reflect this scarcity: $175,000-$300,000 base, with total compensation reaching $400,000-$500,000+ at companies like OpenAI and Databricks including equity. The trade-off is SF's high cost of living, though FDE salaries more than compensate.",
        "tips": "SF FDE candidates should invest in AI/ML skills: prompt engineering, RAG architecture, model evaluation, and LLM integration. These skills are table-stakes for SF FDE roles and differentiating everywhere else. Network directly with FDE teams at target companies through SF tech meetups, AI/ML events, and engineering blog communities. The SF FDE market is relationship-driven: referrals carry significant weight.",
        "faq": [
            {"q": "Which SF companies have the largest FDE teams?", "a": "Salesforce (building to 1,000 FDEs), Palantir/Palo Alto (200+ total), OpenAI (50+), Databricks (30+), Scale AI (20+), Rippling (10-20). The SF market has the highest concentration of FDE roles globally. Adding in smaller startups and consulting firms, there are 200+ active FDE positions in the Bay Area at any given time."},
            {"q": "What is the FDE salary in San Francisco?", "a": "SF FDE base salaries range from $175,000 to $300,000, the highest in the FDE market. Total compensation including equity can reach $400,000-$500,000+ at senior levels at companies like OpenAI and Databricks. Even adjusted for SF's high cost of living, FDE compensation is competitive with top-paying FAANG engineering roles."},
            {"q": "Do SF FDE roles require AI experience?", "a": "Increasingly, yes. About 45% of SF FDE postings now request LLM/AI experience, up from near zero a year ago. AI companies (OpenAI, Anthropic, Databricks, Scale AI) require it. Enterprise SaaS companies (Salesforce, Rippling) prefer it but don't require it. If you're targeting SF specifically, investing in AI skills is high-ROI."},
            {"q": "Is it worth relocating to SF for an FDE role?", "a": "If you're targeting AI-company FDE roles, yes. The concentration of AI FDE opportunities in SF is unmatched. Remote alternatives exist but are fewer and typically require travel to SF anyway. If you're open to non-AI FDE roles, NYC and remote options are competitive alternatives that don't require SF relocation. The cost of living difference is the main consideration."},
            {"q": "How competitive is the SF FDE job market?", "a": "Highly competitive but in the candidate's favor. More FDE openings than qualified candidates. Companies compete on compensation, equity, and mission to attract FDE talent. A strong engineer with customer-facing experience and AI skills will receive multiple offers. The interview process is rigorous (4-6 rounds) but once you pass, the negotiation power is significant."},
        ],
    },
    {
        "slug": "london", "name": "London", "salary_range": "£90,000 - £180,000",
        "overview": "London is the largest FDE market outside the United States. Several major FDE-hiring companies have expanded to London: Anthropic, Palantir, Databricks, Salesforce, and DeepMind/Google. The European AI boom and EU AI Act regulatory requirements are creating additional demand for FDEs who can deploy AI systems while navigating European compliance frameworks. London FDE roles often serve European enterprise customers, making multilingual skills a differentiator.",
        "companies": "Anthropic (London office), Palantir (London office, government and commercial), Databricks (London office), Salesforce (London), Google DeepMind (London HQ), PwC UK, Deloitte UK, and various European fintech and AI startups. The London market also includes FDE-equivalent roles at banks (Barclays, HSBC, Goldman Sachs London) that deploy analytics and AI platforms internally.",
        "market": "London FDE salaries are £90,000-£180,000 base, lower than US equivalents in absolute terms but competitive within the London market. Total compensation including equity at companies like Anthropic and Databricks can reach £200,000-£300,000+. The EU AI Act is creating unique demand for FDEs who understand both technical deployment and European AI regulation. This regulatory expertise is a London-specific differentiator that SF and NYC FDEs don't need.",
        "tips": "London FDE candidates should highlight any experience with European data regulations (GDPR, EU AI Act), cross-border data transfer, and European enterprise software ecosystems. Anthropic and Palantir's London FDE teams are actively growing. The London FDE market is less competitive than SF for qualified candidates, meaning strong engineers can access opportunities that would be harder to land in the US.",
        "faq": [
            {"q": "Which London companies hire Forward Deployed Engineers?", "a": "Anthropic, Palantir, Databricks, Salesforce, Google DeepMind, PwC UK, and Deloitte UK all have London-based FDE or FDE-equivalent positions. Several European AI startups also hire FDEs in London. The London FDE market is smaller than SF or NYC but growing faster as US companies expand their European operations."},
            {"q": "What is the FDE salary in London?", "a": "London FDE base salaries range from £90,000 to £180,000. Total compensation including equity at companies like Anthropic and Databricks can reach £200,000-£300,000+. While lower than US FDE salaries in absolute terms, London FDE compensation is competitive within the London tech market and significantly above average UK engineering salaries."},
            {"q": "Do I need a visa to work as an FDE in London?", "a": "Non-UK citizens need a Skilled Worker visa. Most FDE-hiring companies in London are established sponsors (Anthropic, Palantir, Databricks, Salesforce, Google). The Skilled Worker visa requires employer sponsorship and meeting a minimum salary threshold (which all FDE salaries exceed). Processing time is typically 3-8 weeks. Companies hiring FDEs are generally experienced with visa sponsorship."},
            {"q": "Is the London FDE market growing?", "a": "Yes, faster than the overall European tech market. US AI companies are expanding London offices to serve European enterprise customers. The EU AI Act is creating demand for FDEs who can navigate European regulatory requirements. London's FDE market is expected to double in size over the next 2-3 years as more companies establish European FDE teams."},
            {"q": "Do London FDEs travel to European customer sites?", "a": "Frequently. London-based FDEs often serve customers across the UK and continental Europe. Travel to Paris, Berlin, Amsterdam, and Zurich is common. European FDE travel tends to be shorter trips (2-3 days) rather than the multi-week embeddings typical of US FDE deployments. Some London FDE roles are primarily UK-focused with minimal European travel."},
        ],
    },
    {
        "slug": "india", "name": "India", "salary_range": "₹25,00,000 - ₹70,00,000",
        "overview": "India's Forward Deployed Engineer market is emerging, driven by US companies establishing India-based FDE teams and Indian companies adopting the FDE model. The largest FDE employers in India are HackerRank (Bangalore), Palantir (Hyderabad office), and various US companies with India development centers. FDE salaries in India are lower than US equivalents but represent top-tier compensation within the Indian tech market.",
        "companies": "HackerRank (Bangalore, significant FDE team), Palantir (Hyderabad), Salesforce India, Databricks India, PwC India, Deloitte India, and various Indian enterprise software companies. US startups with India engineering centers are increasingly hiring FDE roles to support APAC customer deployments.",
        "market": "India FDE salaries range from ₹25,00,000 to ₹70,00,000 (approximately $30,000-$84,000 USD), placing them in the top 10-15% of Indian tech salaries. The market is growing as US companies recognize that India-based FDEs can support APAC customers at lower cost than US-based teams. HackerRank's India FDE team is the most established. The role is still relatively new in India, meaning early entrants can shape the FDE function at their companies.",
        "tips": "India-based FDE candidates should focus on strong engineering fundamentals and English communication skills. Experience with US enterprise software (Salesforce, AWS, GCP) is highly valued. The path to FDE roles in India often starts with software engineering or consulting at MNCs (multinational corporations) that have Indian offices. Demonstrating customer-facing experience, even from internal stakeholder work, helps bridge the gap.",
        "faq": [
            {"q": "Which companies hire FDEs in India?", "a": "HackerRank (Bangalore) has the most established India FDE team. Palantir has a Hyderabad office with FDE-adjacent roles. Salesforce India, Databricks India, PwC India, and Deloitte India hire for FDE and FDE-equivalent positions. US startups with India development centers are increasingly adding FDE roles to support APAC customers."},
            {"q": "What is the FDE salary in India?", "a": "FDE salaries in India range from ₹25,00,000 to ₹70,00,000 (approximately $30,000-$84,000 USD). This places FDE roles in the top 10-15% of Indian tech salaries. Senior FDEs at US companies with India offices can earn higher. Equity grants from US companies add significant upside potential for India-based FDEs."},
            {"q": "Is FDE a recognized role in India?", "a": "It's emerging but not yet mainstream. Most Indian tech professionals are unfamiliar with the FDE title. The role is best understood at companies with US headquarters that use the title globally (HackerRank, Palantir, Salesforce). As more US companies expand India FDE teams, recognition will grow. Being early to the FDE title in India is an advantage for career positioning."},
            {"q": "Can India-based FDEs transfer to US offices?", "a": "Possible at companies with both India and US offices (Palantir, Salesforce, Databricks). Internal transfers typically require 1-2 years of strong performance plus visa sponsorship (H-1B or L-1). India-based FDE experience is valued for US transfers because it demonstrates customer-facing engineering skills. Competition for US transfers is high but FDE skills are in demand."},
            {"q": "How is the India FDE market different from the US?", "a": "India FDE roles tend to support APAC customers rather than US customers (though some support US customers in overlapping time zones). The technical work is similar but customer communication may require adjusting for different business cultures. India FDE teams are generally younger (less established) with more greenfield opportunity to define processes and playbooks."},
        ],
    },
]


def generate_location_pages():
    print("  Generating location pages...")
    count = 0
    for loc in LOCATIONS:
        related = get_related_links([
            {"href": "/salaries/", "label": "FDE Salary Data"},
            {"href": "/companies/", "label": "Companies Hiring FDEs"},
            {"href": "/career/what-is-a-forward-deployed-engineer/", "label": "What Is an FDE?"},
            {"href": "/career/forward-deployed-engineer-work-life-balance/", "label": "FDE Work-Life Balance"},
        ])
        faq_html = ""
        faq_items = []
        for faq in loc["faq"]:
            faq_html += '''
                <div style="margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border);">
                    <h3 style="font-size: 1.15rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">%s</h3>
                    <p style="color: var(--text-secondary); line-height: 1.7;">%s</p>
                </div>''' % (faq["q"], faq["a"])
            faq_items.append({"@type": "Question", "name": faq["q"], "acceptedAnswer": {"@type": "Answer", "text": faq["a"]}})

        body = '''
        <section class="section" style="max-width: 900px; margin: 0 auto; padding-top: 8rem;">
            <h1 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">Forward Deployed Engineer Jobs in %s</h1>
            <p style="font-size: 1rem; color: var(--text-muted); margin-bottom: 2rem;">Salary Range: %s</p>

            <div style="color: var(--text-secondary); font-size: 1.05rem; line-height: 1.8;">
                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 0 0 1rem;">Market Overview</h2>
                <p style="margin-bottom: 1.25rem;">%s</p>

                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Companies Hiring FDEs in %s</h2>
                <p style="margin-bottom: 1.25rem;">%s</p>

                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">The %s FDE Market</h2>
                <p style="margin-bottom: 1.25rem;">%s</p>

                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Tips for %s FDE Candidates</h2>
                <p style="margin-bottom: 1.25rem;">%s</p>

                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Frequently Asked Questions</h2>
                %s
            </div>

            %s

            %s
        </section>
''' % (loc["name"], loc["salary_range"], loc["overview"], loc["name"], loc["companies"], loc["name"], loc["market"], loc["name"], loc["tips"], faq_html, related, get_cta_box())

        faq_schema = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_items}, indent=2)
        breadcrumb = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": "Jobs", "item": BASE_URL + "/jobs/"},
            {"@type": "ListItem", "position": 3, "name": loc["name"], "item": BASE_URL + "/jobs/" + loc["slug"] + "/"}
        ]}, indent=2)

        extra_head = '<script type="application/ld+json">\n' + faq_schema + '\n    </script>\n    <script type="application/ld+json">\n' + breadcrumb + '\n    </script>'

        page_title = "FDE Jobs in " + loc["name"] if loc["slug"] != "remote" else "Remote FDE Jobs"
        html = get_html_head(
            title=page_title + ". Salary & Companies",
            description="Forward Deployed Engineer jobs in " + loc["name"] + ". " + loc["salary_range"] + " salary range, companies hiring, and market analysis.",
            canonical_path="/jobs/" + loc["slug"] + "/",
            extra_head=extra_head
        )
        html += "\n<body>\n"
        html += get_header_html()
        html += "\n    <main>\n" + body + "\n    </main>\n"
        html += get_footer_html()
        html += get_mobile_nav_js()
        html += get_signup_js()
        html += "\n</body>\n</html>"

        out_dir = os.path.join(SITE_DIR, 'jobs', loc['slug'])
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        count += 1

    print("  " + str(count) + " location pages generated")


if __name__ == "__main__":
    generate_location_pages()
