#!/usr/bin/env python3
"""
Generate and send the FDE Pulse weekly newsletter email.

Compares this week's job data to last week's and produces a zero-writing-effort
email with active FDE roles, salary, top hiring companies, new companies this
week, skills in demand, and featured jobs.

Usage:
    python scripts/generate_weekly_email.py --preview          # Generate HTML preview
    python scripts/generate_weekly_email.py --send             # Send to all subscribers
    python scripts/generate_weekly_email.py --save-snapshot    # Save current data as baseline
"""

import argparse
import json
import os
import sys
import uuid
from datetime import datetime
from collections import Counter

# Allow `from track_helper import ...` when run as `python scripts/generate_weekly_email.py`
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from track_helper import embed_pixel, log_send

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
PREVIOUS_SNAPSHOT_FILE = os.path.join(DATA_DIR, 'previous_market_snapshot.json')

# Brand — FDE Pulse amber on dark
BRAND = {
    'bg': '#0F1923',
    'card_bg': '#162232',
    'card_hover': '#1C2D3F',
    'amber': '#F59E0B',
    'amber_light': '#FBBF24',
    'amber_dark': '#D97706',
    'green': '#4ade80',
    'red': '#f87171',
    'border': 'rgba(255,255,255,0.08)',
    'gray_100': 'rgba(255,255,255,0.85)',
    'gray_200': 'rgba(255,255,255,0.6)',
    'gray_300': 'rgba(255,255,255,0.4)',
    'white': '#ffffff',
}

FROM_EMAIL = "FDE Pulse <insights@fdepulse.com>"
SITE_URL = "https://fdepulse.com"
LIST_SLUG = "fde-pulse"

WORKER_URL = "https://newsletter-subscribe.rome-workers.workers.dev"


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_current_data():
    """Load current market intelligence, comp analysis, and jobs."""
    mi_path = os.path.join(DATA_DIR, 'market_intelligence.json')
    ca_path = os.path.join(DATA_DIR, 'comp_analysis.json')
    jobs_path = os.path.join(DATA_DIR, 'jobs.json')

    if not os.path.exists(mi_path) or not os.path.exists(jobs_path):
        return None, None, []

    with open(mi_path) as f:
        market_intel = json.load(f)

    comp_analysis = {}
    if os.path.exists(ca_path):
        with open(ca_path) as f:
            comp_analysis = json.load(f)

    with open(jobs_path) as f:
        data = json.load(f)
        if isinstance(data, list):
            jobs = data
        elif isinstance(data, dict):
            jobs = data.get('jobs', [])
        else:
            jobs = []

    return market_intel, comp_analysis, jobs


def load_previous_snapshot():
    """Load previous week's snapshot for diff calculation."""
    if os.path.exists(PREVIOUS_SNAPSHOT_FILE):
        with open(PREVIOUS_SNAPSHOT_FILE) as f:
            return json.load(f)
    return None


def save_current_as_snapshot(market_intel, comp_analysis, jobs, previous):
    """Save current data as snapshot for next week's diff."""
    issue_number = (previous or {}).get('issue_number', 0) + 1
    snapshot = {
        'snapshot_date': datetime.now().isoformat(),
        'issue_number': issue_number,
        'total_jobs': len(jobs) if jobs else market_intel.get('total_jobs', 0) if market_intel else 0,
        'salary_median': comp_analysis.get('salary_stats', {}).get('median', 0) if comp_analysis else 0,
        'top_companies': [],
        'all_companies_seen': list(set(j.get('company_name') or j.get('company') or '' for j in jobs if j)),
    }
    with open(PREVIOUS_SNAPSHOT_FILE, 'w') as f:
        json.dump(snapshot, f, indent=2)


# ---------------------------------------------------------------------------
# Diff computation
# ---------------------------------------------------------------------------

