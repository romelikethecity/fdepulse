#!/usr/bin/env python3
"""Generate specialized topical pages: AI FDE, Strategist, Levels, Work-Life, Hiring Manager, Tech Stack."""

import os, sys, json
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
from nav_config import BASE_URL
from templates import get_html_head, get_header_html, get_footer_html, get_mobile_nav_js, get_signup_js, get_cta_box, get_related_links, get_article_schema
SITE_DIR = os.path.join(os.path.dirname(script_dir), 'site')

PAGES = [
    {
        "slug": "forward-deployed-ai-engineer", "dir": "career",
        "title": "Forward Deployed AI Engineer Guide",
        "meta_desc": "Forward Deployed AI Engineer guide. LLM deployment skills, salary ($180K-$300K), companies hiring, and how the AI FDE role differs from standard FDE.",
        "content": """<p style="margin-bottom: 1.25rem;">Forward Deployed AI Engineer is the fastest-growing FDE specialization. As AI companies shifted from research to enterprise deployment in 2024-2025, they needed engineers who could take powerful models and make them work in customer-specific production environments. The Forward Deployed AI Engineer (sometimes called AI FDE or FD AI Engineer) combines traditional FDE skills with deep AI/ML deployment expertise.</p>

<p style="margin-bottom: 1.25rem;">45% of FDE job postings at AI companies now request LLM integration experience, up from near zero in 2024. Companies like OpenAI, Anthropic, Cohere, and Databricks have made AI skills a core requirement for their FDE teams. This isn't a separate role from FDE. it's the FDE role evolving to match what enterprise AI deployment actually requires.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">What Forward Deployed AI Engineers Do</h2>

<p style="margin-bottom: 1.25rem;">AI FDEs deploy language models, ML systems, and AI infrastructure at customer sites. Typical projects include:</p>

<ul style="margin-bottom: 1.25rem; padding-left: 1.5rem;">
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">RAG architecture design:</strong> Building retrieval-augmented generation systems over customer proprietary data (contracts, medical records, financial documents, internal wikis)</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Custom agent workflows:</strong> Deploying AI agents that use tools, access databases, and execute multi-step workflows specific to each customer's business processes</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Model evaluation and optimization:</strong> Measuring model performance on customer-specific benchmarks, optimizing prompts and retrieval strategies, and building evaluation frameworks</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Safety and guardrails:</strong> Implementing content filtering, output validation, and safety systems specific to regulated industries (healthcare, finance, legal)</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">On-premise model deployment:</strong> Deploying models on customer infrastructure for data-sovereign customers who can't use cloud APIs (Cohere specializes in this)</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Fine-tuning and customization:</strong> Training custom models on customer data for domain-specific performance improvements</li>
</ul>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Required Skills</h2>

<p style="margin-bottom: 1.25rem;">Forward Deployed AI Engineers need everything a standard FDE needs (Python, SQL, API design, customer communication) plus AI-specific skills:</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Must-have:</strong> LLM API integration (OpenAI, Anthropic, Cohere SDKs), prompt engineering (chain-of-thought, few-shot, system prompts), RAG architecture (vector databases, embedding models, retrieval strategies), and model evaluation (accuracy metrics, hallucination detection, latency optimization).</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Strongly preferred:</strong> Fine-tuning experience (LoRA, PEFT), ML infrastructure (model serving, GPU optimization, batch vs. streaming inference), AI safety (content filtering, output validation, red-teaming), and familiarity with AI frameworks (LangChain, LlamaIndex, Haystack, CrewAI).</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Differentiating:</strong> On-premise model deployment (vLLM, TensorRT, NVIDIA Triton), multi-modal AI (vision + text), AI compliance (EU AI Act, HIPAA for healthcare AI), and experience building production AI systems that handle edge cases gracefully.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Salary</h2>

<p style="margin-bottom: 1.25rem;">AI FDE salaries range from $180,000 to $300,000+ base. approximately 10-20% above non-AI FDE roles at equivalent seniority. The premium reflects the scarcity of engineers with combined LLM deployment expertise and customer-facing skills. At OpenAI, senior AI FDEs can earn $250,000-$300,000+ base with equity pushing total comp above $500,000. Anthropic and Cohere pay similarly at senior levels. Databricks AI FDE compensation includes significant pre-IPO equity.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Companies Hiring AI FDEs</h2>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Pure AI companies:</strong> <a href="/companies/openai/" style="color: var(--amber-light);">OpenAI</a> (50+ FDEs), <a href="/companies/anthropic/" style="color: var(--amber-light);">Anthropic</a> (20-30), <a href="/companies/cohere/" style="color: var(--amber-light);">Cohere</a> (10-15), <a href="/companies/scale-ai/" style="color: var(--amber-light);">Scale AI</a> (20+). These companies require the deepest AI skills.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Data/ML platforms:</strong> <a href="/companies/databricks/" style="color: var(--amber-light);">Databricks</a> (30+), Snowflake, Weights & Biases. AI deployment is built into the platform, so FDEs need ML pipeline expertise alongside LLM skills.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Enterprise AI features:</strong> <a href="/companies/salesforce/" style="color: var(--amber-light);">Salesforce</a> (Agentforce), <a href="/companies/servicenow/" style="color: var(--amber-light);">ServiceNow</a> (Now Assist), <a href="/companies/atlassian/" style="color: var(--amber-light);">Atlassian</a> (Atlassian Intelligence). These companies add AI layers to existing enterprise products. AI skills are preferred but not always required.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">How to Transition to AI FDE</h2>

<p style="margin-bottom: 1.25rem;">If you're a current FDE or SWE wanting to move into AI FDE work, the fastest path is building hands-on LLM deployment experience. Build a RAG system over a real dataset. Deploy an AI agent that uses tools. Fine-tune a model for a specific task. Contribute to open-source AI deployment tools (LangChain, LlamaIndex). The gap between 'I've used ChatGPT' and 'I've deployed LLMs in production' is what AI FDE interviews test for.</p>

<p style="margin-bottom: 1.25rem;">Current FDEs have an advantage: you already have the customer-facing skills that pure ML engineers lack. Adding AI deployment skills to your existing FDE toolkit makes you a rare and highly compensated candidate. Most FDE-to-AI-FDE transitions happen within 6-12 months of focused AI skill development.</p>""",
        "faq": [
            {"q": "Is Forward Deployed AI Engineer a separate role from FDE?", "a": "Not formally. 'Forward Deployed AI Engineer' describes an FDE who specializes in AI deployment. Some companies use the explicit title (Adobe, Tribe AI). Most companies simply list 'Forward Deployed Engineer' with AI skills as requirements. The specialization is real (AI deployment requires distinct skills), but it's usually a flavor of FDE rather than a separate job title."},
            {"q": "Do I need a PhD for Forward Deployed AI Engineer roles?", "a": "No. AI FDE roles prioritize practical deployment experience over academic credentials. A strong software engineer with hands-on LLM deployment projects is more competitive than a PhD researcher without customer-facing experience. That said, understanding how models work at a conceptual level (not just API calls) is essential. You need to debug model behavior, optimize inference, and explain AI capabilities to non-technical customers."},
            {"q": "What is the salary for Forward Deployed AI Engineers?", "a": "$180,000 to $300,000+ base, with total compensation reaching $400,000-$500,000+ at senior levels at companies like OpenAI and Databricks. AI FDEs earn 10-20% more than non-AI FDEs at equivalent seniority because the skill combination (strong engineering + AI expertise + customer communication) is rare."},
            {"q": "Will AI replace Forward Deployed Engineers?", "a": "Not in the foreseeable future. AI products become more complex over time, not simpler. Each new AI capability creates new deployment challenges that require human engineers to solve. AI tools will make FDEs more productive (faster coding, better documentation, automated testing), but the need for humans who understand both the technology and the customer's business context will persist. FDE is one of the roles most insulated from AI displacement because it fundamentally requires human judgment and communication."},
            {"q": "What's the best way to learn AI skills for FDE work?", "a": "Build projects, not courses. Deploy a RAG system over real documents. Build an AI agent that uses tools. Fine-tune a small model for a specific task. Contribute to LangChain, LlamaIndex, or similar projects. AI FDE interviews test practical deployment ability. Courses provide theoretical foundation but projects demonstrate the hands-on skills FDE work requires."},
        ],
    },
    {
        "slug": "forward-deployed-strategist", "dir": "career",
        "title": "Forward Deployed Strategist Guide",
        "meta_desc": "What a Forward Deployed Strategist does, how it differs from FDE, salary ranges, and which companies hire. Palantir, Salesforce, ElevenLabs, and more.",
        "content": """<p style="margin-bottom: 1.25rem;">A Forward Deployed Strategist (FDS) is the business-focused counterpart to the Forward Deployed Engineer. While FDEs build technical solutions, Forward Deployed Strategists help customers define what to build, why, and how to measure success. The role combines management consulting skills with technical fluency. FDS is common at Palantir (where it originated alongside FDE) and is spreading to companies like Salesforce, ElevenLabs, and Workhelix.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">What Forward Deployed Strategists Do</h2>

<p style="margin-bottom: 1.25rem;">Forward Deployed Strategists work alongside FDEs at customer sites, handling the business and organizational side of deployments. Day-to-day work includes: scoping deployment projects (defining success criteria, timelines, resource requirements), managing customer stakeholder relationships (C-suite, department heads, IT leadership), translating business problems into technical requirements for FDE teams, building business cases for expansion (ROI analysis, adoption metrics, executive presentations), and navigating organizational change management as customers adopt new technology.</p>

<p style="margin-bottom: 1.25rem;">At Palantir, FDS and FDE work as a pair: the FDS owns the business relationship and project scope, the FDE owns the technical implementation. At Salesforce, the Agentforce team has similar FDS-equivalent roles (sometimes titled 'Customer Success Architect' or 'Deployment Strategist'). At ElevenLabs, the Forward Deployed Strategist focuses on enterprise account expansion and use case discovery.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">FDS vs FDE: Key Differences</h2>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Technical depth:</strong> FDEs write production code. FDS can read and understand code but primarily works in strategy documents, project plans, and stakeholder presentations. FDS is not a coding role.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Customer interface:</strong> FDEs work with customer engineering teams. FDS works with customer executives and business stakeholders. FDS navigates C-suite politics that FDEs rarely encounter.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Background:</strong> FDEs come from software engineering. FDS typically comes from management consulting (McKinsey, BCG, Bain), business operations, or product management. Some FDS have engineering degrees but chose the business track.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Compensation:</strong> FDS salaries range from $120,000 to $220,000 base, below FDE ($150,000-$300,000). The gap reflects the lower demand for business strategy versus engineering skills in the current market. However, FDS roles at Palantir include equity that can close the gap significantly.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Companies Hiring Forward Deployed Strategists</h2>

<ul style="margin-bottom: 1.25rem; padding-left: 1.5rem;">
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Palantir:</strong> The originator of the FDS title. Significant FDS team working across government, healthcare, energy, and financial services verticals.</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">ElevenLabs:</strong> Forward Deployed Strategist roles focused on enterprise account development and voice AI use case discovery.</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Salesforce:</strong> FDS-equivalent roles titled 'Customer Success Architect' or 'Agentforce Strategy Lead.'</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Workhelix:</strong> AI workforce planning company with FDS roles helping enterprise customers understand AI's impact on their workforce.</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">PwC / Deloitte:</strong> FDS-equivalent roles within technology consulting practices.</li>
</ul>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Career Path</h2>

<p style="margin-bottom: 1.25rem;">FDS career paths include: customer success leadership, business development, product management, management consulting partnership, corporate strategy, or founding a startup. The FDS skill set (business strategy + technical fluency + customer management) is valued in any role that bridges technology and business. FDS-to-product-management transitions are common at Palantir. FDS-to-consulting-partner transitions happen at Big 4 firms.</p>""",
        "faq": [
            {"q": "What is the salary for Forward Deployed Strategist?", "a": "$120,000 to $220,000 base depending on company and seniority. Palantir FDS total compensation including equity can reach $250,000-$350,000 at senior levels. Consulting firm FDS-equivalent roles pay $100,000-$180,000 base plus bonus. FDS salaries are lower than FDE because engineering skills command a higher market premium than strategy skills."},
            {"q": "Do I need an MBA for Forward Deployed Strategist?", "a": "Not required. Palantir hires FDS from diverse backgrounds including liberal arts, economics, political science, and engineering. Management consulting experience (even 2-3 years) is the strongest signal. An MBA helps but isn't necessary. What matters is the ability to structure ambiguous business problems, communicate with executives, and manage complex stakeholder relationships."},
            {"q": "Is FDS a stepping stone to FDE?", "a": "Rarely. FDS and FDE require fundamentally different skill sets. FDS is a business/strategy role; FDE is an engineering role. Moving from FDS to FDE would require developing strong software engineering skills, which is a 1-2 year investment at minimum. More commonly, FDS transitions to product management, business development, or consulting. not engineering."},
            {"q": "How does FDS compare to management consulting?", "a": "Very similar in daily work: stakeholder management, strategic analysis, project scoping, executive presentations. The key differences: FDS is embedded at one company deploying one product (like Palantir's Foundry). Consultants work across multiple clients and technologies. FDS has deeper product knowledge and customer relationships. Consulting offers broader industry exposure. Compensation is comparable at equivalent seniority levels."},
            {"q": "Can Forward Deployed Strategists work remotely?", "a": "Less commonly than FDEs. FDS work requires in-person executive relationships and organizational navigation that's harder to do remotely. Palantir FDS travel 40-60% to customer sites. Some hybrid arrangements exist. Fully remote FDS roles are rare because the role's value depends heavily on in-person relationship building."},
        ],
    },
    {
        "slug": "forward-deployed-engineer-levels", "dir": "career",
        "title": "FDE Levels & Career Progression",
        "meta_desc": "FDE career ladder from entry to Staff/Lead. Salary by level, promotion timelines, and how FDE levels compare to standard SWE levels at top companies.",
        "content": """<p style="margin-bottom: 1.25rem;">Forward Deployed Engineer career ladders vary by company, but most follow a 4-5 level progression that mirrors standard software engineering tracks. Understanding the levels helps with salary negotiation, career planning, and evaluating offers across companies. Here's the comprehensive breakdown.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">The FDE Career Ladder</h2>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">Level 1: Associate / Junior FDE (0-2 years)</strong></p>
<p style="margin-bottom: 0.5rem;">Salary: $130,000 - $165,000 base</p>
<p style="margin-bottom: 1.25rem;">Entry-level role available primarily at companies with structured FDE programs (Palantir FDSE, Salesforce FDE I). Works under supervision of senior FDEs. Handles specific technical tasks within larger customer deployments rather than running engagements independently. Focuses on developing both technical skills and customer communication fundamentals. Promotion to mid-level typically takes 1.5-2.5 years.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">Level 2: FDE / Mid-Level (2-5 years)</strong></p>
<p style="margin-bottom: 0.5rem;">Salary: $165,000 - $210,000 base</p>
<p style="margin-bottom: 1.25rem;">The bulk of FDE hiring targets this level. Can run customer deployments independently. Scopes work, designs solutions, implements code, and manages customer relationships without constant oversight. Expected to handle 2-3 customer engagements per year. Begins contributing to internal FDE processes and tooling. This is the level where most external FDE hires land.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">Level 3: Senior FDE (5-8 years)</strong></p>
<p style="margin-bottom: 0.5rem;">Salary: $200,000 - $260,000 base</p>
<p style="margin-bottom: 1.25rem;">Leads the most complex customer engagements. Manages a portfolio of enterprise accounts. Mentors junior FDEs. Contributes to product strategy through deployment feedback. Handles customer escalations and executive-level relationships. Expected to influence product roadmap decisions. At smaller companies, Senior FDE may be the highest individual contributor level.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">Level 4: Staff / Lead FDE (8-12+ years)</strong></p>
<p style="margin-bottom: 0.5rem;">Salary: $240,000 - $300,000+ base</p>
<p style="margin-bottom: 1.25rem;">Defines FDE practices and playbooks for the company. May manage a team of FDEs or lead a vertical (healthcare FDEs, financial services FDEs). Works cross-functionally with product, engineering, and sales leadership. Handles the most strategic customer relationships. At Palantir, this maps to 'Deployment Lead' or 'Head of Forward Deployment.' At Salesforce, maps to FDE III or Lead FDE.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">Level 5: FDE Director / VP (12+ years)</strong></p>
<p style="margin-bottom: 0.5rem;">Salary: $280,000 - $400,000+ base</p>
<p style="margin-bottom: 1.25rem;">Runs the FDE organization. Reports to CTO, VP Engineering, or CEO. Responsible for hiring, team structure, compensation, and FDE methodology. Owns the business metrics for FDE impact (customer deployment velocity, retention, expansion). This role exists at Palantir and is emerging at Salesforce and OpenAI as their FDE teams scale.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">FDE Levels vs. Standard SWE Levels</h2>

<p style="margin-bottom: 1.25rem;">FDE levels generally map to standard engineering levels with a 10-20% salary premium at each tier:</p>

<ul style="margin-bottom: 1.25rem; padding-left: 1.5rem;">
<li style="margin-bottom: 0.5rem;">Associate FDE ≈ SWE L3/E3 (Junior Software Engineer)</li>
<li style="margin-bottom: 0.5rem;">FDE (Mid) ≈ SWE L4/E4 (Software Engineer)</li>
<li style="margin-bottom: 0.5rem;">Senior FDE ≈ SWE L5/E5 (Senior Software Engineer)</li>
<li style="margin-bottom: 0.5rem;">Staff/Lead FDE ≈ SWE L6/E6 (Staff Engineer)</li>
<li style="margin-bottom: 0.5rem;">FDE Director ≈ Engineering Director / VP</li>
</ul>

<p style="margin-bottom: 1.25rem;">The promotion bar for FDE advancement includes both technical excellence and customer impact metrics. You can't advance by coding alone. you also need to demonstrate customer outcomes, cross-functional influence, and the ability to run increasingly complex engagements independently.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Promotion Timelines</h2>

<p style="margin-bottom: 1.25rem;">Typical time at each level before promotion:</p>

<ul style="margin-bottom: 1.25rem; padding-left: 1.5rem;">
<li style="margin-bottom: 0.5rem;">Associate → Mid: 1.5-2.5 years</li>
<li style="margin-bottom: 0.5rem;">Mid → Senior: 2-3 years</li>
<li style="margin-bottom: 0.5rem;">Senior → Staff/Lead: 3-5 years</li>
<li style="margin-bottom: 0.5rem;">Staff → Director: Varies widely (role availability dependent)</li>
</ul>

<p style="margin-bottom: 1.25rem;">These timelines are faster than standard SWE promotion timelines at FAANG companies because the FDE function is newer and growing. There's less of a 'waiting in line' dynamic. Companies actively need senior FDEs to lead growing teams. Engineers who demonstrate both technical and customer leadership skills can advance quickly.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Exit Paths from Each Level</h2>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">From Mid-Level FDE:</strong> Product management, solutions engineering leadership, or return to SWE at a higher level. The customer exposure at mid-level is already more than most SWEs get in 5-7 years.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">From Senior FDE:</strong> Engineering management, solutions architecture, customer engineering leadership, or founding a startup. Senior FDEs have enough context to start companies because they've seen real customer problems up close.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">From Staff/Director FDE:</strong> VP Engineering, CTO (at smaller companies), VP Customer Engineering, or consulting. At this level, you've built and managed teams, defined processes, and owned business outcomes. these skills transfer to any engineering leadership role.</p>""",
        "faq": [
            {"q": "What level should I negotiate for as an FDE candidate?", "a": "Map your experience to the levels above. 3-5 years of SWE experience with some customer-facing work typically maps to mid-level FDE. 5-8 years with significant customer deployment experience maps to senior. Don't accept a lower level than your experience warrants. it affects both immediate compensation and promotion timeline. If you're coming from a senior SWE role, you should be at minimum mid-level FDE, ideally senior."},
            {"q": "Do FDE levels transfer between companies?", "a": "Approximately, but each company calibrates differently. Senior FDE at a startup might map to mid-level FDE at Palantir or Salesforce. The best approach: negotiate based on your demonstrated skills and customer impact rather than your current title. Bring specific examples of customer deployments you've led, their complexity, and the business outcomes."},
            {"q": "Is Staff FDE a terminal level?", "a": "At most companies, yes. Staff/Lead FDE is the highest individual contributor level. Further advancement requires moving into management (FDE Director, VP). Some engineers prefer to stay at Staff level indefinitely for the technical work without management responsibilities. Companies like Palantir and Salesforce support both IC and management tracks at senior FDE levels."},
            {"q": "How does FDE compensation compare to SWE at the same level?", "a": "FDEs earn 10-20% more than SWEs at the same level and company. Mid-level FDE ($165K-$210K) vs. mid-level SWE ($150K-$190K). Senior FDE ($200K-$260K) vs. Senior SWE ($180K-$240K). The premium narrows at Staff level because Staff SWE roles at FAANG companies pay exceptionally well ($300K-$500K+ total comp) with no FDE equivalent at that ceiling."},
            {"q": "What metrics matter for FDE promotion?", "a": "Technical excellence (code quality, system design), customer outcomes (deployment success rate, time-to-value, customer satisfaction), cross-functional impact (product feedback that ships, process improvements), and team contribution (mentoring, documentation, internal tooling). Unlike SWE promotions that primarily evaluate technical output, FDE promotions require demonstrating customer impact alongside engineering quality."},
        ],
    },
    {
        "slug": "forward-deployed-engineer-work-life-balance", "dir": "career",
        "title": "FDE Work-Life Balance & Travel",
        "meta_desc": "Real talk on FDE work-life balance: travel expectations (20-60%), burnout risk, remote options, and how to evaluate FDE lifestyle by company.",
        "content": """<p style="margin-bottom: 1.25rem;">Work-life balance is the most common concern engineers raise about Forward Deployed Engineer roles. The travel, customer pressure, and context-switching are real. But the picture is more nuanced than 'FDE = no life.' The experience varies dramatically by company, and understanding those differences helps you pick the right FDE role for your lifestyle.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Travel Expectations by Company</h2>

<p style="margin-bottom: 1.25rem;">Travel is the single biggest lifestyle variable across FDE roles. Here's the realistic breakdown:</p>

<ul style="margin-bottom: 1.25rem; padding-left: 1.5rem;">
<li style="margin-bottom: 0.75rem;"><strong style="color: var(--text-primary);">Heavy (40-60%):</strong> Palantir, Anduril. Multi-week customer site embeddings. Government/defense deployments may require extended on-site presence. This is the original FDE model and the most travel-intensive.</li>
<li style="margin-bottom: 0.75rem;"><strong style="color: var(--text-primary);">Moderate (20-40%):</strong> OpenAI, Salesforce, Databricks, Ramp, Scale AI, ServiceNow. Periodic customer visits (1-2 weeks per month during active deployments). Travel is concentrated during deployment phases and lighter between engagements.</li>
<li style="margin-bottom: 0.75rem;"><strong style="color: var(--text-primary);">Light (10-20%):</strong> Cohere, Rippling, Atlassian. Primarily remote work with occasional customer site visits. Most customer interaction is virtual.</li>
<li style="margin-bottom: 0.75rem;"><strong style="color: var(--text-primary);">Minimal (0-10%):</strong> PostHog, Watershed. Fully remote companies with virtual customer engagement. Physical travel is rare and optional.</li>
</ul>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Burnout Risk Factors</h2>

<p style="margin-bottom: 1.25rem;">FDE burnout comes from three sources, not just travel:</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">1. Context-switching.</strong> FDEs switch between different customers, technology stacks, and business domains. Each deployment requires learning a new customer environment. Some engineers find this stimulating; others find it exhausting. If you prefer deep focus on a single codebase, FDE's variety may drain you.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">2. Customer pressure.</strong> FDEs work under direct customer scrutiny. When a deployment isn't going well, the customer's frustration is directed at you personally. This is more emotionally demanding than product engineering where customer feedback is filtered through PMs and support teams. Thick skin and the ability to separate professional pressure from personal stress are essential.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">3. Ambiguity.</strong> FDEs rarely get clear specs. They figure out solutions in messy customer environments with incomplete information. Some engineers thrive in ambiguity; others need clarity to be productive. If ambiguity stresses you, FDE will be harder than a well-structured product engineering role.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">How to Evaluate FDE Work-Life Before Accepting</h2>

<p style="margin-bottom: 1.25rem;">Ask these questions during the interview process:</p>

<ul style="margin-bottom: 1.25rem; padding-left: 1.5rem;">
<li style="margin-bottom: 0.5rem;">"What percentage of time do FDEs spend at customer sites versus working remotely?"</li>
<li style="margin-bottom: 0.5rem;">"Are customer visits concentrated (one week per month) or distributed (random travel)?"</li>
<li style="margin-bottom: 0.5rem;">"How many customers does a typical FDE work with simultaneously?"</li>
<li style="margin-bottom: 0.5rem;">"What does an FDE's week look like when they're not actively on a deployment?"</li>
<li style="margin-bottom: 0.5rem;">"What's the typical duration of a customer engagement?"</li>
<li style="margin-bottom: 0.5rem;">"How does the company handle FDE burnout or time-off between deployments?"</li>
</ul>

<p style="margin-bottom: 1.25rem;">The answers separate companies with healthy FDE cultures from those that will burn you out. A company that can't clearly describe what an FDE's 'off-deployment' time looks like probably doesn't have a sustainable model.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">The Honest Trade-off</h2>

<p style="margin-bottom: 1.25rem;">FDE work-life balance is worse than typical product engineering but better than management consulting. The travel is less than Big 4 consulting (which runs 40-80%). The compensation is higher than most SWE roles. The career acceleration is faster. The variety keeps the work interesting longer than many engineering roles.</p>

<p style="margin-bottom: 1.25rem;">If you're single, early-career, and want maximum learning, the travel-heavy FDE model (Palantir, Anduril) offers unmatched professional development. If you have a family or value routine, the remote-friendly FDE model (PostHog, Cohere, Atlassian) offers the FDE career path without the lifestyle sacrifice. The key is choosing the right company for your life stage.</p>""",
        "faq": [
            {"q": "Do Forward Deployed Engineers work weekends?", "a": "Occasionally during intense deployment phases, but it's not the norm. Most FDE work happens during standard business hours because customers operate on business schedules. Weekend work is more common at startups (Ramp, Rippling) during crunch periods and rare at larger companies (Salesforce, ServiceNow). Palantir and Anduril deployments can require extended hours when deadlines are tight."},
            {"q": "Can I be an FDE with a family?", "a": "Yes, but company choice matters enormously. PostHog (fully remote, near-zero travel), Cohere (remote-friendly, light travel), and Atlassian (distributed, flexible) are family-compatible FDE employers. Palantir and Anduril's heavy travel makes them harder with young children. Salesforce's hybrid model with 20-30% travel is manageable for most families. The key is negotiating travel expectations upfront and choosing companies that respect boundaries."},
            {"q": "Is FDE more or less stressful than regular software engineering?", "a": "More stressful on average because of customer pressure and ambiguity. Product SWEs deal with technical challenges but rarely face direct customer frustration. FDEs face both technical challenges and interpersonal pressure. However, many FDEs report higher job satisfaction because the impact is visible and immediate: you see customers use what you built. The stress is different in kind, not uniformly worse."},
            {"q": "Do FDE roles offer unlimited PTO?", "a": "Many do (especially at tech companies). The practical question is whether you can actually take it. FDE vacation depends on deployment schedules. Between engagements, taking extended time off is easier than for product SWEs who have sprint commitments. During active deployments, taking time off is harder because the customer depends on you. The best approach: plan vacations between deployment cycles."},
            {"q": "What happens when an FDE burns out?", "a": "At well-run companies (Palantir, Salesforce, OpenAI), there are off-ramps: moving to a product engineering role temporarily, taking a sabbatical between deployments, or transitioning to an internal-facing role (tooling, documentation, training). At smaller companies without these structures, burned-out FDEs typically switch companies or roles entirely. If burnout is a concern, ask about internal mobility during the interview process."},
        ],
    },
    {
        "slug": "how-to-hire-forward-deployed-engineers", "dir": "insights",
        "title": "How to Hire Forward Deployed Engineers",
        "meta_desc": "FDE hiring playbook: job description templates, interview process design, compensation benchmarks, and how to build an FDE team from scratch.",
        "content": """<p style="margin-bottom: 1.25rem;">Hiring Forward Deployed Engineers is different from hiring standard software engineers. The candidate pool is smaller, the interview process needs additional rounds, and the compensation expectations are higher. This guide covers everything a hiring manager needs to build and staff an FDE team.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Writing the FDE Job Description</h2>

<p style="margin-bottom: 1.25rem;">Common mistakes in FDE job descriptions that reduce applicant quality:</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Mistake 1: Listing it as a SWE role with 'customer-facing' tacked on.</strong> This attracts SWEs who tolerate customer work rather than engineers who want it. Lead with the customer-deployment aspect. The best FDE candidates are actively looking for roles that combine engineering with customer impact.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Mistake 2: Requiring 10+ years of experience.</strong> The FDE role is too new for anyone to have 10 years of titled FDE experience. The best candidates have 3-7 years of SWE experience with some customer-facing work (consulting, support engineering, solutions architecture). Lower the year requirements and evaluate on demonstrated skills instead.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Mistake 3: Not disclosing salary range.</strong> FDE candidates have multiple options. Postings without salary ranges get fewer applications. Be transparent about compensation. it saves everyone time.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Mistake 4: Not explaining what makes your FDE role different.</strong> 50+ companies hire FDEs. Your posting should explain: what customers you'll serve, what technology you'll deploy, what a typical engagement looks like, and how much travel is involved. Generic FDE postings lose to companies that paint a specific picture.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Designing the FDE Interview Process</h2>

<p style="margin-bottom: 1.25rem;">The standard FDE interview has 4-5 rounds:</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Round 1: Recruiter Screen (30 min).</strong> Verify the candidate understands what FDE means. Many applicants think it's a standard SWE role. Ask: "Why FDE instead of a product engineering role?" The answer reveals whether they genuinely want customer-facing work.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Round 2-3: Technical Coding (45-60 min each).</strong> Use practical coding problems rather than pure algorithm challenges. Good FDE coding questions involve: building an API integration, processing messy data, or designing a data pipeline. The coding should resemble actual FDE work. Evaluate code quality, communication during coding, and handling of edge cases.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Round 4: Customer Scenario (45-60 min).</strong> This is the FDE-specific round that doesn't exist in standard SWE interviews. Give the candidate a realistic customer problem. One interviewer plays the customer. Evaluate: Does the candidate ask clarifying questions? Can they explain technical trade-offs in plain English? Do they manage scope and expectations? Can they handle pushback gracefully? This round is the strongest predictor of FDE success.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Round 5: Behavioral / Team Fit (30-45 min).</strong> Focus on stories about working independently, handling ambiguity, and navigating difficult customer situations. FDEs need high autonomy and emotional resilience. Probe for evidence of both.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Compensation Benchmarks</h2>

<p style="margin-bottom: 1.25rem;">FDE compensation by level (2026 data from FDE Pulse):</p>

<ul style="margin-bottom: 1.25rem; padding-left: 1.5rem;">
<li style="margin-bottom: 0.5rem;">Junior/Associate FDE: $130,000-$165,000 base + equity</li>
<li style="margin-bottom: 0.5rem;">Mid-Level FDE: $165,000-$210,000 base + equity</li>
<li style="margin-bottom: 0.5rem;">Senior FDE: $200,000-$260,000 base + equity</li>
<li style="margin-bottom: 0.5rem;">Staff/Lead FDE: $240,000-$300,000+ base + equity</li>
</ul>

<p style="margin-bottom: 1.25rem;">FDEs expect 10-20% more than equivalent-seniority SWEs. If your SWE band for mid-level is $150,000-$180,000, your FDE band should be $165,000-$210,000. Under-paying relative to market costs you in candidate quality and retention. FDE candidates have strong bargaining power because the talent pool is small.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Building an FDE Team from Scratch</h2>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Start with 2-3 senior FDEs.</strong> Don't hire junior FDEs until you have senior people to define processes, build playbooks, and mentor. Your first FDE hires will shape the entire function.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Define the FDE-product feedback loop.</strong> FDEs generate the most valuable product feedback in your company. Build formal channels for FDE insights to reach the product team. Without this, FDE feedback gets lost and the product team builds features that don't match customer deployment reality.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Invest in FDE tooling.</strong> FDEs are more productive when they have reusable deployment tools, documentation templates, and customer environment setup automation. Budget for internal FDE tooling from day one. Palantir and Salesforce both invest heavily in FDE-specific internal tools.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Define deployment playbooks early.</strong> Document what a successful deployment looks like: scoping checklist, technical requirements gathering template, deployment milestones, customer sign-off criteria, and handoff process. These playbooks become the foundation for scaling the FDE team beyond the first 3-5 hires.</p>""",
        "faq": [
            {"q": "How many FDEs do I need per enterprise customer?", "a": "It depends on deployment complexity. Simple product deployments: 0.5-1 FDE per customer (one FDE manages 2-3 customers). Complex AI or analytics deployments: 1-2 FDEs per customer during active deployment phase. Post-deployment support: 0.25-0.5 FDE per customer. Plan for 1 FDE per active customer engagement as a starting ratio, then adjust based on actual deployment intensity."},
            {"q": "Should FDEs report to engineering or sales?", "a": "Engineering, not sales. FDEs who report to sales leadership face pressure to prioritize new deals over customer deployment quality. Engineering leadership understands the technical nature of FDE work and can evaluate FDE performance on engineering quality metrics. Some companies create a separate 'FDE org' that reports to the CTO or a dedicated VP. Avoid putting FDEs in the customer success org. the engineering caliber suffers."},
            {"q": "Where do I find FDE candidates?", "a": "Former consultants (McKinsey, BCG, PwC, Deloitte technology practices) with CS backgrounds. Solutions Engineers looking for more technical depth. SWEs at companies with customer-facing engineering culture. DevRel engineers who want to write more production code. Palantir and Salesforce alumni. Post on FDE Pulse to reach the FDE-specific audience."},
            {"q": "How do I retain FDE talent?", "a": "FDE turnover drivers: burnout from travel, feeling undervalued compared to product engineers, lack of career progression, and frustration with slow product feedback loops. Address each: offer travel flexibility and recovery time between deployments, pay at or above SWE equivalents, create a clear FDE career ladder, and build formal channels for FDE insights to influence the product roadmap. Companies that treat FDEs as first-class engineers (not support staff) retain them longest."},
            {"q": "What's the ROI of an FDE team?", "a": "FDE teams typically improve three metrics: customer time-to-value (30-50% faster deployment), net revenue retention (5-15% improvement from reduced churn and expansion), and product-market fit (FDE feedback accelerates product improvements). A single FDE generating $500K-$2M in retained/expanded revenue per year at a cost of $250K-$400K total comp provides strong ROI. Track customer health metrics before and after FDE engagement to measure impact."},
        ],
    },
    {
        "slug": "forward-deployed-engineer-tech-stack", "dir": "insights",
        "title": "FDE Tech Stack & Tools (2026)",
        "meta_desc": "The most in-demand FDE tools and technologies in 2026. Python, SQL, LLM frameworks, cloud platforms, and the tools FDE teams actually use.",
        "content": """<p style="margin-bottom: 1.25rem;">FDE Pulse analyzes job descriptions to track which technologies and tools appear most frequently in Forward Deployed Engineer postings. Here's the definitive 2026 tech stack guide for FDE candidates and hiring managers.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Programming Languages</h2>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">Python (78% of postings)</strong>. The dominant FDE language. Used for data pipelines, API integrations, ML/AI deployment, scripting, and backend services. Python's ecosystem (pandas, FastAPI, SQLAlchemy, LangChain) maps directly to FDE work. If you learn one language for FDE, learn Python deeply.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">SQL (65%)</strong>. Essential for every FDE role. Customer data lives in databases. FDEs write queries, design schemas, optimize performance, and build data pipelines. Strong SQL skills (window functions, CTEs, query optimization, schema design) separate effective FDEs from those who struggle with customer data.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">TypeScript/JavaScript (52%)</strong>. Required for full-stack FDE work: building customer-facing dashboards, API endpoints, integration services. TypeScript is preferred over JavaScript for production FDE code because type safety catches integration errors earlier.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">Go (15%)</strong>. Growing in FDE postings, particularly at infrastructure-heavy companies (Databricks, cloud providers). Go's concurrency model and performance make it valuable for data pipeline and system integration work.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-muted);">Other languages (5-10% each):</strong> Java (ServiceNow, enterprise), Rust (Anduril, performance-critical), C++ (Anduril, embedded systems), Ruby (legacy integrations).</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">AI/ML Tools (Growing Fastest)</h2>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">LLM APIs (45% of AI-company postings)</strong>. OpenAI API, Anthropic Claude SDK, Cohere SDK, Google Vertex AI. The ability to integrate, configure, and optimize LLM API calls is the fastest-growing FDE skill.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">RAG Frameworks (35%)</strong>. LangChain, LlamaIndex, Haystack. Building retrieval-augmented generation systems is the most common AI FDE task. These frameworks provide the scaffolding for connecting LLMs to customer-specific data sources.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">Vector Databases (30%)</strong>. Pinecone, Weaviate, Qdrant, Chroma, pgvector. Essential infrastructure for RAG systems. FDEs need to understand embedding models, similarity search, and vector index optimization.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">ML Platforms (25%)</strong>. MLflow, Weights & Biases, Databricks ML, SageMaker. For FDEs deploying ML models beyond LLMs: model training, experiment tracking, model serving, and monitoring.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">Model Serving (20%)</strong>. vLLM, TensorRT, NVIDIA Triton, BentoML. For on-premise and performance-critical AI deployments. Cohere and Databricks FDE roles particularly value model serving expertise.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Data Engineering Tools</h2>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">Apache Spark (38%)</strong>. The standard for distributed data processing. Required for Databricks FDE roles. Valuable for any FDE working with large-scale customer data.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">dbt (25%)</strong>. Data transformation and modeling. Growing in FDE postings as companies adopt modern data stack approaches. Valuable for FDEs building analytical data pipelines.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">Apache Airflow (22%)</strong>. Workflow orchestration. FDEs build data pipelines that run on schedules or triggers. Airflow is the most common orchestration tool in FDE job descriptions.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">Kafka (18%)</strong>. Stream processing and event-driven architectures. Valuable for FDEs deploying real-time data pipelines at customer sites.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Cloud & Infrastructure</h2>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">AWS (42%)</strong>. The most common cloud platform in FDE job descriptions. Key services: Lambda, ECS, S3, RDS, SageMaker, Bedrock.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">GCP (28%)</strong>. Google Cloud Platform. Key services: Vertex AI, BigQuery, Cloud Run, GKE. Preferred by AI-focused companies.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">Azure (20%)</strong>. Growing in FDE postings as enterprise customers on Microsoft stacks adopt AI. Key services: Azure OpenAI, Cognitive Services, AKS.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">Docker/Kubernetes (32%)</strong>. Container orchestration is essential for deploying services at customer sites. FDEs need to package applications, manage deployments, and troubleshoot container issues in customer environments.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">Terraform (18%)</strong>. Infrastructure as code. Valuable for FDEs who provision customer infrastructure as part of deployments. Increasingly important as FDE work involves cloud infrastructure setup alongside application deployment.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Integration & API Tools</h2>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">REST APIs (48%)</strong>. The universal integration standard. Every FDE builds and consumes REST APIs. Deep understanding of authentication (OAuth, API keys), pagination, rate limiting, and error handling is essential.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">GraphQL (15%)</strong>. Growing in FDE postings, especially at companies with complex data models. Provides more efficient data fetching for customer-facing applications.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">FastAPI (20%)</strong>. The preferred Python web framework for FDE work. Lightweight, fast, and type-safe. FDEs build custom API endpoints, webhook handlers, and microservices with FastAPI.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--amber-light);">Webhooks/Event-Driven (22%)</strong>. Many customer integrations are event-driven: receiving webhooks from customer systems, processing events, and triggering downstream actions. FDEs need to design reliable webhook handlers with retry logic and error recovery.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">What to Learn First</h2>

<p style="margin-bottom: 1.25rem;">If you're preparing for FDE roles, prioritize in this order:</p>

<ol style="margin-bottom: 1.25rem; padding-left: 1.5rem;">
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Python + SQL</strong>. non-negotiable foundation for all FDE roles</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">REST API design + integration patterns</strong>. the core FDE skill</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Docker + one cloud platform (AWS or GCP)</strong>. deployment fundamentals</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">LLM APIs + RAG architecture</strong>. if targeting AI companies</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">TypeScript</strong>. for full-stack FDE work</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Data pipeline tools (Airflow, Spark, dbt)</strong>. for data-heavy FDE roles</li>
</ol>""",
        "faq": [
            {"q": "What's the most important technology for FDE roles?", "a": "Python. It appears in 78% of FDE job descriptions and is used for the widest range of FDE tasks: data pipelines, API integrations, ML deployment, scripting, and backend services. If you're strong in Python, you're qualified for most FDE roles. SQL is a close second at 65%."},
            {"q": "Do FDEs need to know Kubernetes?", "a": "It depends on the company. 32% of FDE postings mention Docker/Kubernetes. If you're targeting infrastructure-heavy roles (Databricks, cloud providers, Anduril), Kubernetes is important. For application-focused FDE roles (OpenAI, Ramp, Rippling), Docker knowledge is sufficient. Kubernetes is a 'nice to have' not a 'must have' for most FDE positions."},
            {"q": "Should I learn LangChain for FDE interviews?", "a": "If you're targeting AI companies, yes. LangChain (or LlamaIndex) is the most common RAG framework in FDE job descriptions. Building a project with LangChain demonstrates practical AI deployment skills. However, the underlying concepts (embedding models, vector search, retrieval strategies) matter more than framework-specific knowledge. Frameworks change; concepts persist."},
            {"q": "Is the FDE tech stack different from SWE tech stack?", "a": "The languages overlap (Python, TypeScript, SQL) but the tools diverge. FDEs use more integration tools (API clients, webhook handlers, data migration tools) and less product development tools (React, mobile frameworks, CI/CD pipelines). FDEs also use more AI/ML tools than typical SWEs. The biggest FDE-specific skill is API integration design. connecting systems that don't natively talk to each other."},
            {"q": "How quickly does the FDE tech stack change?", "a": "The core stack (Python, SQL, REST APIs, Docker) is stable and has been for years. The AI layer changes fast: LLM frameworks, vector databases, and model serving tools evolve monthly. The strategic approach: invest deeply in stable fundamentals (Python, SQL, API design) and stay current on AI tools without over-investing in any single framework. The ability to learn new tools quickly matters more than knowing today's specific tools."},
        ],
    },
]


