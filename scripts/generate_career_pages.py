#!/usr/bin/env python3
"""
Generate career guide pages for FDE Pulse.
Hub+spoke content targeting career/interview/resume queries.
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

PAGES = [
    {
        "slug": "how-to-become-a-forward-deployed-engineer",
        "title": "How to Become a Forward Deployed Engineer",
        "meta_desc": "Step-by-step guide to landing an FDE role. Required skills, resume tips, where to apply, and what companies look for in FDE candidates.",
        "sections": [
            {"heading": "What Companies Look For in FDE Candidates", "content": """<p style="margin-bottom: 1.25rem;">FDE hiring managers evaluate three things: engineering ability, customer communication skills, and adaptability. You need all three. Strong coding with weak communication gets you a software engineering offer instead. Strong communication with weak coding gets you a solutions engineer offer. The FDE role specifically requires both.</p>

<p style="margin-bottom: 1.25rem;">Engineering ability means you can write production-quality code, design systems that work at scale, and debug complex issues across unfamiliar codebases. Most FDE roles require 3-7 years of software engineering experience. The bar is similar to a mid-level SWE interview at a top tech company.</p>

<p style="margin-bottom: 1.25rem;">Customer communication means you can explain technical concepts to non-technical stakeholders, manage expectations, and navigate organizational politics at customer companies. This is the hardest skill to develop if you've spent your career as a pure backend engineer. The best way to build it is through consulting, technical account management, or developer relations experience.</p>