def compute_diff(market_intel, comp_analysis, jobs, previous):
    """Compute WoW deltas + section data."""
    total_jobs = len(jobs) if jobs else (market_intel.get('total_jobs', 0) if market_intel else 0)
    salary_median = comp_analysis.get('salary_stats', {}).get('median', 0) if comp_analysis else 0

    # WoW deltas
    prev_total = (previous or {}).get('total_jobs', total_jobs)
    prev_median = (previous or {}).get('salary_median', salary_median)
    jobs_delta = total_jobs - prev_total
    median_delta = salary_median - prev_median

    # Top hiring companies (top 8 by post count)
    company_counts = Counter()
    for j in jobs:
        c = j.get('company_name') or j.get('company') or ''
        if c:
            company_counts[c] += 1
    top_companies = company_counts.most_common(8)

    # Companies new this week (FDE-specific)
    # A "new" company is one not in previous snapshot's all_companies_seen
    prev_companies = set((previous or {}).get('all_companies_seen', []))
    current_companies = set(c for c, _ in company_counts.items())
    new_companies = sorted(current_companies - prev_companies)[:8]

    # Skills/tools in demand (top 10 by mention count)
    tools = market_intel.get('tools', []) if market_intel else []
    if isinstance(tools, dict):
        tools_list = sorted(tools.items(), key=lambda x: -x[1])[:10]
    else:
        # tools can be list of {name, count}
        tools_list = [(t.get('name') or t.get('tool'), t.get('count') or t.get('mentions') or 0)
                      for t in tools[:10] if isinstance(t, dict)]

    # Featured jobs (top 5–8 with comp visible)
    featured = [j for j in jobs if (j.get('annual_salary_min') or j.get('compensation', {}).get('min'))][:8]
    if len(featured) < 5:
        # Fall back to first 5 jobs even without comp
        featured = jobs[:5]

    return {
        'total_jobs': total_jobs,
        'jobs_delta': jobs_delta,
        'salary_median': salary_median,
        'median_delta': median_delta,
        'top_companies': top_companies,
        'new_companies': new_companies,
        'tools': tools_list,
        'featured': featured,
    }


def fmt_delta(delta, prefix='', suffix=''):
    """Format a WoW delta with arrow + color hint, returns (text, color)."""
    if delta == 0:
        return ('— flat vs last week', BRAND['gray_300'])
    arrow = '&#9650;' if delta > 0 else '&#9660;'
    color = BRAND['green'] if delta > 0 else BRAND['red']
    return (f'{arrow} {prefix}{abs(delta):,}{suffix} vs last week', color)


def fmt_salary(n):
    """Format salary like $165K."""
    if not n:
        return '—'
    if n >= 1000:
        return f'${int(n / 1000)}K'
    return f'${int(n)}'


# ---------------------------------------------------------------------------
# HTML rendering
# ---------------------------------------------------------------------------