def generate_topical_pages():
    print("  Generating topical pages...")
    count = 0
    for page in PAGES:
        related = get_related_links([
            {"href": "/companies/", "label": "Companies Hiring FDEs"},
            {"href": "/salaries/", "label": "FDE Salary Data"},
            {"href": "/career/how-to-become-a-forward-deployed-engineer/", "label": "How to Become an FDE"},
            {"href": "/jobs/", "label": "Browse FDE Jobs"},
        ])
        faq_html = ""
        faq_items = []
        for faq in page["faq"]:
            faq_html += '<div style="margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border);"><h3 style="font-size: 1.15rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">%s</h3><p style="color: var(--text-secondary); line-height: 1.7;">%s</p></div>' % (faq["q"], faq["a"])
            faq_items.append({"@type": "Question", "name": faq["q"], "acceptedAnswer": {"@type": "Answer", "text": faq["a"]}})

        body = '''
        <section class="section" style="max-width: 900px; margin: 0 auto; padding-top: 8rem;">
            <h1 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">%s</h1>
            <div style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 1.5rem;">By <a href="https://www.linkedin.com/in/romethorndike/" target="_blank" rel="noopener" style="color: var(--amber); text-decoration: none;">Rome Thorndike</a></div>
            <div style="color: var(--text-secondary); font-size: 1.05rem; line-height: 1.8;">
                %s
                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Frequently Asked Questions</h2>
                %s
            </div>
            %s

            %s
        </section>
''' % (page["title"], page["content"], faq_html, related, get_cta_box())

        canon = "/" + page["dir"] + "/" + page["slug"] + "/"
        faq_schema = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_items}, indent=2)
        breadcrumb = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": page["dir"].title(), "item": BASE_URL + "/" + page["dir"] + "/"},
            {"@type": "ListItem", "position": 3, "name": page["title"].split(":")[0], "item": BASE_URL + canon}
        ]}, indent=2)
        article = get_article_schema(page["title"], page["meta_desc"], canon, "2026-04-10")
        extra_head = '<script type="application/ld+json">\n' + faq_schema + '\n    </script>\n    <script type="application/ld+json">\n' + breadcrumb + '\n    </script>\n    ' + article

        html = get_html_head(title=page["title"], description=page["meta_desc"], canonical_path=canon, extra_head=extra_head)
        html += "\n<body>\n" + get_header_html() + "\n    <main>\n" + body + "\n    </main>\n" + get_footer_html() + get_mobile_nav_js() + get_signup_js() + "\n</body>\n</html>"

        out_dir = os.path.join(SITE_DIR, page["dir"], page["slug"])
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        count += 1
    print("  " + str(count) + " topical pages generated")

if __name__ == "__main__":
    generate_topical_pages()
