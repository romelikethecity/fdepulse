#!/usr/bin/env python3
"""
Generate the /newsletter/ landing page for FDE Pulse.
Wires the existing signup handler (newsletter-subscribe.rome-workers.workers.dev).
"""

import os
import sys
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from nav_config import SITE_NAME, BASE_URL
from templates import (
    get_html_head, get_header_html, get_footer_html,
    get_mobile_nav_js, get_signup_js, get_cta_box, SIGNUP_WORKER_URL
)

SITE_DIR = os.path.join(os.path.dirname(script_dir), 'site')

FAQS = [
    {
        "q": "How often does the FDE Pulse Brief go out?",
        "a": "Every week. The brief goes out on Tuesday mornings, covering the prior week's data across active job postings, salary movements, and which companies opened or closed FDE roles."
    },
    {
        "q": "What's in the FDE Pulse Brief?",
        "a": "Each issue covers: the count of active FDE roles and week-over-week change, top new postings with salary data and direct links, a spotlight company (who they are, how many FDEs they hire, what the roles look like), and one data point from the market intelligence dataset (a skills breakdown, a salary by metro chart, or a team structure stat)."
    },
    {
        "q": "Is the newsletter free?",
        "a": "Yes, it's free. There's no paid tier. The FDE Pulse Brief is supported by the broader FDE Pulse platform."
    },
    {
        "q": "Can I unsubscribe?",
        "a": "Yes, at any time. Every issue includes an unsubscribe link in the footer. One click removes you from the list, no confirmation email required."
    },
    {
        "q": "How long does each issue take to read?",
        "a": "About 5 minutes. The brief is designed to be scannable. Each section is one to three short paragraphs with a data table or stat. No long essays, no opinion columns."
    },
]


