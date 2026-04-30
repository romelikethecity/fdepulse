#!/usr/bin/env python3
"""
Generate company-specific FDE profile pages.
pSEO Profiles playbook. targets "[company] forward deployed engineer" queries.
"""

import os, sys, json

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from nav_config import SITE_NAME, BASE_URL
from templates import get_html_head, get_header_html, get_footer_html, get_mobile_nav_js, get_signup_js, get_cta_box, get_related_links

SITE_DIR = os.path.join(os.path.dirname(script_dir), 'site')

COMPANIES = [
    {
        "slug": "palantir", "name": "Palantir", "hq": "Denver, CO", "fde_count": "200+", "salary": "$135,000 - $250,000",
        "overview": "Palantir invented the Forward Deployed Engineer role in the early 2010s. Their FDE program is the gold standard that every other company copies. Palantir FDEs deploy Foundry and Gotham platforms inside government agencies, healthcare systems, energy companies, and financial institutions. The role is central to Palantir's entire go-to-market strategy: instead of selling software licenses and walking away, Palantir embeds engineers with customers to build custom analytical applications on top of their platforms.",
        "what_fdes_do": "Palantir FDEs work in verticals: government/defense, healthcare, energy, and financial services. A government FDE might build a logistics optimization system for the US Army. A healthcare FDE might build a clinical decision support application for a hospital network. Each deployment is custom. FDEs own the full stack: data modeling, pipeline construction, application building, user training, and ongoing support. Palantir distinguishes between FDE (more customer-facing, business-oriented) and FDSE (Forward Deployed Software Engineer, more code-heavy). New grads typically start as FDSE.",
        "tech_stack": "Palantir's proprietary platforms (Foundry, Gotham, Apollo, AIP), Python, TypeScript, Java, SQL, Spark, data modeling. FDEs need to learn Palantir's platform deeply. External tool experience matters less than the ability to learn proprietary systems fast.",
        "interview": "Palantir's FDE interview is 5-6 rounds: recruiter screen, coding (2 rounds, medium-hard), system design, customer scenario (called 'deployment exercise'), and a behavioral/values round. The deployment exercise is unique to Palantir: you're given a dataset and asked to build an analytical application while explaining your approach to a mock customer. The entire process takes 3-5 weeks. Palantir is known for slower hiring timelines than startups.",
        "culture": "Mission-driven culture focused on building software for institutions that protect society. FDEs travel 40-60% (higher than most FDE roles elsewhere). Deployments can be intense: 2-3 months embedded at a customer site. Work-life balance varies by deployment. Palantir values independent operators who can run customer engagements with minimal oversight. The learning curve is steep but the career development is unmatched in the FDE space.",
        "faq": [
            {"q": "What is the difference between FDE and FDSE at Palantir?", "a": "FDE (Forward Deployed Engineer) is more customer-facing: scoping projects, managing relationships, translating business problems into technical solutions. FDSE (Forward Deployed Software Engineer) is more code-heavy: building data pipelines, applications, and platform customizations. In practice, both roles overlap significantly. FDSEs often transition to FDE as they gain customer experience. FDSE is the more common entry point for new grads and engineers with less customer-facing background."},
            {"q": "Does Palantir hire new grads for FDE roles?", "a": "Yes, primarily through the FDSE (Forward Deployed Software Engineer) track. Palantir actively recruits from top CS programs and runs a structured onboarding program for new grads. The FDSE new grad role is one of the few entry-level FDE positions in the industry. Starting salaries for new grad FDSEs are $130,000-$155,000 base plus equity."},
            {"q": "How much travel does a Palantir FDE do?", "a": "More than most FDE roles at other companies. Palantir FDEs travel 40-60%, often spending 2-3 months embedded at a single customer site. Government deployments may require security clearances and work at secure facilities. The travel intensity is one of the main lifestyle trade-offs of Palantir FDE work compared to FDE roles at companies like Salesforce or OpenAI that offer more remote flexibility."},
            {"q": "What is Palantir FDE salary and total compensation?", "a": "Base salary ranges from $135,000 (new grad FDSE) to $250,000 (senior FDE). Total compensation including equity can reach $350,000+ at senior levels. Palantir RSUs vest over 4 years. As a public company (NYSE: PLTR), equity value is liquid. Palantir's compensation is competitive with Big Tech but below top-paying AI startups like OpenAI or Databricks at equivalent seniority levels."},
            {"q": "Is Palantir FDE a good first job?", "a": "For the right person, it's one of the best first jobs in tech. You'll learn faster than in almost any other role: building real production systems, working with senior customers, and developing both technical and business skills simultaneously. The downsides are heavy travel, steep learning curve, and the pressure of customer-facing work from day one. If you thrive under intensity and want maximum career acceleration, Palantir FDSE is an excellent starting point."},
        ],
    },
    {
        "slug": "openai", "name": "OpenAI", "hq": "San Francisco, CA", "fde_count": "50+", "salary": "$185,000 - $285,000",
        "overview": "OpenAI runs the largest dedicated FDE team among pure AI companies. Their FDEs deploy ChatGPT Enterprise, custom GPT models, and the OpenAI API inside Fortune 500 companies. As OpenAI shifted from research lab to enterprise software company, FDEs became essential to their go-to-market strategy. Enterprise customers buying $1M+ API contracts need more than documentation. They need engineers who understand both the models and the customer's business to make deployments successful.",
        "what_fdes_do": "OpenAI FDEs work with enterprise customers across healthcare, financial services, legal, and technology sectors. Day-to-day work includes: designing RAG (retrieval-augmented generation) architectures specific to each customer's data, building custom prompt chains and agent workflows, integrating the OpenAI API with customer systems (EHR, CRM, ERP), evaluating model performance for specific use cases, and implementing safety guardrails and content filtering. FDEs also feed customer insights back to the product and research teams, directly influencing model development priorities.",
        "tech_stack": "Python (primary), OpenAI API, LangChain/LlamaIndex (RAG frameworks), vector databases (Pinecone, Weaviate, Chroma), TypeScript, FastAPI, Docker, Kubernetes, AWS/Azure. FDEs need deep LLM knowledge: prompt engineering, fine-tuning, evaluation metrics, token optimization, and safety/alignment techniques.",
        "interview": "OpenAI's FDE interview is 4-5 rounds over 2-3 weeks: recruiter screen, coding (practical Python, not LeetCode-heavy), system design (expect an LLM deployment scenario), customer scenario round, and a team/values interview. The system design round is heavily AI-focused: 'Design a RAG pipeline for a healthcare customer with HIPAA requirements.' OpenAI moves faster than Palantir but is highly selective. They want engineers who genuinely understand AI, not just engineers who can call APIs.",
        "culture": "Mission-driven culture centered on ensuring AI benefits everyone. FDE work at OpenAI is high-profile: you're deploying the most talked-about AI technology in the world to the most demanding enterprise customers. The pace is intense. Product changes frequently, requiring FDEs to adapt quickly. Compensation is among the highest in the FDE market. The team is small (50 people) relative to the impact, meaning each FDE handles significant customer relationships.",
        "faq": [
            {"q": "What is the OpenAI FDE salary?", "a": "Base salary ranges from $185,000 to $285,000 depending on seniority. Total compensation including equity (PPUs. profit participation units) can significantly exceed base salary. OpenAI's PPUs are valued based on private market valuations that have increased substantially. At senior levels, total compensation can reach $400,000-$500,000+. OpenAI pays at or above the top of the FDE market."},
            {"q": "Do I need AI/ML experience to be an OpenAI FDE?", "a": "Yes. Unlike FDE roles at non-AI companies, OpenAI expects FDE candidates to have hands-on experience with LLMs: prompt engineering, RAG architecture, model evaluation, and ideally fine-tuning. Candidates who've only used ChatGPT as a consumer product won't pass the technical bar. You need to have built production systems using the OpenAI API or similar LLM platforms. Prior ML engineering or AI research experience is a strong signal."},
            {"q": "How does OpenAI's FDE interview differ from standard SWE interviews?", "a": "OpenAI's FDE coding rounds are more practical and less algorithmic than their SWE interviews. Expect to build something real (a data pipeline, an API integration, a prompt chain) rather than solve LeetCode problems. The system design round is AI-specific: you'll design an LLM deployment architecture for a customer scenario. The customer scenario round tests your ability to scope a deployment, manage stakeholder expectations, and communicate technical trade-offs to non-technical customers."},
            {"q": "Is OpenAI FDE remote?", "a": "OpenAI's FDE roles are primarily based in San Francisco with some travel to customer sites. Fully remote FDE positions at OpenAI are rare. The company emphasizes in-person collaboration, especially for customer-facing roles where team coordination is critical. If remote work is a priority, consider Salesforce or Databricks FDE roles, which offer more location flexibility."},
            {"q": "What's the career path for an OpenAI FDE?", "a": "OpenAI's FDE team is still relatively new, so career paths are less formalized than at Palantir. Common trajectories include: moving into a senior/lead FDE role managing larger customer portfolios, transitioning to product management (FDEs have direct customer insight that PMs value), moving to the solutions architecture or partnerships team, or returning to a research/engineering role on the core model team. The AI domain expertise you build as an OpenAI FDE is highly transferable to any AI company."},
        ],
    },
    {
        "slug": "anthropic", "name": "Anthropic", "hq": "San Francisco, CA", "fde_count": "20-30", "salary": "$180,000 - $280,000",
        "overview": "Anthropic's FDE team deploys Claude (their AI assistant) for enterprise customers. As one of the leading AI safety companies, Anthropic's FDE role carries an additional dimension: ensuring that enterprise deployments meet Anthropic's safety standards while delivering customer value. Anthropic FDEs work at the intersection of powerful AI capabilities and responsible deployment, making the role uniquely challenging and impactful.",
        "what_fdes_do": "Anthropic FDEs build custom Claude integrations for enterprise customers in healthcare, legal, financial services, and technology. Typical projects include: building RAG systems over proprietary customer data, implementing custom agent workflows using Claude's tool use capabilities, designing safety guardrails specific to regulated industries (HIPAA, SOC2, FINRA), and integrating Claude into existing customer workflows. FDEs also work closely with Anthropic's safety research team to ensure enterprise deployments align with responsible AI principles.",
        "tech_stack": "Python, Anthropic API, Claude SDK, TypeScript, vector databases, Docker/Kubernetes, AWS/GCP. Strong emphasis on AI safety tooling: content filtering, output evaluation, red-teaming, and bias detection. FDEs need to understand constitutional AI and RLHF concepts to explain Anthropic's safety approach to enterprise customers.",
        "interview": "Anthropic's FDE interview is 4-5 rounds: recruiter screen, coding (practical, not algorithmic), system design (AI deployment scenario), customer scenario (with a safety twist), and a values/mission alignment interview. The values round is more important at Anthropic than at most companies. They specifically assess whether candidates care about AI safety and can articulate why responsible deployment matters. Candidates who are purely motivated by compensation or prestige may not be a good fit.",
        "culture": "Safety-first culture with a research-lab feel. Anthropic is smaller than OpenAI and more academically oriented. FDEs are expected to engage with safety research and contribute to internal discussions about responsible deployment. The pace is fast but thoughtful. Anthropic values careful reasoning over speed. FDE team sizes are smaller, meaning more autonomy per engineer but also higher expectations for independent judgment.",
        "faq": [
            {"q": "How does Anthropic's FDE role differ from OpenAI's?", "a": "The technical work is similar (deploying LLMs for enterprise customers), but Anthropic places significantly more emphasis on AI safety in the FDE role. Anthropic FDEs are expected to be safety advocates at customer sites, sometimes pushing back on customer requests that conflict with responsible AI practices. OpenAI FDEs are more focused on maximizing customer value with fewer safety constraints in the deployment process. If AI safety is important to you, Anthropic is the stronger cultural fit."},
            {"q": "What is the Anthropic FDE salary?", "a": "Base salary ranges from $180,000 to $280,000 depending on seniority. Total compensation including equity is competitive with OpenAI. Anthropic's private valuation has increased significantly, making early equity grants potentially very valuable. The compensation is at the top of the FDE market, similar to OpenAI and slightly above Palantir at equivalent seniority levels."},
            {"q": "Does Anthropic have FDE roles in London?", "a": "Yes. Anthropic has expanded FDE hiring to London as part of their European operations. London FDE roles focus on enterprise customers in the UK and European markets, with additional emphasis on EU AI Act compliance. London FDE salaries are adjusted for the local market but remain competitive with top London tech compensation."},
            {"q": "Do I need a PhD to be an Anthropic FDE?", "a": "No. Anthropic's research roles often prefer PhDs, but FDE roles prioritize practical engineering experience. A strong software engineering background (3-5+ years) with hands-on LLM experience is the core requirement. That said, FDE candidates who can engage with AI safety concepts at a technical level (understanding RLHF, constitutional AI, model evaluation) have a meaningful advantage in Anthropic's interview process."},
            {"q": "Is Anthropic FDE a good career move if I'm interested in AI safety?", "a": "It's one of the best roles in the industry for combining AI safety interests with practical engineering work. You'll deploy AI systems in high-stakes enterprise environments while working closely with Anthropic's safety research team. The domain knowledge and safety expertise you build are highly differentiated. Few other companies offer FDE roles where safety is a first-class concern rather than an afterthought."},
        ],
    },
    {
        "slug": "salesforce", "name": "Salesforce", "hq": "San Francisco, CA", "fde_count": "1,000 (target)", "salary": "$170,000 - $240,000",
        "overview": "Salesforce committed to hiring 1,000 Forward Deployed Engineers for their Agentforce AI platform, making it the largest single FDE hiring initiative in history. When the world's largest enterprise software company restructures their go-to-market around Forward Deployed Engineers, it validates the role as a standard function in enterprise software. Salesforce FDEs deploy AI agents that automate sales, service, marketing, and commerce workflows for Salesforce's 150,000+ enterprise customers.",
        "what_fdes_do": "Salesforce FDEs deploy Agentforce AI agents inside enterprise customer orgs. Day-to-day work includes: configuring and customizing AI agents for specific business processes, building data integrations between Salesforce and customer data sources, training customer teams on AI agent capabilities, monitoring agent performance and iterating on prompts/workflows, and feeding deployment insights back to the Agentforce product team. Salesforce FDEs work within the existing Salesforce ecosystem, so deep Salesforce platform knowledge (Apex, Lightning, SOQL, Einstein) is a differentiator.",
        "tech_stack": "Salesforce platform (Apex, Lightning Web Components, SOQL, Einstein AI), Python, JavaScript/TypeScript, MuleSoft (integration), Tableau (analytics), SQL. FDEs also need familiarity with LLM concepts since Agentforce is built on AI foundations. Salesforce's proprietary ecosystem means FDEs spend significant time learning platform-specific tools rather than open-source technologies.",
        "interview": "Salesforce FDE interviews are 4-5 rounds: recruiter screen, coding (medium difficulty, often Salesforce-ecosystem-adjacent), system design (focused on integration and data architecture), customer scenario, and behavioral/values. Salesforce values 'Ohana' culture fit and customer obsession. The interview is less algorithmically difficult than Palantir or OpenAI but places more emphasis on communication skills and Salesforce ecosystem knowledge. Prior Salesforce experience isn't required but is a significant advantage.",
        "culture": "Salesforce has a structured, process-oriented culture with strong training infrastructure. FDEs benefit from Trailhead (Salesforce's learning platform), mentorship programs, and a large peer community. Travel is moderate (20-30%). Work-life balance is generally better than at startups. Salesforce is a public company (NYSE: CRM) with predictable compensation and benefits. The FDE program is designed for scale: standardized onboarding, documented playbooks, and clear career progression from FDE I to FDE III and beyond.",
        "faq": [
            {"q": "Is Salesforce really hiring 1,000 FDEs?", "a": "Salesforce CEO Marc Benioff announced the 1,000-FDE target for the Agentforce platform. As of early 2026, hiring is actively ramping. The company is posting FDE roles across multiple geographies and seniority levels. Whether they hit exactly 1,000 depends on market conditions and Agentforce adoption, but the commitment signals a massive, sustained investment in the FDE model."},
            {"q": "Do I need Salesforce experience to become a Salesforce FDE?", "a": "No, but it helps significantly. Salesforce FDE job postings list Salesforce platform experience as 'preferred' rather than 'required.' Strong software engineering skills plus willingness to learn the Salesforce ecosystem are sufficient. However, candidates with existing Salesforce certifications (Admin, Developer I/II, Platform App Builder) skip the platform learning curve and can contribute faster to customer deployments."},
            {"q": "How does Salesforce FDE compare to Salesforce Solutions Engineer?", "a": "Salesforce Solutions Engineers are pre-sales: they demo Salesforce products to prospects and help close deals. FDEs are post-sale: they deploy Agentforce AI agents inside existing customer environments. SEs have quota-based compensation with commissions. FDEs have standard engineering compensation with equity. If you prefer building over selling, FDE is the better fit. Both roles require strong customer communication skills."},
            {"q": "What is the Salesforce FDE career progression?", "a": "Salesforce has a structured FDE career ladder: FDE I (entry/junior), FDE II (mid-level), FDE III (senior), Lead FDE, and FDE Manager. The progression mirrors Salesforce's standard engineering ladder with equivalent compensation bands. Promotion timelines are typically 2-3 years per level. FDEs can also transition to product management, solutions architecture, or engineering management roles within Salesforce."},
            {"q": "Is Salesforce FDE remote?", "a": "Many Salesforce FDE roles offer remote or hybrid options. Salesforce adopted a flexible work model ('Work from Anywhere') during the pandemic and has maintained it. Remote FDE roles require periodic travel to customer sites (estimated 20-30% travel). Fully on-site FDE roles exist at major Salesforce hubs (SF, NYC, Chicago, Atlanta) for candidates who prefer in-person collaboration."},
        ],
    },
    {
        "slug": "databricks", "name": "Databricks", "hq": "San Francisco, CA", "fde_count": "30+", "salary": "$175,000 - $260,000",
        "overview": "Databricks FDEs deploy the Databricks Lakehouse Platform and Mosaic AI tools inside enterprise data teams. As one of the highest-valued private tech companies, Databricks' FDE equity could be worth significantly more than the base salary if the company goes public. FDEs at Databricks sit at the intersection of data engineering, ML/AI, and customer deployment, making it one of the most technically demanding FDE roles in the market.",
        "what_fdes_do": "Databricks FDEs build custom data pipelines, ML workflows, and AI applications on the Databricks platform for enterprise customers. Typical projects: migrating a customer's data warehouse to a lakehouse architecture, building MLOps pipelines for model training and deployment, implementing Unity Catalog for data governance across a customer's organization, and deploying Mosaic AI for custom model fine-tuning. The role is heavier on data engineering than most FDE positions. FDEs work with Apache Spark, Delta Lake, MLflow, and Databricks' proprietary tools daily.",
        "tech_stack": "Python, SQL, Apache Spark, Delta Lake, MLflow, Databricks Notebooks, Unity Catalog, Mosaic AI, Terraform, Docker, AWS/Azure/GCP. Strong data engineering fundamentals are essential. FDEs who understand distributed computing, data modeling, and ML pipelines thrive. Web development skills are less important than at other FDE roles.",
        "interview": "Databricks FDE interviews are 4-5 rounds: recruiter screen, coding (data-focused Python, SQL heavy), system design (expect a data pipeline or lakehouse architecture question), customer scenario, and a team/values round. The technical bar is high. Databricks wants engineers who can explain complex data concepts to non-technical stakeholders. Strong SQL skills are surprisingly important for this role.",
        "culture": "Engineering-centric culture with a strong open-source heritage (Apache Spark originated at Databricks). FDEs are treated as peers to product engineers, not as a separate support organization. The company is growing fast with pre-IPO energy. Compensation is competitive, and the equity component could be substantial. Travel is moderate (20-30%). Remote-friendly for many FDE roles.",
        "faq": [
            {"q": "What is the Databricks FDE salary and equity?", "a": "Base salary ranges from $175,000 to $260,000. Total compensation including RSUs (restricted stock units) can reach $350,000-$450,000 at senior levels. As a private company valued at $43B+, Databricks equity isn't liquid yet but could be very valuable at IPO. FDEs who join pre-IPO with significant equity grants stand to benefit most."},
            {"q": "Do I need Spark experience to be a Databricks FDE?", "a": "It's strongly preferred but not strictly required. If you have strong Python, SQL, and general data engineering experience, you can learn Spark on the job. However, candidates who already know Spark, Delta Lake, and the Databricks platform have a significant advantage in interviews and ramp up to customer deployments much faster. Consider getting a Databricks certification before applying."},
            {"q": "How technical is the Databricks FDE role?", "a": "Very technical. Databricks FDE is one of the most engineering-heavy FDE roles in the market. You'll write production data pipelines, optimize Spark jobs, build ML workflows, and debug distributed computing issues. If you're looking for an FDE role that's closer to data engineering than customer management, Databricks is the right fit."},
            {"q": "Is Databricks FDE a good path to ML engineering?", "a": "Excellent. Databricks FDEs work daily with ML tooling (MLflow, Mosaic AI, model deployment pipelines). The customer exposure gives you applied ML experience that pure ML engineers in research labs don't get. Many Databricks FDEs transition to ML engineering or MLOps roles, either within Databricks or at other companies."},
            {"q": "Does Databricks have FDE roles outside San Francisco?", "a": "Yes. Databricks has FDE roles in multiple locations including New York, Seattle, London, and some remote positions. The company is more distributed than OpenAI or Anthropic. Remote FDE roles require periodic customer site visits but are available for candidates who prefer not to relocate to the Bay Area."},
        ],
    },
    {
        "slug": "scale-ai", "name": "Scale AI", "hq": "San Francisco, CA", "fde_count": "20+", "salary": "$165,000 - $245,000",
        "overview": "Scale AI FDEs deploy data labeling, model evaluation, and AI infrastructure products for enterprise and government customers. Scale AI sits at a unique intersection: their FDEs need to understand both the data annotation workflows that train AI models and the production ML systems that use that training data. The company serves defense (US DOD), automotive (self-driving cars), and general enterprise AI customers.",
        "what_fdes_do": "Scale AI FDEs build custom data pipelines for AI training: designing annotation workflows, integrating customer data sources with Scale's labeling platform, building quality assurance systems for labeled data, and deploying model evaluation frameworks. Government FDEs work on classified projects requiring security clearances. Commercial FDEs work with autonomous vehicle companies, healthcare AI firms, and large language model developers. The work is uniquely data-centric compared to other FDE roles.",
        "tech_stack": "Python, SQL, Scale AI platform, data pipeline tools (Airflow, dbt), cloud platforms (AWS/GCP), Docker, Kubernetes. Government-focused FDEs also need familiarity with classified computing environments and FedRAMP compliance. Data quality assessment and annotation workflow design are Scale-specific skills that transfer to any ML data engineering role.",
        "interview": "Scale AI FDE interviews are 4-5 rounds: recruiter screen, coding (practical Python, data processing focus), system design (data pipeline architecture), customer scenario, and behavioral. The technical emphasis is on data engineering and quality systems rather than frontend or web development. Scale looks for engineers who understand how data quality impacts model performance.",
        "culture": "Mission-oriented culture (Scale's tagline: 'Accelerate the development of AI'). The government contracts add a national security dimension to the work. Scale AI's FDE team is smaller than Palantir's but growing fast. Compensation is strong, with pre-IPO equity that could be significant. Travel varies by customer: government deployments may require more on-site presence than commercial deployments.",
        "faq": [
            {"q": "Does Scale AI FDE require a security clearance?", "a": "For government-focused FDE roles, yes. Scale AI has significant DOD contracts. FDEs working on these projects need an active or obtainable security clearance (typically Secret or Top Secret). Commercial FDE roles at Scale AI do not require clearances. The application process will specify if a clearance is needed."},
            {"q": "What makes Scale AI FDE different from other FDE roles?", "a": "Scale AI FDEs are uniquely data-centric. While most FDE roles focus on deploying a software product, Scale AI FDEs design and manage the data pipelines that train AI models. This means more work on data quality, annotation workflow design, and evaluation metrics. It's the most data-engineering-heavy FDE role in the market, making it a strong fit for engineers who love working with data rather than building user-facing applications."},
            {"q": "What is Scale AI FDE total compensation?", "a": "Base salary ranges from $165,000 to $245,000. Total compensation including equity can reach $300,000-$400,000 at senior levels. As a private company valued at $14B+, Scale AI's equity is pre-liquidity. FDEs who joined early and received significant equity grants could see substantial returns at IPO. Current grants are priced at the latest valuation."},
            {"q": "Is Scale AI FDE remote-friendly?", "a": "Scale AI offers remote FDE positions for commercial customers. Government FDE roles typically require on-site presence at secure facilities. Remote commercial FDE roles require periodic travel to customer sites (estimated 20-30%). The company is San Francisco-headquartered but supports distributed teams for non-classified work."},
            {"q": "What career paths do Scale AI FDEs pursue after?", "a": "Scale AI FDEs commonly move into: ML engineering (the data pipeline expertise transfers directly), data engineering leadership at AI companies, product management for AI/data products, or founding AI-focused startups. The government FDE path also opens doors to defense tech companies like Anduril, Palantir, and Shield AI."},
        ],
    },
    {
        "slug": "ramp", "name": "Ramp", "hq": "New York, NY", "fde_count": "15-25", "salary": "$160,000 - $220,000",
        "overview": "Ramp FDEs deploy the company's corporate card, expense management, and financial automation platform for enterprise customers. Ramp is one of the fastest-growing fintech companies, and their FDE team handles the complex financial system integrations that enterprise adoption requires. FDEs at Ramp work at the intersection of fintech infrastructure and enterprise IT, making it a unique FDE role focused on financial data rather than AI or analytics.",
        "what_fdes_do": "Ramp FDEs build custom integrations between Ramp's financial platform and customer systems: ERP platforms (NetSuite, SAP, Oracle), HRIS systems (Workday, BambooHR), accounting software (QuickBooks, Xero), and banking infrastructure. They also configure custom approval workflows, build expense policy automation, and implement financial controls specific to each customer. The work is less AI-focused than OpenAI or Anthropic but more operationally critical: getting financial data wrong has immediate, measurable business impact.",
        "tech_stack": "Python, TypeScript, SQL, REST APIs, GraphQL, Ramp's internal platform, ERP integration tools, financial data standards (ISO 20022, NACHA). FDEs need strong API integration skills and comfort working with financial data. Understanding of accounting principles (GL codes, cost centers, accrual vs. cash accounting) is surprisingly helpful for this role.",
        "interview": "Ramp's FDE interview is 4-5 rounds: recruiter screen, coding (practical API and data work), system design (integration architecture focus), customer scenario, and a team fit round. Ramp moves faster than most companies (2 weeks from first call to offer). They value speed and execution. The technical bar is high but the problems are more practical than algorithmic. Expect questions about designing strong integrations, handling edge cases in financial data, and managing data migration between systems.",
        "culture": "Speed-obsessed startup culture. Ramp ships fast and expects FDEs to match that pace. The team is lean, which means each FDE handles significant customer impact. NYC-based with a strong in-office culture, though some remote FDE roles exist. Compensation is competitive for a growth-stage startup, with meaningful equity grants. Ramp's valuation has grown rapidly, making early equity grants potentially very valuable.",
        "faq": [
            {"q": "What makes Ramp's FDE role different?", "a": "Ramp FDEs focus on financial system integrations rather than AI or analytics deployments. This means more work with ERP systems, accounting software, and banking infrastructure. The work is highly operational: accuracy matters more than speed because financial data errors have immediate, quantifiable business impact. If you enjoy data integration and financial systems, Ramp's FDE role is uniquely well-suited."},
            {"q": "Do I need fintech experience for Ramp's FDE role?", "a": "Not required but helpful. Ramp looks for strong software engineers who can learn financial systems on the job. That said, candidates who understand accounting concepts (GL codes, journal entries, cost centers) or have worked with ERP systems have a meaningful advantage. If you've built integrations with financial APIs or worked at a fintech company, highlight that experience prominently."},
            {"q": "What is Ramp FDE compensation?", "a": "Base salary ranges from $160,000 to $220,000. Total compensation including equity is competitive with larger companies when factoring in Ramp's rapid valuation growth. Ramp stock options are pre-IPO, meaning they carry both upside potential and liquidity risk. The equity component can be significant for early FDE hires."},
            {"q": "Is Ramp's FDE role in-office?", "a": "Ramp has a strong in-office culture in their New York City headquarters. Most FDE roles are based in NYC with in-office expectations 3-4 days per week. Some remote FDE roles exist but are less common. If you're committed to remote work, other companies (Salesforce, Databricks) offer more flexibility."},
            {"q": "What's the career path for a Ramp FDE?", "a": "Ramp FDEs commonly progress to: senior FDE (managing larger enterprise accounts), engineering management within Ramp's customer-facing engineering org, product management (especially for integration and platform products), or solutions architecture roles at other fintech companies. Ramp's lean team structure means FDEs get broad exposure that accelerates career growth faster than at larger companies."},
        ],
    },
    {
        "slug": "rippling", "name": "Rippling", "hq": "San Francisco, CA", "fde_count": "10-20", "salary": "$155,000 - $230,000",
        "overview": "Rippling FDEs deploy the company's unified HR, IT, and finance platform for enterprise customers. Rippling's product is unusually broad (it replaces 5-10 separate SaaS tools), which makes FDE deployments complex but impactful. FDEs handle the migration, integration, and customization work that lets enterprise customers consolidate their HR, payroll, benefits, device management, and app provisioning onto a single platform.",
        "what_fdes_do": "Rippling FDEs manage complex enterprise migrations: moving customer data from legacy HRIS, payroll, and IT systems to Rippling's unified platform. This includes data migration, custom workflow configuration, SSO/identity integration, device management setup, and benefits administration configuration. FDEs also build custom integrations between Rippling and customer systems that aren't natively supported. The role requires understanding of HR/IT/finance business processes in addition to software engineering.",
        "tech_stack": "Python, TypeScript, SQL, REST APIs, Rippling's internal platform, SCIM (identity provisioning), SSO protocols (SAML, OIDC), MDM (mobile device management) tools, HRIS data standards. FDEs need comfortable working with identity and access management systems. Understanding of HR workflows (onboarding, offboarding, payroll processing) differentiates strong candidates.",
        "interview": "Rippling FDE interviews are 4-5 rounds: recruiter screen, coding (practical, integration-focused), system design (enterprise migration scenario), customer scenario, and behavioral. Rippling values engineers who can handle complexity and ambiguity. Expect system design questions about migrating an enterprise customer from 5 separate SaaS tools to Rippling's unified platform. They want to see how you handle interconnected systems with conflicting data.",
        "culture": "Intense, execution-focused startup culture led by Parker Conrad (serial founder). Rippling moves fast and expects FDEs to match. The product surface area is enormous, which means FDEs need to learn many domains (HR, IT, finance, identity) rather than specializing in one. Compensation is competitive with meaningful pre-IPO equity. The company has raised $1.4B+ at high valuations.",
        "faq": [
            {"q": "What makes Rippling's FDE role unique?", "a": "Rippling's product breadth makes this the most domain-diverse FDE role. You'll work across HR, IT, finance, and identity management in a single deployment. Most FDE roles at other companies focus on one domain (AI at OpenAI, data at Databricks, finance at Ramp). Rippling FDEs need to be generalists who can quickly learn new business domains."},
            {"q": "Do I need HR or IT experience for Rippling's FDE role?", "a": "Not required, but understanding HR workflows (onboarding, payroll, benefits) and IT administration (SSO, device management, identity provisioning) accelerates your ramp time significantly. Rippling trains FDEs on the platform, but domain knowledge helps you ask better questions during customer deployments and anticipate migration challenges."},
            {"q": "What is Rippling FDE compensation?", "a": "Base salary ranges from $155,000 to $230,000. Total compensation including equity can be substantial given Rippling's high valuation ($13.5B as of last raise). Pre-IPO equity carries both upside potential and liquidity risk. The equity grants for early FDE hires could be significant if Rippling goes public."},
            {"q": "How much travel do Rippling FDEs do?", "a": "Moderate. Rippling FDEs typically travel 15-25% for customer onsite visits during migrations. The company is San Francisco-based with a strong in-office culture. Some remote FDE positions exist but most roles are based at Rippling offices. Travel intensity peaks during new enterprise customer deployments and decreases as the customer stabilizes on the platform."},
            {"q": "Is Rippling FDE a good career move?", "a": "If you want breadth over depth, yes. Rippling FDEs develop a uniquely broad skill set spanning HR tech, IT infrastructure, identity management, and financial systems. This generalist expertise is valuable for founding startups, consulting, or taking product/engineering leadership roles at enterprise software companies. The risk is that Rippling's intense culture isn't for everyone."},
        ],
    },
]


