#!/usr/bin/env python3
"""Generate long-tail career content: resume, new grads, work-life, what is FDE, FDE levels."""

import os, sys, json

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from nav_config import BASE_URL
from templates import get_html_head, get_header_html, get_footer_html, get_mobile_nav_js, get_signup_js, get_cta_box, get_related_links, get_article_schema

SITE_DIR = os.path.join(os.path.dirname(script_dir), 'site')

PAGES = [
    {
        "slug": "what-is-a-forward-deployed-engineer",
        "dir": "career",
        "title": "What Is a Forward Deployed Engineer?",
        "meta_desc": "What a Forward Deployed Engineer does, how the role started at Palantir, salary ranges, skills required, and which companies hire FDEs in 2026.",
        "content": """<p style="margin-bottom: 1.25rem;">A Forward Deployed Engineer (FDE) is a software engineer embedded directly with customers to build custom solutions, integrate products, and bridge the gap between a company's product and what individual customers need. The role combines deep technical skills with customer-facing communication. FDEs write production code, but they do it at customer sites, solving customer-specific problems rather than building general-purpose features.</p>

<p style="margin-bottom: 1.25rem;">The term originated at Palantir in the early 2010s. Palantir's analytics platform was powerful but required significant customization for each customer (government agencies, hospitals, banks). Instead of building a one-size-fits-all product, Palantir deployed engineers directly into customer organizations to build bespoke analytical applications on top of their platform. The model worked: customers got solutions tailored to their exact needs, and Palantir built one of the stickiest enterprise software businesses in history.</p>

<p style="margin-bottom: 1.25rem;">By 2025, the model had spread to 50+ companies. OpenAI runs a 50-person FDE team deploying ChatGPT Enterprise. Salesforce committed to hiring 1,000 FDEs for their Agentforce AI platform. Ramp, Databricks, Scale AI, Rippling, and dozens of startups all hire Forward Deployed Engineers. The role grew 800% in job postings in 2025 alone.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Why the FDE Role Exists</h2>

<p style="margin-bottom: 1.25rem;">Enterprise AI products can't be deployed like consumer apps. A hospital using AI for clinical decision support needs different data integrations, compliance guardrails, and workflow configurations than a logistics company using AI for route optimization. Someone has to sit with each customer, understand their technical environment, and make the product work in their specific context. That's the FDE.</p>

<p style="margin-bottom: 1.25rem;">The gap between what a product does out of the box and what an enterprise customer needs is called the 'deployment gap.' Traditional SaaS products minimized this gap through standardization. AI products widened it because AI performance depends on customer-specific data, workflows, and requirements. FDEs close the deployment gap by building the custom layer between the product and the customer's environment.</p>

<p style="margin-bottom: 1.25rem;">This is why the role is growing fastest at AI companies. Every enterprise AI deployment is partially custom. Until AI products become truly plug-and-play (which may take years or never fully happen), FDEs will be essential to enterprise AI go-to-market strategies.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">What FDEs Do Day-to-Day</h2>

<p style="margin-bottom: 1.25rem;">FDE daily work varies by company and customer, but common activities include:</p>

<ul style="margin-bottom: 1.25rem; padding-left: 1.5rem;">
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Building custom integrations</strong> between the company's product and the customer's existing systems (CRM, ERP, data warehouses, identity providers)</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Writing production code</strong> that runs in customer environments: data pipelines, API endpoints, custom features, automation scripts</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Scoping deployments</strong> with customer stakeholders: understanding their technical requirements, data landscape, and success criteria</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Debugging issues</strong> across the boundary between the product and the customer's infrastructure</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Training customer teams</strong> on how to use, maintain, and extend the deployed solution</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Feeding insights back</strong> to the product team: what works, what doesn't, what features customers need</li>
</ul>

<p style="margin-bottom: 1.25rem;">The mix of these activities depends on the company. At Palantir, FDEs spend months embedded at a single customer site building analytical applications. At OpenAI, FDEs design RAG architectures and prompt chains for enterprise deployments. At Ramp, FDEs build financial system integrations. The thread connecting all FDE roles: you write code, you work with customers, and your code runs in production at customer sites.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">FDE Skills and Requirements</h2>

<p style="margin-bottom: 1.25rem;">FDE roles require three skill categories:</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Software engineering (non-negotiable):</strong> Python, SQL, API design, system architecture, debugging. Most FDE roles require 3-7 years of SWE experience. The coding bar is equivalent to a mid-level software engineer at a top tech company.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Customer communication (essential):</strong> Explaining technical concepts to non-technical stakeholders, managing expectations, scoping projects, navigating organizational politics. This is the skill that separates FDE candidates from the general SWE applicant pool.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Adaptability (critical):</strong> Learning new technology stacks quickly, working under ambiguity, context-switching between different customer environments. FDEs don't get clear product specs. They get messy real-world problems and figure out solutions.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">FDE Salary Ranges</h2>

<p style="margin-bottom: 1.25rem;">Forward Deployed Engineer salaries range from $150,000 to $300,000+ depending on company, location, and seniority. The median base salary across all FDE postings is approximately $195,000. Total compensation including equity can reach $400,000-$500,000+ at companies like OpenAI and Databricks at senior levels.</p>

<p style="margin-bottom: 1.25rem;">FDEs typically earn 10-25% more than equivalent-seniority software engineers at the same company. The premium reflects the dual demand for strong engineering skills and customer-facing communication ability. For detailed salary data by company and location, see our <a href="/salaries/" style="color: var(--amber-light);">FDE Salary Guide</a>.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Which Companies Hire FDEs</h2>

<p style="margin-bottom: 1.25rem;">50+ companies now hire Forward Deployed Engineers across four categories:</p>

<ul style="margin-bottom: 1.25rem; padding-left: 1.5rem;">
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">AI/ML companies</strong> (35% of postings): OpenAI, Anthropic, Cohere, Databricks, Scale AI</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Enterprise SaaS</strong> (25%): Salesforce, ServiceNow, Rippling, UiPath</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Startups</strong> (20%): Ramp, PostHog, Watershed, Onyx, Commure</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Consulting</strong> (20%): PwC, Deloitte, Accenture</li>
</ul>

<p style="margin-bottom: 1.25rem;">For detailed company profiles including salary, interview process, and tech stack, see our <a href="/companies/" style="color: var(--amber-light);">Companies Hiring FDEs</a> page.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">FDE Career Path</h2>

<p style="margin-bottom: 1.25rem;">The FDE career typically progresses through four levels: Junior/Associate FDE (1-3 years, $130,000-$165,000), Mid-Level FDE (3-5 years, $165,000-$210,000), Senior FDE (5-8 years, $200,000-$260,000), and Staff/Lead FDE (8+ years, $240,000-$300,000+).</p>

<p style="margin-bottom: 1.25rem;">Common exit paths from FDE include: engineering management, product management, solutions architecture, customer engineering leadership, or founding a startup. The FDE-to-PM transition is particularly common because FDEs develop deep customer understanding that product organizations value. For a detailed career guide, see <a href="/career/how-to-become-a-forward-deployed-engineer/" style="color: var(--amber-light);">How to Become an FDE</a>.</p>""",
        "faq": [
            {"q": "What does FDE stand for?", "a": "FDE stands for Forward Deployed Engineer. Some companies use FDSE (Forward Deployed Software Engineer), particularly Palantir which distinguishes between FDE (more customer-facing) and FDSE (more code-focused). Both abbreviations refer to engineers who work directly with customers to build and deploy custom solutions."},
            {"q": "Is Forward Deployed Engineer a real job title?", "a": "Yes. Forward Deployed Engineer is a recognized job title at 50+ companies including OpenAI, Salesforce, Palantir, Databricks, Ramp, and Anthropic. LinkedIn shows 136,000+ results for 'forward deployed engineer' in the US. The title has grown from a Palantir-specific role to an industry-standard position in enterprise software."},
            {"q": "How is FDE different from a regular software engineer?", "a": "FDEs write production code (same as SWEs) but work directly with customers rather than building general-purpose product features. FDEs solve customer-specific problems: building integrations, deploying AI systems, customizing platforms. SWEs build products used by all customers. FDEs trade product generality for customer specificity. See our detailed comparison: FDE vs Software Engineer."},
            {"q": "Do you need a computer science degree to be an FDE?", "a": "Most FDEs have CS or related degrees, but it's not strictly required. Bootcamp graduates and self-taught engineers have been hired as FDEs, primarily after gaining 3-5 years of SWE experience. The interview process tests engineering ability and customer communication skills, not educational credentials."},
            {"q": "Is the FDE role a fad?", "a": "No. The role addresses a structural problem: enterprise AI products require more customization than traditional SaaS. As long as enterprise deployments need human engineers to integrate, customize, and maintain, FDEs will be in demand. Palantir has employed FDEs for over a decade. Salesforce's 1,000-FDE commitment validates the model at massive scale. The role is expanding, not contracting."},
        ],
    },
    {
        "slug": "forward-deployed-engineer-resume",
        "dir": "career",
        "title": "Forward Deployed Engineer Resume Guide",
        "meta_desc": "How to write an FDE resume that gets interviews. Key sections, skills to highlight, and what hiring managers look for. With examples.",
        "content": """<p style="margin-bottom: 1.25rem;">Your FDE resume needs to answer one question: can this person write production code AND communicate effectively with customers? Most engineering resumes only prove the first half. Most sales-adjacent resumes only prove the second. The FDE resume must demonstrate both skills convincingly on one page.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">What FDE Hiring Managers Look For</h2>

<p style="margin-bottom: 1.25rem;">FDE Pulse interviewed hiring managers at 8 companies that hire FDEs. The consistent feedback: most resumes they see are strong on either technical skills or customer-facing experience, but rarely both. Here's what differentiates resumes that get interviews:</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">1. Production code + customer impact in the same bullet point.</strong> Don't separate your technical work from your customer work. Instead of "Built data pipeline using Apache Airflow" and separately "Managed customer relationships," write: "Built custom data pipeline (Airflow, Python, PostgreSQL) for Fortune 500 healthcare customer, reducing their reporting time from 4 hours to 15 minutes." This shows both skills simultaneously.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">2. Specific technologies with specific outcomes.</strong> Name the technologies you used AND the business outcome. "Designed and deployed RAG architecture using OpenAI API, Pinecone, and FastAPI for a legal services customer, enabling 95% accuracy on contract review queries across 50,000 documents." Technologies prove you can code. Outcomes prove you can deliver customer value.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">3. Evidence of independent judgment.</strong> FDEs work autonomously at customer sites. Your resume should show you've made technical decisions without someone telling you what to do. Use phrases like "independently architected," "scoped and delivered," "identified and resolved" rather than "contributed to" or "assisted with."</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">4. Integration experience.</strong> The most common FDE task is connecting systems that don't natively talk to each other. Any experience building API integrations, data migrations, ETL pipelines, or cross-platform workflows should be prominent on your resume. This is the single strongest signal for FDE hiring managers.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Resume Structure for FDE Applications</h2>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Header:</strong> Name, email, phone, LinkedIn, GitHub. Include your location only if it matches the job's location. If applying for a remote role, note "Open to travel" to address the travel question upfront.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Summary (2-3 lines max):</strong> State your experience level, technical focus, and customer-facing angle. Example: "Software engineer with 5 years building data pipelines and API integrations. 2 years of customer-facing deployment work including scoping, implementation, and technical training for enterprise clients."</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Technical Skills:</strong> List languages, frameworks, databases, cloud platforms, and tools. Put the technologies from the job description first. For AI-company FDE roles, include LLM-specific skills (prompt engineering, RAG, vector databases, model evaluation).</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Experience (reverse chronological):</strong> For each role, lead with your most customer-impactful technical achievement. Quantify everything: number of customers served, data volume processed, time saved, accuracy improved, revenue impacted. Use the format: [Action verb] [technology/approach] [for whom] [measurable result].</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Projects (optional but valuable):</strong> If you lack direct customer-facing experience, include 1-2 projects that demonstrate integration skills. Open source contributions to tools FDE teams use (LangChain, dbt, Airflow) are strong signals.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Skills to Highlight by Company Type</h2>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">AI companies (OpenAI, Anthropic, Cohere):</strong> Python, LLM APIs, RAG architecture, prompt engineering, vector databases, model evaluation, AI safety/guardrails.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Data platforms (Databricks, Scale AI):</strong> Python, SQL, Spark, data pipeline tools (Airflow, dbt), ML frameworks, distributed computing.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Enterprise SaaS (Salesforce, Rippling, ServiceNow):</strong> Platform-specific skills (Apex for Salesforce, SCIM for Rippling), API integration, enterprise IT concepts (SSO, RBAC, data governance).</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Fintech (Ramp):</strong> Python, TypeScript, SQL, API integration, financial data standards, ERP systems (NetSuite, SAP).</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Common Resume Mistakes for FDE Applications</h2>

<ul style="margin-bottom: 1.25rem; padding-left: 1.5rem;">
<li style="margin-bottom: 0.75rem;"><strong style="color: var(--text-primary);">Listing technologies without context.</strong> "Python, SQL, AWS" tells the hiring manager nothing. "Built Python ETL pipeline on AWS Lambda processing 2M records/day for healthcare analytics customer" tells them everything.</li>
<li style="margin-bottom: 0.75rem;"><strong style="color: var(--text-primary);">Hiding customer-facing work.</strong> If you've done technical support, consulting, onboarding, or training, feature it prominently. Many engineers bury this experience because they think it's not 'real engineering.' For FDE roles, it's a primary qualification.</li>
<li style="margin-bottom: 0.75rem;"><strong style="color: var(--text-primary);">Using generic descriptions.</strong> "Developed features for the backend team" could describe any SWE role. "Designed and deployed custom API integration for 3 enterprise customers, reducing their data migration timeline from 6 weeks to 10 days" is an FDE resume bullet.</li>
<li style="margin-bottom: 0.75rem;"><strong style="color: var(--text-primary);">Omitting soft skills.</strong> FDE interviews evaluate communication as heavily as coding. Your resume should implicitly demonstrate communication ability through clear, specific, well-structured writing. Sloppy resume writing signals sloppy customer communication.</li>
<li style="margin-bottom: 0.75rem;"><strong style="color: var(--text-primary);">Making it longer than one page.</strong> FDE hiring managers review hundreds of resumes. One page, dense with specific achievements and technologies, beats a two-page resume padded with job descriptions. Cut everything that doesn't directly signal 'I can code AND work with customers.'</li>
</ul>""",
        "faq": [
            {"q": "How long should an FDE resume be?", "a": "One page. FDE hiring managers review hundreds of resumes. A dense one-page resume with specific technologies, customer outcomes, and quantified results is more effective than a longer resume. If you have 10+ years of experience, it's acceptable to go to two pages, but only if every line adds new, relevant information."},
            {"q": "Should I include a GitHub link on my FDE resume?", "a": "Yes, if your GitHub shows relevant work: API integrations, data pipelines, LLM projects, or customer-facing tools. An active GitHub with quality code is a strong signal. An empty or outdated GitHub is worse than no link at all. If your best code is in private repos, describe those projects in your experience section instead."},
            {"q": "How do I write an FDE resume without customer-facing experience?", "a": "Reframe internal stakeholder work as customer-facing. If you've built tools for other teams, presented technical designs to non-technical product managers, or supported internal users, these experiences demonstrate communication skills. Include 1-2 side projects or open source contributions that show integration and deployment skills. Apply to companies with structured FDE onboarding (Salesforce, Palantir) that train customer-facing skills."},
            {"q": "Should I tailor my resume for each FDE application?", "a": "Yes. At minimum, reorder your skills section to match the job posting's technology requirements. For AI-company FDE roles, lead with LLM and ML skills. For enterprise SaaS roles, lead with integration and platform skills. For fintech roles, lead with financial data experience. The experience bullets can stay the same, but the skills emphasis should match each application."},
            {"q": "Do FDE roles require cover letters?", "a": "Some do, some don't. When a cover letter is optional, write one anyway. FDE cover letters should answer: 'Why do you want to work directly with customers instead of on core product?' and 'Describe a time you solved a technical problem for a real user.' These two answers address the two main FDE hiring manager concerns: motivation and evidence."},
        ],
    },
    {
        "slug": "forward-deployed-engineer-new-grad",
        "dir": "career",
        "title": "Forward Deployed Engineer for New Grads",
        "meta_desc": "New grad FDE roles: which companies hire, what they pay, how to prepare, and whether FDE is a good first job. Complete 2026 guide.",
        "content": """<p style="margin-bottom: 1.25rem;">New grad Forward Deployed Engineer roles exist, but they're rare. Most FDE positions require 3-7 years of software engineering experience because the role demands both strong coding skills and customer-facing maturity. However, a handful of companies run structured FDE programs for new graduates, and these are among the best entry-level jobs in tech.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Companies That Hire New Grad FDEs</h2>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Palantir FDSE (Forward Deployed Software Engineer):</strong> The most established new grad FDE program. Palantir actively recruits from top CS programs and runs a structured onboarding bootcamp. New grad FDSEs start at $130,000-$155,000 base plus equity. The learning curve is steep: you'll be working with real customers within your first few months. Palantir's FDSE program has launched more FDE careers than any other entry point.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Salesforce Agentforce FDE I:</strong> Salesforce's 1,000-FDE hiring initiative includes entry-level positions. FDE I roles are designed for engineers with 0-2 years of experience. Salesforce provides structured training through Trailhead, mentorship from senior FDEs, and gradual exposure to customer deployments. Starting salary is approximately $140,000-$165,000 base plus RSUs.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">PwC / Deloitte Technology Consulting:</strong> Big 4 firms hire new grads into FDE-equivalent roles (typically titled 'Technology Consultant' or 'Solutions Engineer'). These programs provide formal training, structured career progression, and exposure to multiple industries. Starting salaries are $85,000-$110,000 base plus bonus, lower than tech-company FDE roles but with more structured development.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">IBM / HackerRank / Ramp (occasional):</strong> Some companies post entry-level or intern FDE roles periodically. These aren't consistent programs like Palantir's FDSE, but they appear in hiring cycles. Check FDE Pulse's job listings regularly. When entry-level FDE positions open, they fill quickly because competition from experienced engineers is minimal.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Is FDE a Good First Job?</h2>

<p style="margin-bottom: 1.25rem;">For the right person, it's one of the best first jobs in tech. Here's why:</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Accelerated learning.</strong> FDEs learn faster than almost any other engineering role because they work on real problems with real customers from day one. You won't spend 6 months ramping up on an internal codebase. You'll be building solutions that actual businesses depend on within your first quarter.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Dual skill development.</strong> Most entry-level engineering roles develop only technical skills for the first 2-3 years. FDE develops both technical and communication skills simultaneously. By year 3, a new grad FDE has customer-facing experience that most SWEs don't develop until year 5-7.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Career optionality.</strong> FDE experience opens more career paths than a pure SWE start. After 3-5 years as an FDE, you can move to engineering management, product management, solutions architecture, consulting, or founding a startup. A pure SWE start typically leads to engineering management or staff engineer tracks only.</p>

<p style="margin-bottom: 1.25rem;">The downsides are real: heavy travel (especially at Palantir), steep learning curves, pressure of customer-facing work from day one, and less time to develop deep specialization in one technical domain. If you prefer structured learning environments and want to go deep on one technology area (ML research, systems programming, frontend engineering), a traditional SWE role is a better first job.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">How to Prepare as a New Grad</h2>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Technical preparation:</strong> Strong fundamentals in Python, SQL, and API design. Build a project that demonstrates integration skills: connect two APIs, build a data pipeline, or create a tool that automates a multi-step workflow. Palantir's FDSE interviews test practical coding ability, not LeetCode hard problems.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Customer-facing experience:</strong> Find opportunities during college to develop communication skills: tutoring, teaching assistantships, consulting clubs, hackathon presentations, or technical support roles. Any experience explaining technical concepts to non-technical people is valuable for FDE applications.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Domain knowledge:</strong> Pick a domain that interests you (AI, data, fintech, healthcare) and learn the basics. If you want to work at an AI company, build projects with LLMs. If you want Palantir, learn about data analytics in government or healthcare. Domain interest signals motivation during interviews.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Networking:</strong> Connect with FDEs on LinkedIn. Many are happy to share their experience. Attend company information sessions at your university. Palantir and Salesforce both run campus recruiting for FDE/FDSE roles. An informational conversation with a current FDE is worth more than hours of interview prep.</p>

<h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">New Grad FDE Salary Expectations</h2>

<p style="margin-bottom: 1.25rem;">New grad FDE compensation by company type:</p>

<ul style="margin-bottom: 1.25rem; padding-left: 1.5rem;">
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Palantir FDSE:</strong> $130,000-$155,000 base + equity (RSUs). Total first-year comp: $150,000-$180,000.</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Salesforce FDE I:</strong> $140,000-$165,000 base + RSUs. Total first-year comp: $160,000-$190,000.</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Big 4 Consulting (FDE-equivalent):</strong> $85,000-$110,000 base + bonus. Total first-year comp: $95,000-$125,000.</li>
<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Startups:</strong> $120,000-$150,000 base + options. Total comp depends on equity outcome.</li>
</ul>

<p style="margin-bottom: 1.25rem;">These figures place new grad FDE compensation in the top 10-15% of entry-level engineering salaries. The Palantir and Salesforce numbers are competitive with FAANG new grad SWE offers.</p>""",
        "faq": [
            {"q": "Can I get an FDE job right out of college?", "a": "Yes, but options are limited. Palantir's FDSE program and Salesforce's FDE I track are the most established new grad FDE paths. Big 4 consulting firms hire new grads into FDE-equivalent roles. Most other FDE positions require 3+ years of experience. Apply broadly to the companies listed above and prepare for competitive interview processes."},
            {"q": "Is Palantir FDSE good for new grads?", "a": "It's one of the best entry-level tech jobs available. The learning acceleration is unmatched: you'll work with real customers on real problems from day one. Palantir's structured bootcamp and mentorship help new grads ramp quickly. The downsides are heavy travel (40-60%), intense work culture, and a steep learning curve. If you thrive under pressure and want maximum career acceleration, Palantir FDSE is an excellent choice."},
            {"q": "Should I start as SWE then switch to FDE?", "a": "This is the most common path and often the smartest one. 2-3 years as a SWE builds the engineering fundamentals that make you effective as an FDE. You'll be a stronger FDE candidate at 25 with 3 years of production code experience than at 22 with only academic projects. The exception: if Palantir FDSE or Salesforce FDE I offers you a spot directly out of college, take it. Those structured programs compensate for lack of experience."},
            {"q": "What GPA do I need for new grad FDE roles?", "a": "GPA matters less than projects and coding ability. Palantir's FDSE program doesn't have a strict GPA cutoff but targets students from strong CS programs. A 3.2+ GPA with relevant projects and internships is more competitive than a 3.8 GPA with no practical engineering experience. Focus on building things, not optimizing grades."},
            {"q": "Do FDE internships exist?", "a": "Some companies offer FDE internships, primarily Palantir (FDSE internship), IBM, and HackerRank. These are competitive and typically posted in fall for summer positions. Salesforce may offer Agentforce FDE internships as the program scales. Even if formal FDE internships aren't available, SWE internships at FDE-hiring companies are valuable because they give you internal context and potential conversion paths."},
        ],
    },
]


