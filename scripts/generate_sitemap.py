#!/usr/bin/env python3
"""
Generate XML sitemap for FDE Pulse.
Scans site/ directory for all HTML files and generates sitemap.xml.
"""

import os
import sys
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from nav_config import BASE_URL

SITE_DIR = os.path.join(os.path.dirname(script_dir), 'site')


def generate_sitemap():
    print("  Generating sitemap...")

    urls = []
    for root, dirs, files in os.walk(SITE_DIR):
        for f in files:
            if not f.endswith('.html'):
                continue
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, SITE_DIR)

            # Skip noindex check
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as fh:
                head = fh.read(2000)
                if 'noindex' in head:
                    continue

            # Build URL
            if rel_path == 'index.html':
                url_path = '/'
            elif rel_path.endswith('/index.html'):
                url_path = '/' + rel_path.replace('/index.html', '/')
            else:
                url_path = '/' + rel_path

            # Priority based on depth
            depth = url_path.count('/') - 1
            if url_path == '/':
                priority = '1.0'
                changefreq = 'weekly'
            elif depth <= 1:
                priority = '0.8'
                changefreq = 'weekly'
            else:
                priority = '0.6'
                changefreq = 'monthly'

            urls.append({
                'loc': f"{BASE_URL}{url_path}",
                'lastmod': datetime.now().strftime('%Y-%m-%d'),
                'changefreq': changefreq,
                'priority': priority,
            })

    # Sort: homepage first, then alphabetical
    urls.sort(key=lambda u: (0 if u['loc'] == f"{BASE_URL}/" else 1, u['loc']))

    # Write sitemap
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml += f'''  <url>
    <loc>{url['loc']}</loc>
    <lastmod>{url['lastmod']}</lastmod>
    <changefreq>{url['changefreq']}</changefreq>
    <priority>{url['priority']}</priority>
  </url>\n'''
    xml += '</urlset>\n'

    output_path = os.path.join(SITE_DIR, 'sitemap.xml')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml)

    print(f"  Sitemap generated: {len(urls)} URLs")
    return len(urls)


if __name__ == "__main__":
    generate_sitemap()
