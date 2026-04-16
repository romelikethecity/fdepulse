#!/usr/bin/env python3
"""
Navigation configuration for FDE Pulse.
Single source of truth for all navigation elements.
"""

# Site information
SITE_NAME = "FDE Pulse"
SITE_TAGLINE = "Jobs & Market Intelligence for Forward Deployed Engineers"
BASE_URL = "https://fdepulse.com"
LOGO_TEXT = "FDE"

# Main navigation items
NAV_ITEMS = [
    {"label": "Jobs", "href": "/jobs/"},
    {"label": "Salaries", "href": "/salaries/"},
    {"label": "Companies", "href": "/companies/"},
    {"label": "Career", "href": "/career/"},
    {"label": "Insights", "href": "/insights/"},
    {"label": "Top Voices", "href": "/voices/"},
    {"label": "About", "href": "/about/"},
]

# Header CTA button
HEADER_CTA = {
    "label": "Subscribe",
    "href": "#subscribe",
}

# Footer configuration
FOOTER_COLUMNS = [
    {
        "title": "Jobs",
        "links": [
            {"label": "All FDE Jobs", "href": "/jobs/"},
            {"label": "Remote FDE Jobs", "href": "/jobs/remote/"},
            {"label": "FDE Jobs in SF", "href": "/jobs/san-francisco/"},
            {"label": "FDE Jobs in NYC", "href": "/jobs/new-york/"},
        ]
    },
    {
        "title": "Resources",
        "links": [
            {"label": "Salary Data", "href": "/salaries/"},
            {"label": "Companies Hiring", "href": "/companies/"},
            {"label": "Market Insights", "href": "/insights/"},
            {"label": "Top Voices", "href": "/voices/"},
        ]
    },
    {
        "title": "Company",
        "links": [
            {"label": "About", "href": "/about/"},
            {"label": "Newsletter", "href": "#subscribe"},
            {"label": "Contact", "href": "mailto:hello@fdepulse.com"},
        ]
    },
    {
        "title": "Related Sites",
        "links": [
            {"label": "The GTM Index", "href": "https://thegtmindex.com", "external": True},
            {"label": "Fractional Pulse", "href": "https://fractionalpulse.com", "external": True},
            {"label": "CRO Report", "href": "https://thecroreport.com", "external": True},
            {"label": "RevOps Report", "href": "https://therevopsreport.com", "external": True},
            {"label": "AI Market Pulse", "href": "https://theaimarketpulse.com", "external": True},
            {"label": "GTME Pulse", "href": "https://gtmepulse.com", "external": True},
        ]
    },
]

# Company categories for browse section
COMPANY_CATEGORIES = [
    {
        "id": "ai",
        "title": "AI / ML",
        "icon": ">>",
        "examples": "OpenAI, Anthropic, Cohere, Databricks",
    },
    {
        "id": "enterprise",
        "title": "Enterprise SaaS",
        "icon": ">>",
        "examples": "Salesforce, Ramp, Rippling, ServiceNow",
    },
    {
        "id": "startup",
        "title": "Startups",
        "icon": ">>",
        "examples": "PostHog, Watershed, Onyx, Commure",
    },
    {
        "id": "consulting",
        "title": "Consulting",
        "icon": ">>",
        "examples": "PwC, Deloitte, Accenture",
    },
]

# Social links
SOCIAL_LINKS = []

# Copyright text
COPYRIGHT_TEXT = f"© 2026 {SITE_NAME}. All rights reserved."