<p style="margin-bottom: 1.25rem;">Adaptability means you can context-switch between different technology stacks, learn new systems quickly, and deliver results under ambiguity. FDEs don't get clear product specs. They get a customer with a problem and a product that partially solves it. The FDE figures out the rest.</p>"""},
            {"heading": "Required Technical Skills", "content": """<p style="margin-bottom: 1.25rem;">Based on FDE Pulse analysis of 150+ job postings, the most requested skills are:</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Must-have (80%+ of postings):</strong> Python, SQL, REST API design, Git. These appear in virtually every FDE job description. If you're missing any of these, start here.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Strongly preferred (50-70%):</strong> TypeScript/JavaScript, cloud platforms (AWS/GCP/Azure), Docker/Kubernetes, data pipeline tools (Airflow, dbt, Spark). These differentiate competitive candidates from baseline-qualified ones.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Growing fast (30-50%):</strong> LLM integration (prompt engineering, RAG, fine-tuning), ML/AI deployment, system design at scale. This cluster didn't exist in FDE postings a year ago. AI-company FDE roles now require it.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Nice-to-have (20-30%):</strong> Terraform/IaC, GraphQL, streaming systems (Kafka), mobile development. These matter for specific companies but aren't universal requirements.</p>"""},
            {"heading": "Step-by-Step Path to Your First FDE Role", "content": """<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Step 1: Build your engineering foundation (0-3 years).</strong> Work as a software engineer for 2-3 years minimum. Focus on full-stack development, API design, and database work. FDE roles rarely hire new grads (Palantir's FDSE program is the main exception). You need demonstrated ability to ship production code independently.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Step 2: Get customer-facing experience.</strong> This is what separates FDE candidates from the SWE applicant pool. Options: volunteer for customer escalations at your current company, do consulting or freelance work on the side, contribute to open source projects where you interact with users, or move into a developer relations or technical account management role for 1-2 years.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Step 3: Learn the product space.</strong> FDEs don't work in a vacuum. They deploy specific products. Pick a domain: AI/ML, data platforms, developer tools, healthcare IT, or fintech. Learn the leading products in that space. Ideally, build projects using them. If you want to be an FDE at Databricks, build something substantial on Databricks first.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Step 4: Optimize your application.</strong> Apply directly through company career pages (not job boards). Tailor your resume to highlight customer-facing engineering work. In your cover letter, describe a time you solved a technical problem for a real user or customer. If you know someone at the company, get a referral. FDE roles have smaller applicant pools than SWE, so referrals carry significant weight.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Step 5: Prepare for the FDE-specific interview rounds.</strong> Most FDE interviews include standard coding rounds plus a customer scenario or case study. You'll be given a hypothetical customer problem and asked to design a technical solution while communicating with a mock customer (played by the interviewer). Practice explaining technical trade-offs in plain English.</p>"""},
            {"heading": "Where to Apply", "content": """<p style="margin-bottom: 1.25rem;">50+ companies now hire FDEs. The best entry points depend on your experience level:</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">New to FDE (3-5 years SWE experience):</strong> Salesforce Agentforce (structured program, mentorship), Palantir (dedicated FDSE track for newer engineers), PwC/Deloitte (consulting version with training infrastructure).</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Mid-career (5-8 years):</strong> OpenAI, Databricks, Scale AI, Ramp, Rippling. These companies want autonomous FDEs who can run customer engagements independently. Smaller team sizes mean more impact per person.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Senior/Lead (8+ years):</strong> Companies building FDE teams from scratch. Startups like PostHog, Watershed, Onyx, and Commure are hiring first or second FDEs. You'll define the role, build the playbook, and hire your team. Highest risk but highest impact.</p>"""},
        ],
        "faq": [
            {"q": "Do I need a computer science degree to become an FDE?", "a": "Not strictly, but most FDEs have CS or related degrees. Bootcamp graduates have been hired as FDEs, but primarily at smaller companies or after gaining 3-5 years of SWE experience first. The engineering interview bar for FDE is equivalent to mid-level SWE at top tech companies, so you need to pass those coding rounds regardless of educational background."},
            {"q": "Can I become an FDE without customer-facing experience?", "a": "It's possible but harder. Some companies hire pure SWEs into FDE roles and train the customer-facing skills. Palantir's FDSE program and Salesforce's Agentforce team both include customer communication training for new hires. However, candidates with existing customer experience (consulting, technical account management, developer relations) have a significant advantage in FDE interviews."},
            {"q": "How long does it take to become an FDE?", "a": "Most FDEs have 3-7 years of professional experience before their first FDE role. The fastest path is 3 years as a SWE with some customer-facing work, then a direct transition to FDE. The most common path is 4-5 years as a SWE, 1-2 years in a hybrid role (solutions engineering, technical consulting), then FDE. A few companies hire new grads into FDE programs, but these are rare."},
            {"q": "What's the best programming language to learn for FDE roles?", "a": "Python. It appears in 78% of FDE job postings, far ahead of any other language. After Python: SQL (65%), TypeScript/JavaScript (52%), and Go (15%). If you're coming from a Java or C++ background, adding Python proficiency is the single highest-ROI investment for FDE hiring."},
            {"q": "Should I learn AI/ML skills for FDE roles?", "a": "Yes, if you want to work at AI companies. 45% of AI-company FDE postings now request LLM integration experience (prompt engineering, RAG architecture, model evaluation). This number was near zero a year ago. For non-AI companies (Salesforce, Rippling, ServiceNow), traditional software engineering skills are more important than AI/ML. But the market is moving toward AI literacy being expected of all FDEs."},
        ],
    },
    {
        "slug": "forward-deployed-engineer-interview-questions",
        "title": "Forward Deployed Engineer Interview Questions",
        "meta_desc": "50+ real FDE interview questions from OpenAI, Palantir, Salesforce, and more. Coding, system design, and customer scenario prep guide.",
        "sections": [
            {"heading": "FDE Interview Structure", "content": """<p style="margin-bottom: 1.25rem;">FDE interviews typically have 4-6 rounds spread across 1-2 weeks. The structure varies by company but usually includes these components:</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Recruiter Screen (30 min):</strong> Background review, motivation for FDE vs SWE, salary expectations. No technical questions. The recruiter is checking that you understand what FDE means and aren't applying thinking it's a standard SWE role.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Technical Coding (1-2 rounds, 45-60 min each):</strong> Standard LeetCode-style or practical coding problems. Difficulty is typically medium. Companies care more about code quality and communication than algorithmic wizardry. You'll be asked to talk through your approach as you code.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">System Design (1 round, 45-60 min):</strong> Design a system relevant to the company's product. For AI companies: "Design a RAG pipeline for a healthcare customer." For SaaS companies: "Design an integration between our product and Salesforce." The focus is on practical architecture, not theoretical distributed systems.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Customer Scenario / Case Study (1 round, 45-60 min):</strong> This is the FDE-specific round. You're given a hypothetical customer problem and must design a solution while explaining your approach to a mock customer (the interviewer). They're evaluating: Can you translate technical concepts for non-technical stakeholders? Can you ask good clarifying questions? Can you handle pushback gracefully?</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">Behavioral / Values (1 round, 30-45 min):</strong> Stories about past customer interactions, handling ambiguity, working independently, managing conflicting priorities. STAR format works well here.</p>"""},
            {"heading": "Technical Coding Questions", "content": """<p style="margin-bottom: 1.25rem;">Real coding questions reported by FDE candidates (anonymized by company):</p>

<ul style="margin-bottom: 1.25rem; padding-left: 1.5rem;">
<li style="margin-bottom: 0.75rem;">Build a function that takes a customer's CSV data and normalizes it into a standard schema. Handle missing fields, duplicate rows, and inconsistent date formats.</li>
<li style="margin-bottom: 0.75rem;">Write an API endpoint that accepts a webhook from a third-party service, validates the payload, and updates a database. Include error handling and retry logic.</li>
<li style="margin-bottom: 0.75rem;">Given a customer's database schema, write SQL queries to extract the data needed for a dashboard. Optimize for performance on tables with 10M+ rows.</li>
<li style="margin-bottom: 0.75rem;">Build a simple data pipeline that reads from an API, transforms the data, and writes to a database. Handle rate limiting and pagination.</li>
<li style="margin-bottom: 0.75rem;">Implement a caching layer for an API that serves customer-specific data. Define your cache invalidation strategy and explain trade-offs.</li>
<li style="margin-bottom: 0.75rem;">Parse and transform a nested JSON response from a customer's legacy API into the format our product expects. Handle edge cases in the schema.</li>
<li style="margin-bottom: 0.75rem;">Write a script that detects data quality issues in a customer dataset: duplicates, outliers, missing required fields, type mismatches.</li>
<li style="margin-bottom: 0.75rem;">Build a simple CLI tool that automates a multi-step deployment process. Include logging, error recovery, and a dry-run mode.</li>
</ul>"""},
            {"heading": "System Design Questions", "content": """<ul style="margin-bottom: 1.25rem; padding-left: 1.5rem;">
<li style="margin-bottom: 0.75rem;">Design a system that ingests data from 50 different customer sources (APIs, SFTP, databases) and normalizes it into a common schema for analysis.</li>
<li style="margin-bottom: 0.75rem;">A healthcare customer wants to deploy our AI model behind their firewall with no data leaving their network. Design the deployment architecture.</li>
<li style="margin-bottom: 0.75rem;">Design a multi-tenant system where each customer sees only their own data but shares the same infrastructure. How do you handle isolation, performance, and cost?</li>
<li style="margin-bottom: 0.75rem;">A customer wants real-time dashboards from data that currently updates daily. Design a system to move from batch to streaming without breaking existing workflows.</li>
<li style="margin-bottom: 0.75rem;">Design an integration between our product and a customer's existing ERP system (SAP, Oracle, NetSuite). How do you handle schema differences, data sync, and conflict resolution?</li>
</ul>"""},
            {"heading": "Customer Scenario Questions", "content": """<p style="margin-bottom: 1.25rem;">These are the FDE-specific questions that don't appear in standard SWE interviews:</p>

<ul style="margin-bottom: 1.25rem; padding-left: 1.5rem;">
<li style="margin-bottom: 0.75rem;">A customer's CTO is pushing back on your recommended architecture. They want a simpler solution that you believe won't scale. How do you handle this?</li>
<li style="margin-bottom: 0.75rem;">You're two weeks into a customer deployment and discover their data quality is much worse than expected. The timeline hasn't changed. What do you do?</li>
<li style="margin-bottom: 0.75rem;">A customer's engineering team is resistant to adopting your product. They built an internal tool that does 60% of what your product does. How do you approach this?</li>
<li style="margin-bottom: 0.75rem;">You discover a bug in your company's product during a customer deployment. The fix requires a change to the core product that will take 3 weeks. The customer needs a solution this week. What do you do?</li>
<li style="margin-bottom: 0.75rem;">A customer asks you to build a feature that would only benefit them but not other customers. Your product team says no. The customer is a large account. How do you navigate this?</li>
<li style="margin-bottom: 0.75rem;">Walk me through how you would plan the first week of a new customer deployment. What questions do you ask? What do you deliver?</li>
<li style="margin-bottom: 0.75rem;">You're working with a non-technical customer stakeholder who keeps changing requirements. How do you manage scope while maintaining the relationship?</li>
</ul>"""},
            {"heading": "Behavioral Questions", "content": """<ul style="margin-bottom: 1.25rem; padding-left: 1.5rem;">
<li style="margin-bottom: 0.75rem;">Tell me about a time you had to learn a new technology quickly to solve a customer problem.</li>
<li style="margin-bottom: 0.75rem;">Describe a situation where you disagreed with a customer's technical approach. How did you handle it?</li>
<li style="margin-bottom: 0.75rem;">Give an example of when you had to work independently with minimal guidance. What was the outcome?</li>
<li style="margin-bottom: 0.75rem;">Tell me about a project where requirements changed significantly mid-stream. How did you adapt?</li>
<li style="margin-bottom: 0.75rem;">Describe a time you had to explain a complex technical concept to a non-technical audience.</li>
<li style="margin-bottom: 0.75rem;">What's the most complex integration or deployment you've worked on? Walk me through the challenges.</li>
<li style="margin-bottom: 0.75rem;">Tell me about a time you identified a problem before anyone asked you to look at it.</li>
</ul>"""},
            {"heading": "How to Prepare", "content": """<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">For coding rounds:</strong> Practice medium-difficulty LeetCode problems, but spend equal time on practical coding (building APIs, data pipelines, CLI tools). FDE coding rounds skew practical rather than algorithmic. Write clean, readable code with good error handling. Talk through your decisions out loud.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">For system design:</strong> Study the company's product before the interview. Understand what it does, who uses it, and how it's deployed. Your system design should reference their actual product architecture, not generic distributed systems theory. Draw diagrams. Name specific technologies you'd use and explain why.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">For customer scenarios:</strong> Practice with a friend playing the customer role. The most common mistake is jumping to solutions before understanding the problem. Ask clarifying questions. Summarize what you heard. Propose options with trade-offs. Let the "customer" choose. This is a communication test, not a technical test.</p>

<p style="margin-bottom: 1.25rem;"><strong style="color: var(--text-primary);">For behavioral:</strong> Prepare 5-6 stories from your career using STAR format. At least 2 should involve customer or stakeholder interaction. At least 1 should involve a failure or mistake you learned from. FDE interviews value self-awareness and honesty more than polished success stories.</p>"""},
        ],
        "faq": [
            {"q": "How hard are FDE interviews compared to FAANG SWE interviews?", "a": "The coding portion is slightly easier than FAANG (fewer hard algorithmic problems, more practical coding). The system design portion is comparable but more applied (customer-specific scenarios vs. generic scale problems). The customer scenario round has no equivalent in FAANG interviews and is the most unique challenge. Overall, FDE interviews are different-hard rather than easier-hard."},
            {"q": "How long does the FDE interview process take?", "a": "Typically 2-4 weeks from first recruiter call to offer. Most companies do 4-6 interview rounds. Palantir's process can take 3-5 weeks. OpenAI and Anthropic move faster (2-3 weeks). Startups often complete the entire process in 1-2 weeks with fewer rounds."},
            {"q": "Do I need to prepare differently for AI-company FDE interviews?", "a": "Yes. AI-company FDE interviews (OpenAI, Anthropic, Cohere, Databricks) typically include questions about LLM deployment, prompt engineering, RAG architecture, and model evaluation. If you're interviewing at these companies, spend time building projects with LLMs and understanding production AI system design. Non-AI companies focus on traditional software engineering and integration skills."},
            {"q": "What programming language should I use in FDE coding interviews?", "a": "Python is the safest choice. It's the most common language in FDE job descriptions and interviewers are most familiar with it. TypeScript is a strong second choice, especially for product-focused FDE roles. Use whatever language lets you write clean, readable code fastest. FDE interviewers care about code quality and communication more than language choice."},
            {"q": "Are there take-home assignments in FDE interviews?", "a": "Some companies include a take-home project (typically 3-4 hours of work). Common formats: build an integration between two APIs, clean and transform a messy dataset, or build a small customer-facing tool. Palantir and OpenAI have used take-homes. Salesforce and Ramp generally don't. Ask the recruiter about the interview format upfront so you can plan your time."},
        ],
    },
]