def generate_email_html(diff, date_str, issue_number):
    """Render the full FDE Pulse weekly email HTML."""

    # WoW deltas
    jobs_delta_text, jobs_delta_color = fmt_delta(diff['jobs_delta'])
    median_delta_text, median_delta_color = fmt_delta(
        diff['median_delta'], prefix='$', suffix=''
    )

    # Section 4: Top hiring companies
    companies_html = ""
    for company, count in diff['top_companies']:
        companies_html += f"""
        <tr>
          <td style="padding: 10px 16px; border-bottom: 1px solid {BRAND['border']};">
            <span style="color: {BRAND['white']}; font-weight: 600;">{company}</span>
          </td>
          <td style="padding: 10px 16px; border-bottom: 1px solid {BRAND['border']}; text-align: right;">
            <span style="color: {BRAND['amber']}; font-weight: 700;">{count}</span>
            <span style="color: {BRAND['gray_300']}; font-size: 12px;"> open</span>
          </td>
        </tr>"""
    if not companies_html:
        companies_html = f'<tr><td style="padding: 16px; color: {BRAND["gray_300"]};">No company data yet</td></tr>'

    # Section 5: Companies new this week (FDE-specific)
    new_companies_html = ""
    if diff['new_companies']:
        for c in diff['new_companies']:
            new_companies_html += f"""
            <span style="display: inline-block; background: {BRAND['amber_dark']}; color: {BRAND['white']};
                         padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600;
                         margin: 4px 6px 4px 0;">{c}</span>"""
    else:
        new_companies_html = f'<span style="color: {BRAND["gray_300"]};">No new companies this week</span>'

    # Section 6: Skills/tools in demand
    tools_html = ""
    for name, count in diff['tools']:
        if not name:
            continue
        tools_html += f"""
        <tr>
          <td style="padding: 8px 16px; border-bottom: 1px solid {BRAND['border']};">
            <span style="color: {BRAND['white']};">{name}</span>
          </td>
          <td style="padding: 8px 16px; border-bottom: 1px solid {BRAND['border']}; text-align: right;">
            <span style="color: {BRAND['amber']}; font-family: 'Source Code Pro', monospace; font-weight: 600;">{count}</span>
          </td>
        </tr>"""
    if not tools_html:
        tools_html = f'<tr><td style="padding: 16px; color: {BRAND["gray_300"]};">Skills data populating</td></tr>'

    # Section 7: Featured jobs
    featured_html = ""
    for j in diff['featured']:
        title = j.get('title', '')
        company = j.get('company_name') or j.get('company') or 'Company'
        location = j.get('location_raw') or j.get('location') or ''
        if j.get('is_remote'):
            location = 'Remote' if not location else f'{location} (Remote)'
        url = j.get('source_url') or j.get('url') or '#'

        # Comp may be in nested compensation dict (Fractional pattern) or flat
        salary_min = j.get('annual_salary_min') or j.get('compensation', {}).get('min')
        salary_max = j.get('annual_salary_max') or j.get('compensation', {}).get('max')
        salary = ''
        if salary_min and salary_max:
            salary = f'{fmt_salary(int(salary_min))} – {fmt_salary(int(salary_max))}'
        elif salary_min:
            salary = f'From {fmt_salary(int(salary_min))}'

        salary_badge = ''
        if salary:
            salary_badge = f'<span style="display: inline-block; background: rgba(245,158,11,0.15); color: {BRAND["amber"]}; font-size: 12px; font-weight: 600; padding: 2px 8px; border-radius: 4px; margin-left: 8px;">{salary}</span>'

        featured_html += f"""
        <tr>
          <td style="padding: 12px 16px; border-bottom: 1px solid {BRAND['border']};">
            <a href="{url}" style="color: {BRAND['white']}; text-decoration: none; font-weight: 600; font-size: 14px;">{title}</a>{salary_badge}<br>
            <span style="color: {BRAND['gray_300']}; font-size: 13px;">{company} &middot; {location}</span>
          </td>
        </tr>"""
    if not featured_html:
        featured_html = f'<tr><td style="padding: 16px; color: {BRAND["gray_300"]};">No jobs available yet — first scrape pending</td></tr>'

    # Full HTML
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FDE Pulse — Weekly Issue {issue_number}</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Source+Code+Pro:wght@400;500;600&display=swap" rel="stylesheet">
</head>
<body style="margin: 0; padding: 0; background: {BRAND['bg']}; font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background: {BRAND['bg']};">
<tr><td align="center" style="padding: 20px 10px;">
<table width="600" cellpadding="0" cellspacing="0" style="max-width: 600px; width: 100%;">

  <!-- Header -->
  <tr><td style="padding: 24px 24px 20px;">
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td width="44" valign="middle">
          <div style="width: 40px; height: 40px;
                      background: linear-gradient(135deg, {BRAND['amber']} 0%, {BRAND['amber_dark']} 100%);
                      border-radius: 8px; text-align: center; line-height: 40px;
                      font-size: 20px; color: {BRAND['white']};">&#10148;</div>
        </td>
        <td valign="middle" style="padding-left: 12px;">
          <span style="font-size: 18px; font-weight: 700; color: {BRAND['white']};">FDE Pulse</span>
        </td>
      </tr>
    </table>
  </td></tr>

  <!-- Title -->
  <tr><td style="padding: 0 24px 16px; border-bottom: 2px solid {BRAND['amber']};">
    <h1 style="margin: 0 0 6px; font-size: 32px; font-weight: 700; color: {BRAND['white']}; letter-spacing: -0.5px;">FORWARD DEPLOYED PULSE</h1>
    <p style="margin: 0; font-size: 14px; color: {BRAND['gray_300']};">Issue #{issue_number} &middot; Week of {date_str} &middot; {diff['total_jobs']:,} active FDE roles</p>
  </td></tr>

  <!-- Section 2: Hero stat (Active Roles + WoW) + Section 3: Salary + WoW -->
  <tr><td style="padding: 24px 24px 12px;">
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td width="50%" style="padding-right: 6px;">
          <table width="100%" cellpadding="0" cellspacing="0" style="background: {BRAND['card_bg']}; border-radius: 8px;">
            <tr><td style="padding: 16px 20px;">
              <div style="font-size: 11px; color: {BRAND['gray_300']}; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">Active FDE Roles</div>
              <div style="font-size: 32px; font-weight: 700; color: {BRAND['amber']};">{diff['total_jobs']:,}</div>
              <div style="font-size: 12px; color: {jobs_delta_color}; margin-top: 6px;">{jobs_delta_text}</div>
            </td></tr>
          </table>
        </td>
        <td width="50%" style="padding-left: 6px;">
          <table width="100%" cellpadding="0" cellspacing="0" style="background: {BRAND['card_bg']}; border-radius: 8px;">
            <tr><td style="padding: 16px 20px;">
              <div style="font-size: 11px; color: {BRAND['gray_300']}; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">Median Salary</div>
              <div style="font-size: 32px; font-weight: 700; color: {BRAND['amber']};">{fmt_salary(diff['salary_median'])}</div>
              <div style="font-size: 12px; color: {median_delta_color}; margin-top: 6px;">{median_delta_text}</div>
            </td></tr>
          </table>
        </td>
      </tr>
    </table>
  </td></tr>

  <!-- Section 4: Top hiring companies -->
  <tr><td style="padding: 12px 24px;">
    <h2 style="margin: 16px 0 8px; font-size: 14px; font-weight: 700; color: {BRAND['amber']}; text-transform: uppercase; letter-spacing: 1.5px;">Top Hiring Companies</h2>
    <table width="100%" cellpadding="0" cellspacing="0" style="background: {BRAND['card_bg']}; border-radius: 8px;">
      {companies_html}
    </table>
  </td></tr>

  <!-- Section 5: Companies new this week -->
  <tr><td style="padding: 12px 24px;">
    <h2 style="margin: 16px 0 8px; font-size: 14px; font-weight: 700; color: {BRAND['amber']}; text-transform: uppercase; letter-spacing: 1.5px;">Companies New This Week</h2>
    <div style="background: {BRAND['card_bg']}; border-radius: 8px; padding: 16px;">
      {new_companies_html}
    </div>
  </td></tr>

  <!-- Section 6: Skills in demand -->
  <tr><td style="padding: 12px 24px;">
    <h2 style="margin: 16px 0 8px; font-size: 14px; font-weight: 700; color: {BRAND['amber']}; text-transform: uppercase; letter-spacing: 1.5px;">Skills In Demand</h2>
    <table width="100%" cellpadding="0" cellspacing="0" style="background: {BRAND['card_bg']}; border-radius: 8px;">
      {tools_html}
    </table>
  </td></tr>

  <!-- Section 7: Featured jobs -->
  <tr><td style="padding: 12px 24px 24px;">
    <h2 style="margin: 16px 0 8px; font-size: 14px; font-weight: 700; color: {BRAND['amber']}; text-transform: uppercase; letter-spacing: 1.5px;">Featured Jobs</h2>
    <table width="100%" cellpadding="0" cellspacing="0" style="background: {BRAND['card_bg']}; border-radius: 8px;">
      {featured_html}
    </table>
    <p style="margin: 12px 0 0; text-align: center;">
      <a href="{SITE_URL}/jobs/" style="color: {BRAND['amber']}; text-decoration: none; font-weight: 600; font-size: 14px;">See all {diff['total_jobs']:,} FDE roles &rarr;</a>
    </p>
  </td></tr>

  <!-- Section 8: Footer -->
  <tr><td style="padding: 16px 24px; border-top: 1px solid {BRAND['border']}; text-align: center;">
    <p style="margin: 0; font-size: 12px; color: {BRAND['gray_300']}; line-height: 1.8;">
      <a href="{SITE_URL}" style="color: {BRAND['amber']}; text-decoration: none; font-weight: 600;">FDE Pulse</a> &middot; Career intelligence for Forward Deployed Engineers<br>
      Data from active job postings, updated every Tuesday.<br>
      <a href="{SITE_URL}/newsletter/" style="color: {BRAND['gray_300']}; text-decoration: underline;">Subscribe</a> &middot;
      <a href="{{{{unsubscribe_url}}}}" style="color: {BRAND['gray_300']}; text-decoration: underline;">Unsubscribe</a> &middot;
      <a href="{SITE_URL}" style="color: {BRAND['gray_300']}; text-decoration: underline;">fdepulse.com</a>
    </p>
  </td></tr>