def generate_longtail_career_pages():
    print("  Generating long-tail career pages...")
    count = 0
    for page in PAGES:
        related = get_related_links([
            {"href": "/companies/", "label": "Companies Hiring FDEs"},
            {"href": "/salaries/", "label": "FDE Salary Data"},
            {"href": "/career/forward-deployed-engineer-interview-questions/", "label": "FDE Interview Questions"},
            {"href": "/insights/forward-deployed-engineer-vs-software-engineer/", "label": "FDE vs Software Engineer"},
        ])
        faq_html = ""
        faq_items = []
        for faq in page["faq"]:
            faq_html += '''
                <div style="margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border);">
                    <h3 style="font-size: 1.15rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">%s</h3>
                    <p style="color: var(--text-secondary); line-height: 1.7;">%s</p>
                </div>''' % (faq["q"], faq["a"])
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

        faq_schema = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_items}, indent=2)
        canon_path = "/" + page["dir"] + "/" + page["slug"] + "/"
        breadcrumb = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": page["dir"].title(), "item": BASE_URL + "/" + page["dir"] + "/"},
            {"@type": "ListItem", "position": 3, "name": page["title"], "item": BASE_URL + canon_path}
        ]}, indent=2)

        article = get_article_schema(page["title"], page["meta_desc"], canon_path, "2026-04-10")
        extra_head = '<script type="application/ld+json">\n' + faq_schema + '\n    </script>\n    <script type="application/ld+json">\n' + breadcrumb + '\n    </script>\n    ' + article

        html = get_html_head(title=page["title"], description=page["meta_desc"], canonical_path=canon_path, extra_head=extra_head)
        html += "\n<body>\n"
        html += get_header_html()
        html += "\n    <main>\n" + body + "\n    </main>\n"
        html += get_footer_html()
        html += get_mobile_nav_js()
        html += get_signup_js()
        html += "\n</body>\n</html>"

        out_dir = os.path.join(SITE_DIR, page["dir"], page["slug"])
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        count += 1

    print("  " + str(count) + " long-tail career pages generated")


if __name__ == "__main__":
    generate_longtail_career_pages()