def generate_career_pages():
    print("  Generating career pages...")
    count = 0

    for page in PAGES:
        related = get_related_links([
            {"href": "/companies/", "label": "Companies Hiring FDEs"},
            {"href": "/salaries/", "label": "FDE Salary Data"},
            {"href": "/insights/forward-deployed-engineer-vs-solutions-engineer/", "label": "FDE vs Solutions Engineer"},
            {"href": "/career/forward-deployed-ai-engineer/", "label": "AI FDE Guide"},
            {"href": "/jobs/", "label": "Browse FDE Jobs"},
        ])
        sections_html = ""
        for section in page["sections"]:
            sections_html += f'''
                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">{section["heading"]}</h2>
                {section["content"]}'''

        faq_html = ""
        faq_items = []
        for faq in page["faq"]:
            faq_html += f'''
                <div style="margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border);">
                    <h3 style="font-size: 1.15rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">{faq["q"]}</h3>
                    <p style="color: var(--text-secondary); line-height: 1.7;">{faq["a"]}</p>
                </div>'''
            faq_items.append({"@type": "Question", "name": faq["q"], "acceptedAnswer": {"@type": "Answer", "text": faq["a"]}})

        body = f'''
        <section class="section" style="max-width: 900px; margin: 0 auto; padding-top: 8rem;">
            <h1 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">{page["title"]}</h1>
            <div style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 1.5rem;">By <a href="https://www.linkedin.com/in/romethorndike/" target="_blank" rel="noopener" style="color: var(--amber); text-decoration: none;">Rome Thorndike</a></div>

            <div style="color: var(--text-secondary); font-size: 1.05rem; line-height: 1.8;">
                {sections_html}

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
            {"@type": "ListItem", "position": 2, "name": "Career", "item": f"{BASE_URL}/career/"},
            {"@type": "ListItem", "position": 3, "name": page["title"], "item": f"{BASE_URL}/career/{page['slug']}/"}
        ]}, indent=2)

        article = get_article_schema(page["title"], page["meta_desc"], f"/career/{page['slug']}/", "2026-04-10")
        extra_head = f'<script type="application/ld+json">\n{faq_schema}\n    </script>\n    <script type="application/ld+json">\n{breadcrumb}\n    </script>\n    {article}'

        html = get_html_head(
            title=page["title"],
            description=page["meta_desc"],
            canonical_path=f"/career/{page['slug']}/",
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

        out_dir = os.path.join(SITE_DIR, 'career', page['slug'])
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        count += 1

    print(f"  {count} career pages generated")


if __name__ == "__main__":
    generate_career_pages()