def generate_company_profile_pages():
    print("  Generating company profile pages...")
    count = 0

    for co in COMPANIES:
        faq_html = ""
        faq_items = []
        for faq in co["faq"]:
            faq_html += f'''
                <div style="margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border);">
                    <h3 style="font-size: 1.15rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">{faq["q"]}</h3>
                    <p style="color: var(--text-secondary); line-height: 1.7;">{faq["a"]}</p>
                </div>'''
            faq_items.append({"@type": "Question", "name": faq["q"], "acceptedAnswer": {"@type": "Answer", "text": faq["a"]}})

        related = get_related_links([
            {"href": "/salaries/", "label": "FDE Salary Data"},
            {"href": "/career/forward-deployed-engineer-interview-questions/", "label": "FDE Interview Questions"},
            {"href": "/insights/forward-deployed-engineer-vs-software-engineer/", "label": "FDE vs Software Engineer"},
            {"href": "/career/forward-deployed-engineer-levels/", "label": "FDE Career Levels"},
            {"href": "/jobs/", "label": "Browse All FDE Jobs"},
        ])

        body = f'''
        <section class="section" style="max-width: 900px; margin: 0 auto; padding-top: 8rem;">
            <h1 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">Forward Deployed Engineer at {co["name"]}</h1>
            <p style="font-size: 1rem; color: var(--text-muted); margin-bottom: 2rem;">{co["hq"]} &middot; {co["fde_count"]} FDEs &middot; {co["salary"]}</p>

            <div style="color: var(--text-secondary); font-size: 1.05rem; line-height: 1.8;">
                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 0 0 1rem;">Overview</h2>
                <p style="margin-bottom: 1.25rem;">{co["overview"]}</p>

                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">What FDEs Do at {co["name"]}</h2>
                <p style="margin-bottom: 1.25rem;">{co["what_fdes_do"]}</p>

                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Tech Stack</h2>
                <p style="margin-bottom: 1.25rem;">{co["tech_stack"]}</p>

                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Interview Process</h2>
                <p style="margin-bottom: 1.25rem;">{co["interview"]}</p>

                <h2 style="font-size: 1.75rem; font-weight: 700; color: var(--text-primary); margin: 2.5rem 0 1rem;">Culture & Work-Life</h2>
                <p style="margin-bottom: 1.25rem;">{co["culture"]}</p>

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
            {"@type": "ListItem", "position": 2, "name": "Companies", "item": BASE_URL + "/companies/"},
            {"@type": "ListItem", "position": 3, "name": co["name"], "item": BASE_URL + "/companies/" + co["slug"] + "/"},
        ]}, indent=2)
        org_schema = json.dumps({"@context": "https://schema.org", "@type": "Organization", "name": co["name"]}, indent=2)

        extra_head = '<script type="application/ld+json">\n' + faq_schema + '\n    </script>\n    <script type="application/ld+json">\n' + breadcrumb + '\n    </script>\n    <script type="application/ld+json">\n' + org_schema + '\n    </script>'

        html = get_html_head(
            title="FDE at " + co["name"] + ": Salary, Interview, Role",
            description="Forward Deployed Engineer at " + co["name"] + ". " + co["salary"] + " salary, interview process, tech stack, and what FDEs do. Complete guide.",
            canonical_path="/companies/" + co["slug"] + "/",
            extra_head=extra_head
        )
        html += "\n<body>\n"
        html += get_header_html()
        html += "\n    <main>\n"
        html += body
        html += "\n    </main>\n"
        html += get_footer_html()
        html += get_mobile_nav_js()
        html += get_signup_js()
        html += "\n</body>\n</html>"

        out_dir = os.path.join(SITE_DIR, 'companies', co['slug'])
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        count += 1

    print("  " + str(count) + " company profile pages generated")


if __name__ == "__main__":
    generate_company_profile_pages()