def generate_newsletter_page():
    print("  Generating newsletter page...")

    faq_html = ''
    faq_schema_items = []
    for faq in FAQS:
        faq_html += f'''
            <div style="margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border);">
                <h3 style="font-size: 1.1rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">{faq["q"]}</h3>
                <p style="color: var(--text-secondary); line-height: 1.7;">{faq["a"]}</p>
            </div>'''
        faq_schema_items.append({
            "@type": "Question",
            "name": faq["q"],
            "acceptedAnswer": {"@type": "Answer", "text": faq["a"]}
        })

    # Sample issue content (rendered HTML, no external images)
    sample_issue = '''
        <div class="nl-sample">
            <div class="nl-sample__header">
                <div class="nl-sample__label">Sample Issue &mdash; Week of April 28, 2026</div>
                <div class="nl-sample__title">FDE Pulse Brief</div>
            </div>
            <div class="nl-sample__body">
                <div class="nl-sample__section">
                    <div class="nl-sample__section-title">This Week's Numbers</div>
                    <div class="nl-sample__stat-row">
                        <div class="nl-sample__stat">
                            <div class="nl-sample__stat-value">134</div>
                            <div class="nl-sample__stat-label">Active FDE roles</div>
                        </div>
                        <div class="nl-sample__stat">
                            <div class="nl-sample__stat-value">70</div>
                            <div class="nl-sample__stat-label">Companies hiring</div>
                        </div>
                        <div class="nl-sample__stat">
                            <div class="nl-sample__stat-value">$135K</div>
                            <div class="nl-sample__stat-label">Median base salary</div>
                        </div>
                        <div class="nl-sample__stat">
                            <div class="nl-sample__stat-value">83%</div>
                            <div class="nl-sample__stat-label">Salary disclosure rate</div>
                        </div>
                    </div>
                </div>
                <div class="nl-sample__section">
                    <div class="nl-sample__section-title">Top New Postings This Week</div>
                    <div class="nl-sample__job">
                        <div class="nl-sample__job-title">Senior Staff Forward Deployed Developer, Google Cloud</div>
                        <div class="nl-sample__job-meta">Google &middot; Multiple locations &middot; $262K &ndash; $365K &middot; <a href="/jobs/" style="color:var(--amber-light);">View role &rarr;</a></div>
                    </div>
                    <div class="nl-sample__job">
                        <div class="nl-sample__job-title">Forward Deployed Solution Engineer &mdash; Applied AI</div>
                        <div class="nl-sample__job-meta">ServiceNow &middot; Remote &middot; $201K &ndash; $352K &middot; <a href="/jobs/" style="color:var(--amber-light);">View role &rarr;</a></div>
                    </div>
                    <div class="nl-sample__job">
                        <div class="nl-sample__job-title">Lead Forward Deployed Engineer &mdash; AWS</div>
                        <div class="nl-sample__job-meta">Deloitte &middot; New York &middot; $167K &ndash; $308K &middot; <a href="/jobs/" style="color:var(--amber-light);">View role &rarr;</a></div>
                    </div>
                </div>
                <div class="nl-sample__section">
                    <div class="nl-sample__section-title">Market Signal: Remote FDE Pay Gap</div>
                    <p style="font-size:0.9rem; color:var(--text-secondary); line-height:1.7; margin:0;">Remote FDE roles pay $120K median vs $140K for on-site roles &mdash; a 14% gap. That gap has held steady for three consecutive weeks. FDEs choosing remote should factor in location cost-of-living when comparing offers.</p>
                </div>
            </div>
        </div>'''

    body = f'''
        <div class="nl-wrapper">
            <div class="nl-hero">
                <div class="nl-hero__badge">
                    <span class="nl-hero__badge-dot"></span>
                    Free weekly newsletter
                </div>
                <h1 class="nl-hero__title">FDE Pulse Brief</h1>
                <p class="nl-hero__sub">Weekly Forward Deployed Engineer market intelligence. Active job counts, salary data, top companies, new openings. Every Tuesday morning.</p>

                <div class="nl-hero__form-wrap">
                    <form class="signup-form nl-hero__form" onsubmit="handleSignup(event, this)">
                        <input type="email" name="email" placeholder="you@company.com" required>
                        <button type="submit">Subscribe free</button>
                    </form>
                    <div class="signup-msg"></div>
                    <div class="signup-trust">Unsubscribe anytime. No spam. About 5 minutes to read.</div>
                </div>
            </div>

            <div class="nl-value">
                <h2 class="nl-value__title">What you get every week</h2>
                <div class="nl-value__grid">
                    <div class="nl-value__item">
                        <div class="nl-value__icon">&#9733;</div>
                        <div>
                            <div class="nl-value__item-title">Active role count</div>
                            <div class="nl-value__item-desc">Total FDE postings tracked, week-over-week change, and new openings by company.</div>
                        </div>
                    </div>
                    <div class="nl-value__item">
                        <div class="nl-value__icon">&#9733;</div>
                        <div>
                            <div class="nl-value__item-title">Salary benchmarks</div>
                            <div class="nl-value__item-desc">Median, average, and range from postings that disclosed pay. Updated every cycle.</div>
                        </div>
                    </div>
                    <div class="nl-value__item">
                        <div class="nl-value__icon">&#9733;</div>
                        <div>
                            <div class="nl-value__item-title">Top companies</div>
                            <div class="nl-value__item-desc">Which companies have the most open roles, who just started hiring, who pulled back.</div>
                        </div>
                    </div>
                    <div class="nl-value__item">
                        <div class="nl-value__icon">&#9733;</div>
                        <div>
                            <div class="nl-value__item-title">Market signal</div>
                            <div class="nl-value__item-desc">One data point from the full dataset each week: a skills breakdown, location chart, or team structure stat.</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="nl-sample-section">
                <h2 class="nl-value__title">Sample issue</h2>
                <p style="color: var(--text-secondary); margin-bottom: 1.5rem; font-size: 0.95rem;">Here's what a typical FDE Pulse Brief looks like.</p>
                {sample_issue}
            </div>

            <div class="nl-past">
                <h2 class="nl-value__title">Past issues</h2>
                <div class="nl-past__card">
                    <div class="nl-past__icon">&#128240;</div>
                    <div>
                        <div class="nl-past__title">Issues archive coming soon</div>
                        <div class="nl-past__desc">The first FDE Pulse Brief goes out this week. Past issues will be archived here after the first few editions.</div>
                    </div>
                </div>
            </div>

            <div class="nl-faq">
                <h2 class="nl-value__title">FAQ</h2>
                {faq_html}
            </div>

            <div class="nl-bottom-cta">
                <h2 style="font-size:1.5rem; font-weight:700; margin-bottom:0.5rem;">Ready to subscribe?</h2>
                <p style="color:var(--text-secondary); margin-bottom:1.5rem;">Join engineers tracking the FDE market. Free, weekly, cancellable anytime.</p>
                <form class="signup-form nl-bottom-form" onsubmit="handleSignup(event, this)">
                    <input type="email" name="email" placeholder="you@company.com" required>
                    <button type="submit">Subscribe free</button>
                </form>
                <div class="signup-msg"></div>
                <div class="signup-trust" style="text-align:center;">Unsubscribe anytime. No spam. About 5 minutes to read.</div>
            </div>
        </div>'''

    page_css = '''
.nl-wrapper { max-width: 860px; margin: 0 auto; padding: 8rem 1.5rem 4rem; }

/* Hero */
.nl-hero { text-align: center; margin-bottom: 4rem; }
.nl-hero__badge {
    display: inline-flex; align-items: center; gap: 0.5rem;
    background: var(--bg-card); border: 1px solid var(--border);
    padding: 0.4rem 1rem; border-radius: var(--radius-full);
    font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 1.5rem;
}
.nl-hero__badge-dot {
    width: 8px; height: 8px; background: var(--success);
    border-radius: 50%; animation: pulse 2s infinite;
}
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.5;} }
.nl-hero__title { font-size: 3rem; font-weight: 700; margin-bottom: 1rem; line-height: 1.1; }
.nl-hero__sub { font-size: 1.15rem; color: var(--text-secondary); max-width: 560px; margin: 0 auto 2rem; line-height: 1.7; }
.nl-hero__form-wrap { max-width: 480px; margin: 0 auto; }
.nl-hero__form { margin-bottom: 0.5rem; }

/* Value props */
.nl-value { margin-bottom: 4rem; }
.nl-value__title { font-size: 1.5rem; font-weight: 700; margin-bottom: 1.5rem; }
.nl-value__grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; }
.nl-value__item {
    display: flex; gap: 1rem; align-items: flex-start;
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--radius-lg); padding: 1.25rem;
}
.nl-value__icon {
    font-size: 1.25rem; color: var(--amber-light);
    flex-shrink: 0; margin-top: 0.1rem;
}
.nl-value__item-title { font-weight: 600; color: var(--text-primary); margin-bottom: 0.25rem; }
.nl-value__item-desc { font-size: 0.9rem; color: var(--text-secondary); line-height: 1.6; }

/* Sample issue */
.nl-sample-section { margin-bottom: 4rem; }
.nl-sample {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--radius-xl); overflow: hidden;
}
.nl-sample__header {
    background: var(--bg-secondary); padding: 1.25rem 1.75rem;
    border-bottom: 1px solid var(--border);
}
.nl-sample__label { font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.25rem; }
.nl-sample__title { font-size: 1.15rem; font-weight: 700; color: var(--text-primary); }
.nl-sample__body { padding: 1.5rem 1.75rem; }
.nl-sample__section { margin-bottom: 1.75rem; padding-bottom: 1.75rem; border-bottom: 1px solid var(--border-light); }
.nl-sample__section:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
.nl-sample__section-title { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; color: var(--amber-light); font-weight: 600; margin-bottom: 0.75rem; }
.nl-sample__stat-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
.nl-sample__stat { text-align: center; }
.nl-sample__stat-value { font-size: 1.5rem; font-weight: 700; color: var(--amber-light); }
.nl-sample__stat-label { font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem; }
.nl-sample__job { margin-bottom: 0.75rem; }
.nl-sample__job-title { font-size: 0.95rem; font-weight: 600; color: var(--text-primary); }
.nl-sample__job-meta { font-size: 0.85rem; color: var(--text-secondary); }

/* Past issues */
.nl-past { margin-bottom: 4rem; }
.nl-past__card {
    display: flex; gap: 1rem; align-items: flex-start;
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--radius-lg); padding: 1.25rem 1.5rem;
}
.nl-past__icon { font-size: 1.5rem; flex-shrink: 0; }
.nl-past__title { font-weight: 600; color: var(--text-primary); margin-bottom: 0.25rem; }
.nl-past__desc { font-size: 0.9rem; color: var(--text-secondary); }

/* FAQ */
.nl-faq { margin-bottom: 4rem; }

/* Bottom CTA */
.nl-bottom-cta {
    text-align: center;
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--radius-xl); padding: 2.5rem;
    position: relative; overflow: hidden;
}
.nl-bottom-cta::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--amber), transparent);
}
.nl-bottom-form { max-width: 440px; margin: 0 auto; }

@media (max-width: 768px) {
    .nl-wrapper { padding: 6rem 1rem 3rem; }
    .nl-hero__title { font-size: 2.25rem; }
    .nl-value__grid { grid-template-columns: 1fr; }
    .nl-sample__stat-row { grid-template-columns: repeat(2, 1fr); }
}
'''

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
            {"@type": "ListItem", "position": 2, "name": "Newsletter", "item": BASE_URL + "/newsletter/"}
        ]
    }, indent=2)

    extra_head = (
        f'<style>{page_css}</style>\n'
        f'    <script type="application/ld+json">\n{faq_schema}\n    </script>\n'
        f'    <script type="application/ld+json">\n{breadcrumb}\n    </script>'
    )

    html = get_html_head(
        title="FDE Pulse Brief: Weekly Forward Deployed Engineer Newsletter",
        description="Free weekly newsletter for Forward Deployed Engineers. Active job counts, salary data, top companies, new openings. Every Tuesday morning.",
        canonical_path="/newsletter/",
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

    os.makedirs(os.path.join(SITE_DIR, 'newsletter'), exist_ok=True)
    out_path = os.path.join(SITE_DIR, 'newsletter', 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  Newsletter page generated: {out_path} ({len(html):,} bytes)")


if __name__ == "__main__":
    generate_newsletter_page()