</table>
</td></tr>
</table>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Subscriber management (Cloudflare D1 via newsletter-subscribe worker)
# ---------------------------------------------------------------------------

def load_subscribers_from_d1():
    """Load active subscribers for fde-pulse from D1 via the worker API.

    Requires API_SECRET env var (matches the worker's API_SECRET secret).
    Returns list of dicts: {email, name, unsubscribe_token}.
    """
    import requests as req

    api_secret = os.environ.get('API_SECRET') or os.environ.get('NEWSLETTER_API_SECRET', '')
    if not api_secret:
        print("Error: API_SECRET not set (needed to fetch subscribers from D1)")
        return []

    try:
        resp = req.get(
            f"{WORKER_URL}/subscribers/{LIST_SLUG}",
            headers={"Authorization": f"Bearer {api_secret}"},
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error fetching subscribers from D1: {e}")
        return []


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='FDE Pulse weekly email')
    parser.add_argument('--preview', action='store_true', help='Generate HTML preview')
    parser.add_argument('--send', action='store_true', help='Send to all subscribers via Resend')
    parser.add_argument('--save-snapshot', action='store_true', help='Save current data as baseline')
    parser.add_argument('--resend-key', type=str, help='Resend API key (or set RESEND_API_KEY)')
    args = parser.parse_args()

    # Load data
    market_intel, comp_analysis, jobs = load_current_data()
    if market_intel is None:
        print("No data found. Run scraper export first: python3 -m src.cli export --audience fde --push")
        return

    previous = load_previous_snapshot()
    diff = compute_diff(market_intel, comp_analysis, jobs, previous)

    issue_number = (previous or {}).get('issue_number', 0) + 1
    date_str = datetime.now().strftime('%B %d, %Y')

    # Diff summary line for subject
    subject = f"FDE Pulse: {diff['total_jobs']:,} roles, {fmt_salary(diff['salary_median'])} median"

    # Render HTML
    html = generate_email_html(diff, date_str, issue_number)

    if args.preview:
        preview_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'email-preview.html')
        with open(preview_path, 'w') as f:
            f.write(html)
        print(f"Preview saved to: {preview_path}")
        print(f"Subject: {subject}")
        print(f"Open: file://{preview_path}")
        return

    if args.save_snapshot:
        save_current_as_snapshot(market_intel, comp_analysis, jobs, previous)
        print(f"Snapshot saved to {PREVIOUS_SNAPSHOT_FILE}")
        return

    if args.send:
        try:
            import resend
        except ImportError:
            print("Error: 'resend' package not installed. Run: pip install resend")
            sys.exit(1)

        api_key = args.resend_key or os.environ.get('RESEND_API_KEY', '')
        if not api_key:
            print("Error: Resend API key required. Use --resend-key or set RESEND_API_KEY")
            sys.exit(1)

        resend.api_key = api_key

        print("Fetching subscribers from D1...")
        subs = load_subscribers_from_d1()
        if not subs:
            print(f"No subscribers found for list '{LIST_SLUG}'. Sign up at {SITE_URL}/newsletter/")
            return
        print(f"  D1: {len(subs)} subscribers")

        unsub_base = f"{WORKER_URL}/unsubscribe"

        print(f"Sending to {len(subs)} subscribers...")
        sent = 0
        errors = 0
        for sub in subs:
            unsub_url = f"{unsub_base}?token={sub['unsubscribe_token']}"
            personalized = html.replace("{{unsubscribe_url}}", unsub_url)
            send_id = uuid.uuid4().hex
            tracked_html = embed_pixel(personalized, send_id)

            try:
                resend.Emails.send({
                    "from": FROM_EMAIL,
                    "to": [sub['email']],
                    "subject": subject,
                    "html": tracked_html,
                    "headers": {
                        "List-Unsubscribe": f"<{unsub_url}>",
                        "List-Unsubscribe-Post": "List-Unsubscribe=One-Click",
                    },
                })
                sent += 1
                log_send(send_id, LIST_SLUG, sub['email'], subject)
                print(f"  Sent: {sub['email']}")
            except Exception as e:
                errors += 1
                print(f"  Failed: {sub['email']} - {e}")

        print(f"\nSent {sent}/{len(subs)} emails ({errors} errors)")

        # Save snapshot for next week's WoW diff
        save_current_as_snapshot(market_intel, comp_analysis, jobs, previous)
        print(f"Snapshot saved for next week's comparison")
        return

    parser.print_help()


if __name__ == '__main__':
    main()
